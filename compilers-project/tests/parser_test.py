from compiler.parser import parse
from compiler.tokenizer import Token, Location
import compiler.ast as ast

L = Location('L',-1, -1)

def test_one_plus_two_works() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='1'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='2')
  ]
  assert parse(tokens) == ast.BinaryOp(
      ast.Literal(1),
      '+',
      ast.Literal(2)
    )

def test_a_plus_two_works() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='2')
  ]
  assert parse(tokens) == ast.BinaryOp(
      ast.Identifier('a'),
      '+',
      ast.Literal(2)
    )
  
def test_addition_multiplication_presedence() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='1'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='int_literal', text='*'),
    Token(loc=L, type='int_literal', text='3'),
  ]
  assert parse(tokens) == ast.BinaryOp(
    left = ast.Literal(1),
    op = '+',
    right = ast.BinaryOp(
      ast.Literal(2),
      '*',
      ast.Literal(3)
    )
  )
