from dataclasses import dataclass
from compiler.tokenizer import Location

@dataclass
class Expression:
  '''Base class for AST nodes'''
  location: Location
  
@dataclass
class Literal(Expression):
  value: int | bool | None

@dataclass
class Identifier(Expression):
  name: str
  
@dataclass
class BinaryOp(Expression):
  left: Expression
  op: str
  right: Expression

@dataclass
class Condition(Expression):
  con: Expression
  then: Expression
  el: Expression | None = None
  
@dataclass
class FunctionCall(Expression):
  name: Expression
  params: list[Expression]
  
@dataclass
class Unary(Expression):
  op: str
  val: Expression
  
@dataclass
class Block(Expression):
  content: list[Expression]
  val: Expression
  
@dataclass
class Declaration(Expression):
  name: Identifier
  val: Expression