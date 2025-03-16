from compiler import ir
from compiler.intrinsics import all_intrinsics, IntrinsicArgs
import dataclasses

class Locals:
    """Knows the memory location of every local variable."""
    _var_to_location: dict[ir.IRVar, str]
    _stack_used: int

    def __init__(self, variables: list[ir.IRVar]) -> None:
        loc = 0
        self._var_to_location = {}
        for v in variables:
            loc -= 8
            self._var_to_location[v] = f'{loc}(%rbp)'
        self._stack_used = -loc

    def get_ref(self, v: ir.IRVar) -> str:
        """Returns an Assembly reference like `-24(%rbp)`
        for the memory location that stores the given variable"""
        return self._var_to_location[v]

    def stack_used(self) -> int:
        """Returns the number of bytes of stack space needed for the local variables."""
        return self._stack_used

def get_all_ir_variables(instructions: list[ir.Instruction]) -> list[ir.IRVar]:
    result_list: list[ir.IRVar] = []
    result_set: set[ir.IRVar] = set()

    def add(v: ir.IRVar) -> None:
        if v not in result_set:
            result_list.append(v)
            result_set.add(v)

    for insn in instructions:
        for field in dataclasses.fields(insn):
            value = getattr(insn, field.name)
            if isinstance(value, ir.IRVar):
                add(value)
            elif isinstance(value, list):
                for v in value:
                    if isinstance(v, ir.IRVar):
                        add(v)
    return result_list

def generate_assembly(functions: dict[str, list[ir.Instruction]]) -> str:
    lines = []
    def emit(line: str) -> None: lines.append(line)
    emit('.extern print_int')
    emit('.extern print_bool')
    emit('.extern read_int')
    emit('.section .text')

    for name, instructions in functions.items():
        emit(f'.global {name}')
        emit(f'.type {name}, @function')
        emit(f'{name}:')

        locals = Locals(
            variables=get_all_ir_variables(instructions)
        )

        for key, val in locals._var_to_location.items():
            emit(f'# {key} in {val}')
        emit('pushq %rbp')
        emit('movq %rsp, %rbp')
        emit(f'subq ${locals.stack_used()}, %rsp')

        for insn in instructions:
            emit('# ' + str(insn))
            match insn:
                case ir.Label():
                    emit("")
                    # ".L" prefix marks the symbol as "private".
                    # This makes GDB backtraces look nicer too:
                    # https://stackoverflow.com/a/26065570/965979
                    emit(f'.L{insn.name}:')
                case ir.LoadIntConst():
                    if -2**31 <= insn.value < 2**31:
                        emit(f'movq ${insn.value}, {locals.get_ref(insn.dest)}')
                    else:
                        # Due to a quirk of x86-64, we must use
                        # a different instruction for large integers.
                        # It can only write to a register,
                        # not a memory location, so we use %rax
                        # as a temporary.
                        emit(f'movabsq ${insn.value}, %rax')
                        emit(f'movq %rax, {locals.get_ref(insn.dest)}')
                        
                case ir.Jump():
                    emit(f'jmp .L{insn.label.name}')
                    
                case ir.LoadBoolConst():
                    emit(f'movq ${int(insn.value)}, {locals.get_ref(insn.dest)}')
                
                case ir.Copy():
                    emit(f'movq {locals.get_ref(insn.source)}, %rax')
                    emit(f'movq %rax, {locals.get_ref(insn.dest)}')
                    
                case ir.CondJump():
                    emit(f'cmpq $0, {locals.get_ref(insn.cond)}')
                    emit(f'jne .L{insn.then_label.name}')
                    emit(f'jmp .L{insn.else_label.name}')
                
                case ir.Call():
                    registers = ['rdi','rsi','rdx','rcx','r8','r9']
                    f = insn.fun
                    if f.name in all_intrinsics.keys():
                        all_intrinsics[f.name](IntrinsicArgs(
                            arg_refs=[locals.get_ref(a) for a in insn.args],
                            result_register='%rax',
                            emit = emit
                        ))
                    else:
                        for i in range(len(insn.args)):
                            emit(f'movq {locals.get_ref(insn.args[i])}, %{registers[i]}')
                        emit(f'callq {f.name}')
                    emit(f'movq %rax, {locals.get_ref(insn.dest)}')
                    
                        
            emit('')
                
        emit(f'movq $0, %rax')
        emit(f'movq %rbp, %rsp')
        emit(f'popq %rbp')
        emit(f'ret')
        emit(f'')
    
    return '\n'.join(lines)