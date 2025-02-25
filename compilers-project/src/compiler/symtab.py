from dataclasses import dataclass, field
from typing import Any, Type

@dataclass
class SymTab[T]:
  locals: dict[T, Any] = field(default_factory=dict)
  parent: Any = None

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
}
)