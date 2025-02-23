from compiler.type_checker import typecheck
from compiler.types import Int, Bool, Unit, Type, TypeTab
from compiler import ast
from compiler.ast import Location

L = Location('L',-1, -1)

def test_plus() -> None:
  assert typecheck(
    ast.BinaryOp(
      L,
      ast.Literal(L, 5),
      '+',
      ast.Literal(L, 5),
    ), TypeTab
  ) == Int