from typing import Any
from compiler import ast
from compiler.symtab import SymTab

type Value = int | bool | None

def interperet(node: ast.Expression, symtab: SymTab) -> Value:
  match node:
    case ast.Literal():
      return node.value
    
    case ast.BinaryOp():
      a: Any = interperet(node.left, symtab)
      b: Any = interperet(node.right,symtab)
      tab = symtab
      while node.op not in tab.locals.keys():
        if tab.parent:
          tab = tab.parent
        else:
          raise NotImplemented
      return tab.locals[node.op](a, b)
      
    case ast.Condition():
      if interperet(node.con, symtab):
        return interperet(node.then, symtab)
      else:
        return interperet(node.el,symtab)
      
    case ast.Declaration():
      symtab.locals[node.name.name] = interperet(node.val, symtab)
      return None

    case ast.Block():
      local_sym = SymTab({}, symtab)
      for expr in node.content:
        interperet(expr, local_sym)
      return interperet(node.val, local_sym)
        
    case ast.Identifier():
      tab = symtab
      while node.name not in tab.locals.keys():
        if tab.parent:
          tab = tab.parent
        else:
          raise Exception(f'{node.location}: {node.name} not defined')
      return symtab.locals[node.name]

    case _:
      raise NotImplemented