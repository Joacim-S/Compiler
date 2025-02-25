from dataclasses import dataclass

@dataclass
class Location:
  file: str
  line: int
  column: int
  def __eq__(self, other: object) -> bool:
    if not isinstance(other, Location):
      return NotImplemented
    return self.file == 'L' and self.line == -1 and self.column == -1 or (
    other.file == 'L' and other.line == -1 and other.column == -1) or (
      self.file == other.file and self.line == other.line and self.column == other.column
    )

L = Location('L',-1, -1)
