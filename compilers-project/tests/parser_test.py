from compiler.parser import parse
from compiler.tokenizer import Token, Location
import compiler.ast as ast

L = Location('TheLocationObjectThatIsEqualToAllLocations',-1, -1)

def test_parse_short() -> None:
  tokens = [
    Token(loc=L, type='int_literal', text='1'),
    Token(loc=L, type='operator', text='+'),
    Token(loc=L, type='int_literal', text='2')
  ]
  assert parse(tokens) == [
    ast.Binaryop(
      ast.Literal(1),
      '+',
      ast.Literal(2)
    )
  ]
