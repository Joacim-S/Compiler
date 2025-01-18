from compiler.tokenizer import tokenize, Token, Location

L = Location('L',-1, -1)

def test_tokenizer_basics() -> None:
  assert tokenize('aaa 123 bbb') == [
      Token(loc=L, type="identifier", text="aaa"),
      Token(loc=L, type="int_literal", text="123"),
      Token(loc=L, type="identifier", text="bbb"),
  ]

def test_additions_with_extra_spaces() -> None:
  assert tokenize('a + b-c   +   1234') == [
    Token(loc=L, type="identifier", text="a"),
    Token(loc=L, type="operator", text="+"),
    Token(loc=L, type="identifier", text="b"),
    Token(loc=L, type="operator", text="-"),
    Token(loc=L, type="identifier", text="c"),
    Token(loc=L, type="operator", text="+"),
    Token(loc=L, type="int_literal", text="1234"),
  ]