from compiler.tokenizer import tokenize, Token, Location

L = Location('TheLocationObjectThatIsEqualToAllLocations',-1, -1)

def test_tokenizer_basics() -> None:
  assert tokenize('aaa 123 bbb') == [
      Token(loc=L, type="identifier", text="aaa"),
      Token(loc=L, type="int_literal", text="123"),
      Token(loc=L, type="identifier", text="bbb"),
  ]