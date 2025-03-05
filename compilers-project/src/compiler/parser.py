from compiler.location import Location
from compiler.token import Token
import compiler.ast as ast
from compiler.types import Int, Unit, Bool, Type


def parse(tokens: list[Token]) -> ast.Expression:
  pos = 0
  
  precedence = [
    ['='],
    ['or'],
    ['and'],
    ['==', '!='],
    ['<', '<=', '>', '>='],
    ['+', '-'],
    ['*', '/', '%'],
    ['not'],
  ]
  
  right_associative_operators = [
    '='
  ]

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
    
  def peek_back() -> Token:
    if pos == 0:
      return Token(
      loc = tokens[-1].loc,
      type = 'punctuation',
      text = ';'
      )
    return tokens[pos-1]

  def consume(expected: str | list[str] | None = None) -> Token:
    nonlocal pos
    token = peek()
    if isinstance(expected, str) and token.text != expected:
      raise Exception(f"{token.loc}: expected '{expected}' got '{token.text}'")
    if isinstance(expected, list) and token.text not in expected:
      comma_separated = ", ".join([f"'{e}'" for e in expected])
      raise Exception(f"{token.loc}: expected one of: {comma_separated} got '{token.text}'")
    pos += 1
    return token

  def parse_factor() -> ast.Expression:
    types = [
      'int_literal',
      'identifier',
      'operator',
    ]
    if peek().text == '(':
      return parse_parenthesized()
    
    if peek().text == '{':
      return parse_block()
    
    if peek().text == 'if':
      return parse_condition()

    if peek().type == 'int_literal':
      token = consume()
      return ast.Literal(token.loc, int(token.text))
    
    if peek().text in ['-', 'not']:
      token = consume()
      op = token.text
      expr = parse_expression(7)
      return ast.Unary(token.loc, op, expr)
    
    if peek().text == 'true':
      token = consume('true')
      return ast.Literal(token.loc, True)
    
    if peek().text == 'false':
      token = consume('false')
      return ast.Literal(token.loc, False)
    
    if peek().text == 'var':
      if peek_back().text not in [';', '{','}',]:
        raise Exception(
            f'''{peek().loc}: 
            Cannot declare here. 
            Declarations are possible directly in blocks and in top-level expressions
            '''
          )
      
      return parse_declaration()
    
    if peek().text == 'while':
      return parse_loop()
      
    if peek().type == 'identifier':
      token = consume()
      if peek().text == '(':
        return parse_function_call(token.loc, ast.Identifier(token.loc, token.text))
      
      return ast.Identifier(token.loc, token.text)
      
    raise Exception(f'{peek().loc}: expected type to be in {types}, "(", got {peek().type}')

  def parse_expression(level: int = 0) -> ast.Expression:
    if level == len(precedence)-1:
      left = parse_factor()
    else:
      left = parse_expression(level+1)
    while get_precedence(peek().text) == level:
      operator_token = consume()
      operator = operator_token.text

      if operator in right_associative_operators:
        right = parse_expression()
      else:
        right = parse_expression(level+1)

      left = ast.BinaryOp(
        operator_token.loc,
        left,
        operator,
        right
      )

    return left
  
  def parse_loop() -> ast.Expression:
    start_token = consume('while')
    condition = parse_expression()
    consume('do')
    do = parse_expression()
    return ast.Loop(start_token.loc, condition, do)
  
  def parse_declaration() -> ast.Expression:
    types = {
      'Int': Int,
      'Bool': Bool,
      'Unit': Unit,
    }
    
    declared_type: Type | None = None
    consume('var')
    name_token = consume()
    if peek().text == ':':
      consume(':')
      type_token = consume()
      declared_type = types[type_token.text]
      
    op_token = consume('=')
    val = parse_expression()
    return ast.Declaration(
      op_token.loc,
      name = ast.Identifier(name_token.loc, name_token.text),
      val = val,
      declared_type = declared_type
      )
  
  def parse_block() -> ast.Expression:
    nonlocal pos
    start_token = consume('{')
    content = []
    val: ast.Expression = ast.Literal(start_token.loc, None)

    while peek().text != '}':
      expr = parse_expression()
      content.append(expr)

      if peek().text == '}':
        consume('}')
        val = content.pop()
        return ast.Block(start_token.loc, content, val)
      
      elif peek().text == ';':
        end = consume(';')
        val = ast.Literal(end.loc, None)
        
      elif peek_back().text not in ['}', ';']:
        consume([';', '}'])

    consume('}')
    if peek().text == ';':
      consume(';')
    
    return ast.Block(start_token.loc, content, val)
  
  def parse_parenthesized() -> ast.Expression:
    consume('(')
    expr = parse_expression()
    consume(')')
    return expr
  
  def parse_condition() -> ast.Expression:
    start_token = consume('if')
    con = parse_expression()
    consume('then')
    then = parse_expression()
    if peek().text == 'else':
      consume()
      el = parse_expression()
    else:
      el = None
    return ast.Condition(
      start_token.loc,
      con,
      then,
      el
    )

  def parse_function_call(loc: Location, name: ast.Identifier) -> ast.Expression:
    consume('(')
    params: list[ast.Expression] = []

    if peek().text != ')':
      params.append(parse_expression())
      while peek().text == ',':
        consume(',')
        params.append(parse_expression())

    consume(')')
    return ast.FunctionCall(loc, name, params)
  
  def get_precedence(text: str) -> int:
    for i in range(len(precedence)):
      if text in precedence[i]:
        return i

    return len(precedence)
  
  parsed = parse_expression()
  content = [parsed]
  val: ast.Expression | ast.Literal = ast.Literal(Location('f',-1,-1), None)

  if peek().type != 'end':
    if peek().text == ';':
      consume(';')
    while peek().type != 'end':
      if val != ast.Literal(Location('f',-1,-1), None):
        content.append(val)
        val = ast.Literal(Location('f',-1,-1), None)
      if peek_back().text in [';', '}']:
        if peek().text == ';':
          if peek_back().text == ';':
            raise Exception(f"Unexpected token '{peek().text}' at {peek().loc}")
          consume(';')
        if peek().type != 'end':
          expr = parse_expression()
          if peek().text == ';':
            content.append(expr)
            consume(';')
          else:
            val = expr
      else:
        raise Exception(f"Unexpected token '{peek().text}' at {peek().loc}")

    '''
    while peek().text == ';':
      consume(';')
      if peek().type != 'end':
        expr = parse_expression()
        if peek().type != 'end':
          content.append(expr)
        else:
          val = expr

    if peek().type != 'end':
      if peek_back().text not in [';', '}']:
        raise Exception (f"Unexpected token '{peek().text}' at {peek().loc}")
      expr = parse_expression()
      val = expr
    '''
    parsed = ast.Block(parsed.location, content, val)
    
    if peek().type != 'end':
      raise Exception(f"Unexpected token '{peek().text}' at {peek().loc}")
    
  
  return parsed