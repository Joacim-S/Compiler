import compiler.ast as ast
from compiler.interpreter import interperet
from compiler.tokenizer import Location
from compiler.symtab import SymTab, TopTab

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
  
def test_assignment() -> None:
  assert interperet(
    ast.Block(L,[
      ast.Declaration(L,
        ast.Identifier(L, 'a'),
        ast.Literal(L, 5)
      ),
      ast.BinaryOp(L,
      ast.Identifier(L, 'a'),
      '=',
      ast.Literal(L, 100),
    )
      ],
      ast.BinaryOp(L,
      ast.Identifier(L, 'a'),
      '*',
      ast.Literal(L, 10),
    )
    ), TopTab
  ) == 1000
  
  assert interperet(
    ast.Block(L,[
      ast.Declaration(L,
        ast.Identifier(L, 'a'),
        ast.Literal(L, 5)
      ),
      ast.BinaryOp(L,
      ast.Identifier(L, 'a'),
      '=',
        ast.BinaryOp(
          L,
          ast.Identifier(L, 'a'),
          '*',
          ast.Literal(L, 10)
        ),
    ),
      ],
      ast.BinaryOp(L,
      ast.Identifier(L, 'a'),
      '=',
        ast.BinaryOp(
          L,
          ast.Identifier(L, 'a'),
          '*',
          ast.Literal(L, 100)
        ),
    ),
    ), TopTab
  ) == 5000

def test_and_or() -> None:
  assert interperet(
    ast.BinaryOp(L,
      ast.Literal(L, True),
      'and',
      ast.Literal(L, True)
    ), TopTab
  ) == True
  
  assert interperet(
    ast.BinaryOp(L,
      ast.Literal(L, False),
      'and',
      ast.Literal(L, True)
    ), TopTab
  ) == False
  
  assert interperet(
    ast.BinaryOp(L,
      ast.Literal(L, True),
      'or',
      ast.Literal(L, False)
    ), TopTab
  ) == True
  
  assert interperet(
    ast.Block(
      L,
      [
        ast.Declaration(
          L,
          ast.Identifier(L, 'evr'),
          ast.Literal(L, False)
        ),
        ast.BinaryOp(
          L,
          ast.Literal(L, True),
          'or',
          ast.Block(
            L,
            [
              ast.BinaryOp(
                L,
                ast.Identifier(L, 'evr'),
                '=',
                ast.Literal(L, True)
              )
            ],
            ast.Literal(L, True)
          )
        )
      ],
      ast.Identifier(L, 'evr')
    ), TopTab
  ) == False
  
  assert interperet(
    ast.Block(
      L,
      [
        ast.Declaration(
          L,
          ast.Identifier(L, 'evr'),
          ast.Literal(L, False)
        ),
        ast.BinaryOp(
          L,
          ast.Literal(L, False),
          'and',
          ast.Block(
            L,
            [
              ast.BinaryOp(
                L,
                ast.Identifier(L, 'evr'),
                '=',
                ast.Literal(L, True)
              )
            ],
            ast.Literal(L, True)
          )
        )
      ],
      ast.Identifier(L, 'evr')
    ), TopTab
  ) == False
  
def test_loop() -> None:
  assert interperet(
    ast.Block(
      L,
      [ast.Declaration(
        L,
        ast.Identifier(L, 'a'),
        ast.Literal(L, 1)
      ),],
      ast.Loop(
        L,
        ast.BinaryOp(
          L,
          ast.Identifier(L, 'a'),
          '<',
          ast.Literal(L, 10)
        ),
        ast.BinaryOp(
          L,
          ast.Identifier(L, 'a'),
          '=',
          ast.BinaryOp(
            L,
            ast.Identifier(L,'a'),
            '+',
            ast.Literal(L,1)
          )
        )
      )
    ), TopTab
  ) == 10