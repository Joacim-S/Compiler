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
      loc = tokens[-1].loc,
      type = 'end',
      text = ''
    )

  def consume(expected: str | list[str] | None = None) -> Token:
    nonlocal pos
    token = peek()
    if isinstance(expected, str) and token.text != expected:
      raise Exception(f'{token.loc}: expected "{expected}"')
    if isinstance(expected, list) and token.text not in expected:
      comma_separated = ", ".join([f'"{e}"' for e in expected])
      raise Exception(f'{token.loc}: expected one of: {comma_separated}')
    pos += 1
    return token

  def parse_factor() -> ast.Expression:
    types = {
      'int_literal': lambda a : ast.Literal(int(a)),
      'identifier': ast.Identifier
    }

    if peek().type not in types:
      raise Exception(f'{peek().loc}: expected type to be in {types.keys()}, got {peek().type}')
    token = consume()
    return types[token.type](token.text)

  def parse_term() -> ast.Expression:
    left = parse_factor()
    while peek().text in ['*', '/']:
      operator_token = consume()
      operator = operator_token.text

      right = parse_factor()

      left = ast.BinaryOp(
        left,
        operator,
        right
      )
    
    return left

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
#TODO: Don't allow garbage in the end
    return left
  
  return parse_expression()
