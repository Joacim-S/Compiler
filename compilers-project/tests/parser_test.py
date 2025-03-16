from compiler.parser import parse
from compiler.location import L, Location
from compiler.token import Token
import compiler.ast as ast
from compiler.types import Int, Unit, Bool, Type


def test_single_character() -> None:
  assert parse([Token(loc=L, type='identifier', text='a')]) == ast.Module([], ast.Identifier(L, 'a'))

def test_one_plus_two_works() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='1'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='2')
  ]
  assert parse(tokens) == ast.Module([], ast.BinaryOp(
    L,
      ast.Literal(L, 1),
      '+',
      ast.Literal(L, 2)
    ))

def test_a_plus_two_works() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='2')
  ]
  assert parse(tokens) == ast.Module([], ast.BinaryOp(L,
      ast.Identifier(L, 'a'),
      '+',
      ast.Literal(L, 2)
    ))
  
def test_addition_multiplication_presedence() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='1'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='int_literal', text='*'),
    Token(loc=L, type='int_literal', text='3'),
  ]
  assert parse(tokens) == ast.Module([], ast.BinaryOp(L,
    left = ast.Literal(L, 1),
    op = '+',
    right = ast.BinaryOp(L,
      ast.Literal(L,2),
      '*',
      ast.Literal(L,3)
    )
  ))
  
  tokens = [
    Token(loc=L, type='int_literal', text='1'),
    Token(loc=L, type='operator', text='*'),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='int_literal', text='+'),
    Token(loc=L, type='int_literal', text='3'),
  ]
  assert parse(tokens) == ast.Module([], ast.BinaryOp(L,
    right = ast.Literal(L,3),
    op = '+',
    left = ast.BinaryOp(L,
      ast.Literal(L,1),
      '*',
      ast.Literal(L,2)
    )
  ))
  
def test_garbage_at_end_throws_error() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='1'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='identifier', text='a'),
  ]
  try:
    parse(tokens)
    assert False == True
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
  assert parse(tokens) == ast.Module([], ast.BinaryOp(L,
    left = ast.BinaryOp(L,
      ast.Literal(L,1),
      '+',
      ast.Literal(L,2)
    ),
    op = '*',
    right = ast.Literal(L,3)
    ))

def test_if() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='b'),
  ]
  assert parse(tokens) == ast.Module([], ast.Condition(L,
    ast.Identifier(L,'a'),
    ast.Identifier(L,'b'),
    None
  ))

  
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
  assert parse(tokens) == ast.Module([], ast.Condition(L,
    ast.Identifier(L,'a'),
    ast.Condition(L,
      ast.Identifier(L,'x'),
      ast.Identifier(L,'b'),
      ast.Identifier(L,'c')
    ),
    ast.Identifier(L,'d')
  ))

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
  
  assert parse(tokens) == ast.Module([], ast.BinaryOp(L,
    left = ast.Literal(L,1),
    op = '+',
    right = ast.Condition(L,
      ast.Identifier(L,'True'),
      ast.Literal(L,2),
      ast.Literal(L,3)
    ),
  ))
  
def test_function_call_no_params() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='f'),
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='punctuation', text=')'),
  ]
  assert parse(tokens) == ast.Module([], ast.FunctionCall(L,
    ast.Identifier(L,'f'), []))
  
def test_function_call_single_params() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='f'),
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='punctuation', text=','),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text=')'),
  ]
  assert parse(tokens) == ast.Module([], ast.FunctionCall(L,
    ast.Identifier(L,'f'), [
      ast.Literal(L,2),
      ast.Identifier(L,'a'),
    ]))

def test_unary() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='not'),
    Token(loc=L, type='identifier', text='a'),
  ]
  assert parse(tokens) == ast.Module([], ast.Unary(L,
    'not',
    ast.Identifier(L,'a')
  ))
  
