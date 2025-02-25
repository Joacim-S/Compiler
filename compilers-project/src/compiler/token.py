from dataclasses import dataclass
from compiler.location import Location

@dataclass
class Token:
  text: str
  type: str
  loc: Location