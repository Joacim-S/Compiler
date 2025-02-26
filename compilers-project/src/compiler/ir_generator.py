# src/compiler/ir_generator.py

from compiler import ast, ir
from compiler.symtab import SymTab
from compiler.types import Bool, Int, Type, Unit

def generate_ir(
    # 'root_types' parameter should map all global names
    # like 'print_int' and '+' to their types.
    root_types: dict[ir.IRVar, Type],
    root_expr: ast.Expression
) -> list[ir.Instruction]:
    var_types: dict[ir.IRVar, Type] = root_types.copy()

    # 'var_unit' is used when an expression's type is 'Unit'.
    var_unit = ir.IRVar('unit')
    var_types[var_unit] = Unit

    def new_var(t: Type) -> ir.IRVar:
        # Create a new unique IR variable and
        # add it to var_types
        ...

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
                return st.require(expr.name)

            # Other AST node cases (see below)

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
    var_final_result = visit(root_symtab, root_expr)

    if var_types[var_final_result] == Int:
        ... # Emit a call to 'print_int'
    elif var_types[var_final_result] == Bool:
        ... # Emit a call to 'print_bool'

    return ins