def test_unary_chain() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='not'),
    Token(loc=L, type='identifier', text='not'),
    Token(loc=L, type='identifier', text='not'),
    Token(loc=L, type='operator', text='-'),
    Token(loc=L, type='identifier', text='a'),
  ]
  assert parse(tokens) == ast.Module([], ast.Unary(L,
    'not',
    ast.Unary(L,
      'not',
      ast.Unary(L,
        'not',
        ast.Unary(L,
          '-',
          ast.Identifier(L,'a')
        )
      )
    )
  ))
  
  
def test_comparison() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='operator', text='=='),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='identifier', text='b')
  ]
  
  assert parse(tokens) == ast.Module([], ast.Condition(L,
    ast.BinaryOp(L,
      ast.Literal(L,2),
      '==',
      ast.Identifier(L,'a')
    ),
    ast.Identifier(L,'b'),
    None
  ))
  
def test_assignment() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='b'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.BinaryOp(L,
    ast.Identifier(L,'a'),
    '=',
    ast.Identifier(L,'b')
  ))
  
  tokens = [
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='c'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.BinaryOp(L,
    ast.Identifier(L,'a'),
    '=',
    ast.BinaryOp(L,
      ast.Identifier(L,'b'),
      '=',
      ast.Identifier(L,'c')
    )
  ))

def test_ors_ands() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='identifier', text='or'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='identifier', text='or'),
    Token(loc=L, type='identifier', text='c'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.BinaryOp(L,
    ast.BinaryOp(L,
      ast.Identifier(L,'a'),
      'or',
      ast.Identifier(L,'b')
    ),
    'or',
    ast.Identifier(L,'c')
  ))

def test_complicated_assignments() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='2'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='c'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='d'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='5'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.BinaryOp(L,
    ast.Identifier(L,'a'),
    '=',
    ast.BinaryOp(L,
      ast.BinaryOp(L,
        ast.Identifier(L,'b'),
        '+',
        ast.Literal(L,2)
      ),
      '=',
      ast.BinaryOp(L,
        ast.Identifier(L,'c'),
        '=',
        ast.BinaryOp(L,
          ast.Identifier(L,'d'),
          '+',
          ast.Literal(L,5)
        )
      )
    )
  ))

def test_blocks() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='{'),
    Token(loc=L, type='identifier', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='identifier', text='}'),
    Token(loc=L, type='identifier', text='{'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='identifier', text='}'),
    Token(loc=L, type='identifier', text='}'),
  ]

  assert parse(tokens) == ast.Module([], ast.Block(L,
    [
      ast.Block(L,[],
                ast.Identifier(L,'a')),
      ],
    ast.Block(L,[],
              ast.Identifier(L,'b'))))

  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text='}'),
  ]
  
  try:
    parse(tokens)
    assert False == True
  except Exception as exc:
    assert exc.args[0] == "Location(file='L', line=-1, column=-1): expected one of: ';', '}' got 'a'"
  
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='true'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='punctuation', text='}'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.Block(L,
    [
      ast.Condition(L,
        ast.Literal(L,True),
        ast.Block(L,
          [], ast.Identifier(L,'a')
        ),
        None
      ),
      ], ast.Identifier(L,'b')
  ))
  
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='true'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='punctuation', text=';'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='identifier', text='}'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.Block(L,
    [
      ast.Condition(L,
        ast.Literal(L,True),
        ast.Block(L,
          [], ast.Identifier(L,'a')
        ),
        None
      ),
      ], ast.Identifier(L,'b')
  ))
  
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='true'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='identifier', text='c'),
    Token(loc=L, type='punctuation', text='}'),
  ]
  
  try:
    parse(tokens)
    assert False == True
  except Exception as exc:
    assert exc.args[0] == "Location(file='L', line=-1, column=-1): expected one of: ';', '}' got 'c'"
    
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='if'),
    Token(loc=L, type='identifier', text='true'),
    Token(loc=L, type='identifier', text='then'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='identifier', text='else'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='identifier', text='c'),
    Token(loc=L, type='punctuation', text='}'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.Block(L,
    [
      ast.Condition(L,
        ast.Literal(L,True),
        ast.Block(L,
          [], ast.Identifier(L,'a')
        ), 
        ast.Block(L,
          [], ast.Identifier(L,'b')
        )
      ),
      ], ast.Identifier(L,'c')
  ))
  
