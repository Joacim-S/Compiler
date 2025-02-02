from dataclasses import dataclass

@dataclass
class Expression:
  '''Base class for AST nodes'''
  
@dataclass
class Literal(Expression):
  value: int | bool
  
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