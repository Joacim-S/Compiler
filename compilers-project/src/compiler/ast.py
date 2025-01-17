from dataclasses import dataclass

@dataclass
class Expression:
  '''Base class for AST nodes'''
  
@dataclass
class Literal(Expression):
  value: int | bool
  
@dataclass
class identifier(Expression):
  name: str
  
@dataclass
class BinaryOp(Expression):
  left: Expression
  op: str
  rigt: Expression