def test_function_call_in_block() -> None:
  tokens = [
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='f'),
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text=')'),
    Token(loc=L, type='punctuation', text='}'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.Block(L,
    [],
    ast.FunctionCall(L,ast.Identifier(L,'f'), [ast.Identifier(L,'a')])
  ))
  
  tokens = [
    Token(loc=L, type='identifier', text='x'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='f'),
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text=')'),
    Token(loc=L, type='punctuation', text='}'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.BinaryOp(L,
    ast.Identifier(L,'x'),
    '=',
    ast.Block(L,
      [],
      ast.FunctionCall(L,ast.Identifier(L,'f'), [ast.Identifier(L,'a')])
    )
  ))


def test_blocks_with_function_calls() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='x'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='f'),
    Token(loc=L, type='punctuation', text='('),
    Token(loc=L, type='identifier', text='a'),
    Token(loc=L, type='punctuation', text=')'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='punctuation', text='{'),
    Token(loc=L, type='identifier', text='b'),
    Token(loc=L, type='punctuation', text='}'),
    Token(loc=L, type='punctuation', text='}'),
  ]

  assert parse(tokens) == ast.Module([], ast.BinaryOp(L,
    ast.Identifier(L,'x'),
    '=',
    ast.Block(L,
      content = [
        ast.Block(L,[],
                  val = ast.FunctionCall(L,ast.Identifier(L,'f'), [ast.Identifier(L,'a')])),
      ],
      val = ast.Block(L,[], ast.Identifier(L,'b'))
    )
  ))

def test_declaration() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='var'),
    Token(loc=L, type='identifier', text='x'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='int_literal', text='123'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.Declaration(L,
    ast.Identifier(L,'x'),
    ast.Literal(L,123)
  ))
  
def test_loop() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='while'),
    Token(loc=L, type='identifier', text='i'),
    Token(loc=L, type='operator', text='<'),
    Token(loc=L, type='int_literal', text='100'),
    Token(loc=L, type='identifier', text='do'),
    Token(loc=L, type='identifier', text='i'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='identifier', text='i'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='1'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.Loop(L,
    ast.BinaryOp(
      L,
      ast.Identifier(L, 'i'),
      '<',
      ast.Literal(L, 100)),
    ast.BinaryOp(
      L,
      ast.Identifier(L, 'i'),
      '=',
      ast.BinaryOp(
        L,
        ast.Identifier(L, 'i'),
        '+',
        ast.Literal(L, 1)))
  ))
  
def test_multiplse_expressions() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='var'),
    Token(loc=L, type='identifier', text='x'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='int_literal', text='123'),
    Token(loc=L, type='punctuation', text=';'),
    Token(loc=L, type='identifier', text='var'),
    Token(loc=L, type='identifier', text='y'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='int_literal', text='10'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.Block(
    L, [ast.Declaration(
      L,
      ast.Identifier(L,'x'),
      ast.Literal(L,123),
    ),

  ],   ast.Declaration(
    L,
    ast.Identifier(L,'y'),
    ast.Literal(L,10)
  )
  ))
  
def test_typed_decleration() -> None:
  tokens = [
    Token(loc=L, type='identifier', text='var'),
    Token(loc=L, type='identifier', text='x'),
    Token(loc=L, type='punctuation', text=':'),
    Token(loc=L, type='identifier', text='Int'),
    Token(loc=L, type='operator', text='='),
    Token(loc=L, type='int_literal', text='123'),
  ]
  
  assert parse(tokens) == ast.Module([], ast.Declaration(L,
    ast.Identifier(L,'x'),
    ast.Literal(L,123),
    Int
  ))
  
def test_no_block_multiple_expressions() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='15'),
    Token(loc=L, type='punctuation', text=';'),
    Token(loc=L, type='int_literal', text='15'),
  ]

  assert parse(tokens) == ast.Module([], ast.Block(
    L,
    [ast.Literal(L, 15)],
    ast.Literal(L, 15)
  ))