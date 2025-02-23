from dataclasses import dataclass
from compiler.symtab import SymTab

@dataclass
class Type:
  type: type | None
  
@dataclass
class FunType:
  params: tuple
  rtype: Type
  
    
Int = Type(int)
Bool = Type(bool)
Unit = Type(None)

TypeTab = SymTab({
  '+': FunType((Int, Int), Int),
  '-': FunType((Int, Int), Int),
  '*': FunType((Int, Int), Int),
  '/': FunType((Int, Int), Int),
  '%': FunType((Int, Int), Int),
  '>': FunType((Int, Int), Bool),
  '>=': FunType((Int, Int), Bool),
  '<': FunType((Int, Int), Bool),
  '<=': FunType((Int, Int), Bool),
  'or': FunType((Bool, Bool), Bool),
  'and': FunType((Bool, Bool), Bool),
})