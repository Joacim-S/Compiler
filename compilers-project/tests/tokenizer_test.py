from compiler.tokenizer import tokenize, Token, Location

L = Location('L',-1, -1)

def test_tokenizer_basics() -> None:
  assert tokenize('aaa 123 bbb') == [
      Token(loc=Location('file', 1, 1), type="identifier", text="aaa"),
      Token(loc=Location('file', 1, 5), type="int_literal", text="123"),
      Token(loc=Location('file', 1, 9), type="identifier", text="bbb"),
  ]

def test_additions_with_extra_spaces() -> None:
  assert tokenize('a + b-c   +   1234') == [
    Token(loc=Location('file', 1, 1), type="identifier", text="a"),
    Token(loc=Location('file', 1, 3), type="operator", text="+"),
    Token(loc=Location('file', 1, 5), type="identifier", text="b"),
    Token(loc=Location('file', 1, 6), type="operator", text="-"),
    Token(loc=Location('file', 1, 7), type="identifier", text="c"),
    Token(loc=Location('file', 1, 11), type="operator", text="+"),
    Token(loc=Location('file', 1, 15), type="int_literal", text="1234"),
  ]
  
def test_multiline() -> None:
  assert tokenize('''a*b
c     ag
#asdöflkj
/*
sadlkjf
adsfasdg
ghadsfagd asdf sdaf
*/
tadaa           
                  ''') == [
  Token(loc=Location('file', 1, 1), type="identifier", text="a"),
  Token(loc=Location('file', 1, 2), type="operator", text="*"),
  Token(loc=Location('file', 1, 3), type="identifier", text="b"),
  Token(loc=Location('file', 2, 1), type="identifier", text="c"),
  Token(loc=Location('file', 2, 7), type="identifier", text="ag"),
  Token(loc=Location('file', 9, 1), type="identifier", text="tadaa"),
  ]