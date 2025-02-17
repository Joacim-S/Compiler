from compiler.parser import parse
from compiler.tokenizer import Token, Location
import compiler.ast as ast

L = Location('L',-1, -1)

def test_single_character() -> None:
  assert parse([Token(loc=L, type='identifier', text='a')]) == ast.Identifier('a')

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
  
  tokens = [
    Token(loc=L, type='int_literal', text='1'),
    Token(loc=L, type='operator', text='*'),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='int_literal', text='+'),
    Token(loc=L, type='int_literal', text='3'),
  ]
  assert parse(tokens) == ast.BinaryOp(
    right = ast.Literal(3),
    op = '+',
    left = ast.BinaryOp(
      ast.Literal(1),
      '*',
      ast.Literal(2)
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
    assert exc.args[0] == "Unexpected token 'a' at Location(file='L', line=-1, column=-1)"
    
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
  
def test_function_call_no_params() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='f'),
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='punctuation', text=')'),
  ]
  assert parse(tokens) == ast.Function(
    ast.Identifier('f'), [])
  
def test_function_call_single_params() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='f'),
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='punctuation', text=','),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text=')'),
  ]
  assert parse(tokens) == ast.Function(
    ast.Identifier('f'), [
      ast.Literal(2),
      ast.Identifier('a'),
    ])

def test_unary() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='not'),
    Token(loc=L, type='identifier', text='a'),
  ]
  assert parse(tokens) == ast.Unary(
    'not',
    ast.Identifier('a')
  )
  
def test_unary_chain() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='not'),
    Token(loc=L, type='identifier', text='not'),
    Token(loc=L, type='identifier', text='not'),
    Token(loc=L, type='operator', text='-'),
    Token(loc=L, type='identifier', text='a'),
  ]
  assert parse(tokens) == ast.Unary(
    'not',
    ast.Unary(
      'not',
      ast.Unary(
        'not',
        ast.Unary(
          '-',
          ast.Identifier('a')
        )
      )
    )
  )
  
  
def test_comparison() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='operator', text='=='),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='b')
  ]
  
  assert parse(tokens) == ast.Condition(
    ast.BinaryOp(
      ast.Literal(2),
      '==',
      ast.Identifier('a')
    ),
    ast.Identifier('b')
  )
  
def test_assignment() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='b'),
  ]
  
  assert parse(tokens) == ast.BinaryOp(
    ast.Identifier('a'),
    '=',
    ast.Identifier('b')
  )
  
  tokens = [
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='c'),
  ]
  
  assert parse(tokens) == ast.BinaryOp(
    ast.Identifier('a'),
    '=',
    ast.BinaryOp(
      ast.Identifier('b'),
      '=',
      ast.Identifier('c')
    )
  )

def test_ors_ands() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='operator', text='or'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='operator', text='or'),
    Token(loc=L, type='identifier', text='c'),
  ]
  
  assert parse(tokens) == ast.BinaryOp(
    ast.BinaryOp(
      ast.Identifier('a'),
      'or',
      ast.Identifier('b')
    ),
    'or',
    ast.Identifier('c')
  )
