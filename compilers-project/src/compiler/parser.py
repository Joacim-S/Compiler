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
      raise Exception(f'{token.loc}: expected "{expected}" got "{token.text}"')
    if isinstance(expected, list) and token.text not in expected:
      comma_separated = ", ".join([f'"{e}"' for e in expected])
      raise Exception(f'{token.loc}: expected one of: {comma_separated} got "{token.text}"')
    pos += 1
    return token

  def parse_factor() -> ast.Expression:
    types = {
      'int_literal': lambda a : ast.Literal(int(a)),
      'identifier': ast.Identifier
    }
    if peek().text == '(':
      return parse_parenthesized()
    
    if peek().text == 'if':
      return parse_condition()

    if peek().type == 'int_literal':
      token = consume()
      return ast.Literal(int(token.text))
    
    if peek().type == 'identifier':
      token = consume()
      if peek().text == '(':
        return parse_function_call(ast.Identifier(token.text))
      
      return ast.Identifier(token.text)
        
      
    raise Exception(f'{peek().loc}: expected type to be in {types.keys()}, "(", got {peek().type}')

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
    return left
  
  def parse_parenthesized() -> ast.Expression:
    consume('(')
    expr = parse_expression()
    consume(')')
    return expr
  
  def parse_condition() -> ast.Expression:
    consume('if')
    con = parse_expression()
    consume('then')
    then = parse_expression()
    el = None
    if peek().text == 'else':
      consume()
      el = parse_expression()
    return ast.Condition(
      con,
      then,
      el
    )
    
  def parse_function_call(name: ast.Expression) -> ast.Expression:
    consume('(')
    params: list[ast.Expression] = []

    if peek().text != ')':
      params.append(parse_expression())
      while peek().text == ',':
        consume(',')
        params.append(parse_expression())

    consume(')')
    return ast.Function(name, params)
  
  parsed = parse_expression()
  if peek().type != 'end':
    raise Exception(f"Unexpected token '{peek().text}' at {peek().loc}")
  
  return parsed