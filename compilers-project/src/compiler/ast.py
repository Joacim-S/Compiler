from dataclasses import dataclass, field
from compiler.tokenizer import Location
from compiler.types import Unit, Type

@dataclass
class Expression:
  '''Base class for AST nodes'''
  location: Location
  type: Type = field(kw_only=True, default=Unit)
  
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
  el: Expression | None
  
@dataclass
class FunctionCall(Expression):
  name: Identifier
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
  
@dataclass
class Loop(Expression):
  condition: Expression
  do: Expression