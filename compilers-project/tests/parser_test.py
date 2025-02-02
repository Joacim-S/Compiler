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
  
def test_garbage_at_end_throws_error() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='1'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='identifier', text='a'),
  ]
  try:
    parse(tokens)
  except Exception as exc:
    assert exc.args[0] == "Unexpected token a at Location(file='L', line=-1, column=-1)"
    
def test_paranthesis() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='int_literal', text='1'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='punctuation', text=')'),
    Token(loc=L, type='int_literal', text='*'),
    Token(loc=L, type='int_literal', text='3'),
  ]
  assert parse(tokens) == ast.BinaryOp(
    left = ast.BinaryOp(
      ast.Literal(1),
      '+',
      ast.Literal(2)
    ),
    op = '*',
    right = ast.Literal(3)
    )

def test_if() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='b'),
  ]
  assert parse(tokens) == ast.Condition(
    ast.Identifier('a'),
    ast.Identifier('b'),
    None
  )

  
def test_nested_if() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='x'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='identifier', text='else'),
    Token(loc=L, type='identifier', text='c'),
    Token(loc=L, type='identifier', text='else'),
    Token(loc=L, type='identifier', text='d'),
  ]
  assert parse(tokens) == ast.Condition(
    ast.Identifier('a'),
    ast.Condition(
      ast.Identifier('x'),
      ast.Identifier('b'),
      ast.Identifier('c')
    ),
    ast.Identifier('d')
  )

def test_if_as_part_of_expression() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='1'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='True'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='identifier', text='else'),
    Token(loc=L, type='int_literal', text='3'),
  ]
  
  assert parse(tokens) == ast.BinaryOp(
    left = ast.Literal(1),
    op = '+',
    right = ast.Condition(
      ast.Identifier('True'),
      ast.Literal(2),
      ast.Literal(3)
    ),
  )