import compiler.ast as ast
from compiler.interpreter import interperet
from compiler.tokenizer import Location
from compiler.symtab import TopTab

L = Location('L',-1, -1)

def test_2_plus_3() -> None:
  
  assert interperet(ast.BinaryOp(
      L,
        ast.Literal(L, 2),
        '+',
        ast.Literal(L, 3)
      ), TopTab) == 5
  
def test_conditioanls() -> None:
  
  assert interperet(
    ast.Condition(
      L,
      ast.Literal(L, False),
      ast.Literal(L, 2),
      ast.Literal(L, None)
      ), TopTab) == None
  
def test_blocks() -> None:
  
  assert interperet(
    ast.Block(
      L,
      [
        ast.Declaration(L, ast.Identifier(L, 'a'), ast.Literal(L, 1)),
        ast.BinaryOp(L, ast.Identifier(L, 'a'), '+', ast.Literal(L, 1))
      ],
      ast.BinaryOp(L, ast.Identifier(L, 'a'), '+', ast.Literal(L, 1))
    ),
    TopTab
  ) == 2