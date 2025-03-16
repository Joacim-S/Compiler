# src/compiler/ir_generator.py

from compiler import ast, ir
from compiler.symtab import SymTab
from compiler.types import Bool, Int, Type, Unit
from compiler.location import Location, L

def generate_ir(
    # 'root_types' parameter should map all global names
    # like 'print_int' and '+' to their types.
    root_types: dict[ir.IRVar, Type],
    root_module: ast.Module
) -> dict[str, list[ir.Instruction]]:
    var_types: dict[ir.IRVar, Type] = root_types.copy()

    # 'var_unit' is used when an expression's type is 'Unit'.
    var_unit = ir.IRVar('unit')
    var_types[var_unit] = Unit
    
    var_num = 1
    label_num = 1
    
    unit_label = ir.Label(L, 'UnitLabel')
    
    in_loop_start: ir.Label = unit_label
    in_loop_end: ir.Label = unit_label

    def new_var(t: Type) -> ir.IRVar:
        nonlocal var_num
        # Create a new unique IR variable and
        # add it to var_types
        var = ir.IRVar(f'x{var_num}')
        var_num += 1
        var_types[var] = t
        return var
    
    def new_label(loc: Location) -> ir.Label:
        nonlocal label_num
        label = ir.Label(loc, f'L{label_num}')
        label_num += 1
        return label

    # We collect the IR instructions that we generate
    # into this list.
    ins: list[ir.Instruction] = []

    # This function visits an AST node,
    # appends IR instructions to 'ins',
    # and returns the IR variable where
    # the emitted IR instructions put the result.
    #
    # It uses a symbol table to map local variables
    # (which may be shadowed) to unique IR variables.
    # The symbol table will be updated in the same way as
    # in the interpreter and type checker.
    def visit(st: SymTab[ir.IRVar], expr: ast.Expression) -> ir.IRVar:
        loc = expr.location
        nonlocal in_loop_start
        nonlocal in_loop_end

        match expr:
            case ast.Literal():
                # Create an IR variable to hold the value,
                # and emit the correct instruction to
                # load the constant value.
                match expr.value:
                    case bool():
                        var = new_var(Bool)
                        ins.append(ir.LoadBoolConst(
                            loc, expr.value, var))
                    case int():
                        var = new_var(Int)
                        ins.append(ir.LoadIntConst(
                            loc, expr.value, var))
                    case None:
                        var = var_unit
                    case _:
                        raise Exception(f"{loc}: unsupported literal: {type(expr.value)}")

                # Return the variable that holds
                # the loaded value.
                return var

            case ast.Identifier():
                # Look up the IR variable that corresponds to
                # the source code variable.

                if expr.name in ('break', 'continue') and in_loop_start.name == 'unit_label':
                    raise Exception(f"{expr.name} not allowed outside of a loop")

                elif expr.name == 'break':
                    ins.append(ir.Jump(loc, in_loop_end))
                
                elif expr.name == 'continue':
                    ins.append(ir.Jump(loc, in_loop_start))

                return st.require(expr.name)
            
            case ast.BinaryOp():
                # Recursively emit instructions to calculate the operands.
                var_left = visit(st, expr.left)
                if expr.op in ['or', 'and']:
                    l_right = new_label(loc)
                    l_skip = new_label(loc)
                    l_end = new_label(loc)
                    if expr.op == 'or':
                        ins.append(ir.CondJump(loc, var_left, l_skip, l_right))
                    elif expr.op == 'and':
                        ins.append(ir.CondJump(loc, var_left, l_right, l_skip))
                    ins.append(l_right)
                    var_rigth = visit(st, expr.right)
                    var_result = new_var(expr.right.type)
                    ins.append(ir.Copy(loc, var_rigth, var_result))
                    ins.append(ir.Jump(loc, l_end))
                    ins.append(l_skip)
                    ins.append(ir.LoadBoolConst(loc, expr.op == 'or', var_result))
                    ins.append(l_end)
                    return var_result
                    

                var_right = visit(st, expr.right)
                # Generate variable to hold the result.
                # Emit a Call instruction that writes to that variable.
                if expr.op == '=':
                    if not isinstance(expr.left, ast.Identifier):
                        raise Exception
                    ins.append(ir.Copy(
                        loc, var_right, var_left))
                    return var_right

                var_result = new_var(expr.type)
                # Ask the symbol table to return the variable that refers
                # to the operator to call.
                var_op = st.require(expr.op)
                ins.append(ir.Call(
                    loc, var_op, [var_left, var_right], var_result))
                return var_result

            # Other AST node cases (see below)
            
            case ast.Condition():
                if expr.el is None:
                    # Create (but don't emit) some jump targets.
                    l_then = new_label(loc)
                    l_end = new_label(loc)

                    # Recursively emit instructions for
                    # evaluating the condition.
                    var_cond = visit(st, expr.con)
                    # Emit a conditional jump instruction
                    # to jump to 'l_then' or 'l_end',
                    # depending on the content of 'var_cond'.
                    ins.append(ir.CondJump(loc, var_cond, l_then, l_end))

                    # Emit the label that marks the beginning of
                    # the "then" branch.
                    ins.append(l_then)
                    # Recursively emit instructions for the "then" branch.
                    visit(st, expr.then)

                    # Emit the label that we jump to
                    # when we don't want to go to the "then" branch.
                    ins.append(l_end)

                    # An if-then expression doesn't return anything, so we
                    # return a special variable "unit".
                    return var_unit
                else:
                    # "if-then-else" case
                    l_then = new_label(loc)
                    l_else = new_label(loc)
                    l_end = new_label(loc)
                    var_cond = visit(st, expr.con)
                    var_result = new_var(expr.then.type)
                    ins.append(ir.CondJump(loc, var_cond, l_then, l_else))
                    ins.append(l_then)
                    var_then = visit(st, expr.then)
                    ins.append(ir.Copy(loc, var_then, var_result))
                    ins.append(ir.Jump(loc, l_end))
                    ins.append(l_else)
                    var_else = visit(st, expr.el)
                    ins.append(ir.Copy(loc, var_else, var_result))
                    ins.append(l_end)
                    return var_result
            
            case ast.Block():
                new_st = SymTab[ir.IRVar](parent = st)
                for b_expr in expr.content:
                    visit(new_st, b_expr)
                return visit(new_st, expr.val)
            
            case ast.Declaration():
                result = visit(st, expr.val)
                var = new_var(expr.val.type)
                st.add_local(expr.name.name, var)
                ins.append(ir.Copy(loc, result, var))
                
                return var_unit
            
            case ast.FunctionCall():
                f = st.require(expr.name.name)
                params = []
                for p in expr.params:
                    params.append(visit(st, p))
                var_result = new_var(expr.type)
                ins.append(ir.Call(loc, f, params, var_result))
                return var_result
            
            case ast.Unary():
                var_val = visit(st, expr.val)
                var_result = new_var(expr.val.type)
                f = st.require(f'unary_{expr.op}')
                ins.append(ir.Call(loc, f, [var_val], var_result))
                return var_result
            
            case ast.Loop():
                prev_start = in_loop_start
                prev_end = in_loop_end
                l_start = new_label(loc)
                l_body = new_label(loc)
                l_end = new_label(loc)
                in_loop_start = l_start
                in_loop_end = l_end
                
                ins.append(l_start)
                var_con = visit(st, expr.condition)
                ins.append(ir.CondJump(loc, var_con, l_body, l_end))
                ins.append(l_body)
                visit(st, expr.do)
                ins.append(ir.Jump(loc, l_start))
                ins.append(l_end)
                in_loop_start = prev_start
                in_loop_end = prev_end
                return var_unit
            
            case _:
                raise Exception

    # Convert 'root_types' into a SymTab
    # that maps all available global names to
    # IR variables of the same name.
    # In the Assembly generator stage, we will give
    # definitions for these globals. For now,
    # they just need to exist.
    root_symtab = SymTab[ir.IRVar](parent=None)
    for v in root_types.keys():
        root_symtab.add_local(v.name, v)

    # Start visiting the AST from the root.
    var_final_result = visit(root_symtab, root_module.body)

    if var_types[var_final_result] == Int:
        ins.append(ir.Call(
            root_module.body.location, ir.IRVar('print_int'), [var_final_result], new_var(var_types[var_final_result])
        ))
    elif var_types[var_final_result] == Bool:
        ins.append(ir.Call(
            root_module.body.location, ir.IRVar('print_bool'), [var_final_result], new_var(var_types[var_final_result])
        ))

    return {'main': ins}
