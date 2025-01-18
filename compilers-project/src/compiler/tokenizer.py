import re
from dataclasses import dataclass

@dataclass
class Location:
  file: str
  line: int
  column: int
  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Location):
      return NotImplemented
    return self.file == 'L' or other.file == 'L'

@dataclass
class Token:
  text: str
  type: str
  loc: Location

def checkMatch(match: re.Match | None, type: str, tokens: list[Token], i: int, error: bool) -> tuple[list, int, bool]:
  if not match:
    return (tokens, i, error)
  i = match.end()
  error = False
  if type == 'whitespace' or type == 'comment':
    return (tokens, i, error)
  tokens.append(Token(match[0], type, Location('0', 0, 0)))
  return (tokens, i, error)

def tokenize(source_code: str) -> list[Token]:
  re_identifier = re.compile(r'[a-zA-Z_][0-9a-zA-Z_]*')
  re_int_lit = re.compile(r'[0-9]+')
  re_whitespace = re.compile(r'[ \n]+')
  re_operator = re.compile(r'\+|-|\*|/|=|<|>|==|!=|<=|>=')
  re_punctuation = re.compile(r'\(|\)|\{|\}|,|;')
  re_comment = re.compile(r'(//|#).*|/\*(\n|.)*?\*/')
  
  i = 0
  tokens: list[Token] = []

  while i < len(source_code):
    error = True
    
    match = re_comment.match(source_code, i)
    tokens, i, error = checkMatch(match, 'comment', tokens, i, error)
    match = re_whitespace.match(source_code, i)
    tokens, i, error = checkMatch(match, 'whitespace', tokens, i, error)
    match = re_int_lit.match(source_code, i)
    tokens, i, error = checkMatch(match, 'int_literal', tokens, i, error)
    match = re_identifier.match(source_code, i)
    tokens, i, error = checkMatch(match, 'identifier', tokens, i, error)
    match = re_operator.match(source_code, i)
    tokens, i, error = checkMatch(match, 'operator', tokens, i, error)
    match = re_punctuation.match(source_code, i)
    tokens, i, error = checkMatch(match, 'punctuation', tokens, i, error)
    if error:
      raise Exception(f'Syntax Error, tokens:{tokens}')

  return tokens
