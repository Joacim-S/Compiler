from dataclasses import dataclass
from typing import Any

@dataclass
class SymTab:
  locals: dict
  parent: Any = None

TopTab = SymTab({
  '+': lambda a, b : a + b,
  '-': lambda a, b: a - b
})