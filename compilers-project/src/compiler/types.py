from dataclasses import dataclass
from compiler.symtab import SymTab

@dataclass(frozen=True)
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
  'unary_-': FunType((Int,), Int),
  'unary_not': FunType((Bool,), Bool),
  'print_int': FunType((Int,), Unit),
  'print_bool': FunType((Bool,), Unit),
  'read_int': FunType(params=(), rtype=Int)
})