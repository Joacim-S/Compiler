from dataclasses import dataclass, field
from typing import Any, Type
from compiler.ir import IRVar

@dataclass
class SymTab[T]:
  locals: dict[Any, T] = field(default_factory=dict)
  parent: Any = None
  
  def require(self, name: str) -> T:
    for key in self.locals.keys():
      if str(key) == name:
        return self.locals[key]
    if self.parent:
      return self.parent.require(name)
    raise Exception
  
  def add_local(self, key: Any, v: T) -> None:
    self.locals[key] = v

TopTab = SymTab({
  '+': lambda a, b: a + b,
  '-': lambda a, b: a - b,
  '*': lambda a, b: a * b,
  '/': lambda a, b: a / b,
  '%': lambda a, b: a % b,
  '==': lambda a, b: a == b,
  '!=': lambda a, b: a != b,
  '>': lambda a, b: a > b,
  '>=': lambda a, b: a >= b,
  '<': lambda a, b: a < b,
  '<=': lambda a, b: a <= b,
  'or': lambda a, b: a or b,
  'and': lambda a, b: a and b,
  'unary_-': lambda a: -a,
  'unary_not': lambda a: not a,
})