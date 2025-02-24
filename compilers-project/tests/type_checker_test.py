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

def test_declarations_assignments_ops() -> None:
  assert typecheck(
    ast.Block(
      L,
      [ast.Declaration(
        L,
        ast.Identifier(L, 'a'),
        ast.Literal(L, True)
      ),
       ast.Declaration(
        L,
        ast.Identifier(L, 'b'),
        ast.Literal(L, True)
      ),
    ], ast.BinaryOp(
      L,
      ast.Identifier(L, 'a'),
      'and',
      ast.Identifier(L, 'b')
    )), TypeTab
  ) == Bool
  
def test_unary() -> None:
  assert typecheck(
    ast.Block(
      L,
      [ast.Declaration(
        L,
        ast.Identifier(L, 'a'),
        ast.Literal(L, True)
      ),
       ast.Declaration(
        L,
        ast.Identifier(L, 'b'),
        ast.Literal(L, True)
      ),
       ast.Declaration(
        L,
        ast.Identifier(L, 'c'),
        ast.Unary(L, 'not', ast.Identifier(L, 'b'))
      ),
    ], ast.BinaryOp(
      L,
      ast.Identifier(L, 'c'),
      'and',
      ast.Identifier(L, 'b')
    )), TypeTab
  ) == Bool
  
  assert typecheck(
    ast.BinaryOp(
      L,
      ast.Literal(L, 5),
      '+',
      ast.Unary(L, '-', ast.Literal(L, 5)),
    ), TypeTab
  ) == Int
  
  try:
    typecheck(
      ast.BinaryOp(
        L,
        ast.Literal(L, 5),
        '+',
        ast.Unary(L, 'not',  ast.Literal(L, 5)),
      ), TypeTab
    )
    assert False == True
  except Exception as exc:
    assert exc.args[0] ==  """Location(file='L', line=-1, column=-1): Unsupported parameters for 'unary_not' Expected: (Type(type=<class 'bool'>),) got: (Type(type=<class 'int'>),)"""
    
def test_function_call() -> None:
  assert typecheck(
    ast.FunctionCall(
      L,
      ast.Identifier(L, 'print_int'),
      [ast.Literal(L, 10)]
    ), TypeTab
  ) == Unit
  
  assert typecheck(
    ast.Block(
      L,
      [ast.Declaration(L, ast.Identifier(L, 'f'), ast.Identifier(L, 'print_int'))],
      ast.FunctionCall(L, ast.Identifier(L, 'f'), [ast.Literal(L, 10)])
    ), TypeTab
  ) == Unit