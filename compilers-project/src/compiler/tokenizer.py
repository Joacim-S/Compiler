import re
from compiler.location import Location
from compiler.token import Token

def tokenize(source_code: str) -> list[Token]:
  re_identifier = re.compile(r'[a-zA-Z_][0-9a-zA-Z_]*')
  re_int_lit = re.compile(r'[0-9]+')
  re_whitespace = re.compile(r'[ \n]+')
  re_operator = re.compile(r'\+|-|\*|/|=|<|>|==|!=|<=|>=')
  re_punctuation = re.compile(r'\(|\)|\{|\}|,|;')
  re_comment = re.compile(r'(//|#).*|/\*(\n|.)*?\*/')
  

  i = 0
  tokens: list[Token] = []
  line = 1
  col = 1
  
  def checkMatch(type: str) -> None:
    nonlocal i
    nonlocal tokens
    nonlocal line
    nonlocal col

    if not match:
      return

    i = match.end()
    
    match_lines = 0
    match_cols = 0
    
    for char in match.group():
      if char == '\n':
        match_lines += 1
        match_cols = 0
        col = 1
      else:
        match_cols += 1

    if type == 'whitespace' or type == 'comment':
      line += match_lines
      col += match_cols
      return

    tokens.append(Token(match[0], type, Location('file', line, col)))
    line += match_lines
    col += match_cols
    return

  while i < len(source_code):
    
    match = re_comment.match(source_code, i)
    if match:
      checkMatch('comment')
      continue
    match = re_whitespace.match(source_code, i)
    if match:
      checkMatch('whitespace')
      continue
    match = re_int_lit.match(source_code, i)
    if match:
      checkMatch('int_literal')
      continue
    match = re_identifier.match(source_code, i)
    if match:
      checkMatch('identifier')
      continue
    match = re_operator.match(source_code, i)
    if match:
      checkMatch('operator')
      continue
    match = re_punctuation.match(source_code, i)
    if match:
      checkMatch('punctuation')
      continue

    raise Exception(f'Syntax Error, tokens:{tokens}')

  return tokens