from compiler.tokenizer import Token
import compiler.ast as ast

def parse(tokens: list[Token]) -> ast.Expression:
  pos = 0
  
  def peek() -> Token:
    if len(tokens) == 0:
      raise Exception('Tokens empty, nothing to parse')
    
    if pos < len(tokens):
      return tokens[pos]

    return Token(
      location = tokens[-1].location,
      type = 'end',
      text = ''
    )
    
  def consume(expected: str | lsit[str] | None = None) -> Token:
    token = peek()
    if isinstance(expected, str) and token.txt != expected:
      raise Exception(f'{token.location}: expected "{expected}"')
    if isinstance(expected, list) and token.text not in expected:
        comma_separated = ", ".join([f'"{e}"' for e in expected])
        raise Exception(f'{token.location}: expected one of: {comma_separated}')
    pos += 1
    return token
  
  def parse_term() -> ast.Literal:
    types = {
      'int_literal': ast.Literal,
      'identifier': ast.identifier
    }

    if peek().type not in types:
      raise Exception(f'{peek().location}: expected type to be in {types.keys()}, got {peek().type}')
    token = consume()
    return types[token.type](token.text)
  
  def parse_expression() -> ast.Expression:
    left = parse_term()
    
    while peek().text in ['+', '-']:
      operator_token = consume()
      operator = operator_token.text
      
      right = parse_term()
      
      left = ast.BinaryOp(
        left,
        operator,
        right
      )
      
    return left