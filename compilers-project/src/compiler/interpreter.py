from typing import Any, Callable
from compiler import ast
from compiler.symtab import SymTab

type Value = int | bool | None | Callable

def interperet(node: ast.Expression, symtab: SymTab) -> Value:
  match node:
    case ast.Literal():
      return node.value
    
    case ast.BinaryOp():
      tab = symtab

      if node.op == '=':
        identifier: Any = node.left

        while identifier.name not in tab.locals.keys():
          if tab.parent:
            tab = tab.parent
          else:
            raise Exception(f'Cannot assign value to undeclared variable {identifier.name}')

        tab.locals[identifier.name] = interperet(node.right, symtab)
        return tab.locals[identifier.name]

      a: Any = interperet(node.left, symtab)
      if node.op == 'or' and a:
        return True

      if node.op == 'and' and not a:
        return False
      
      b: Any = interperet(node.right,symtab)
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
        if node.el is not None:
          return interperet(node.el,symtab)
        return None
      
    case ast.Declaration():
      symtab.locals[node.name.name] = interperet(node.val, symtab)
      return None

    case ast.Block():
      local_sym = SymTab['str']({}, symtab)
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
    
    case ast.Unary():
      tab = symtab
      a = interperet(node.val, symtab)
      while node.op not in tab.locals.keys():
        if tab.parent:
          tab = tab.parent
        else:
          raise NotImplemented
      return tab.locals[f'unary_{node.op}'](a)
    
    case ast.Loop():
      while interperet(node.condition, symtab):
        result = interperet(node.do, symtab)

      return result
      
      
    case _:
      raise NotImplemented