from compiler.types import Unit, Type
from dataclasses import dataclass, field
from compiler.location import Location

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

  def __str__(self) -> str:
    rows = ['CONTENT:']
    for c in self.content:
      rows.append(str(c))
    rows.append('VAL:')
    rows.append(str(self.val))
    return '\n'.join(rows)
  
@dataclass
class Declaration(Expression):
  name: Identifier
  val: Expression
  declared_type: Type | None = None
  
@dataclass
class Loop(Expression):
  condition: Expression
  do: Expression

