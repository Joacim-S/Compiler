import compiler.ast as ast
from compiler.types import Int, Bool, Unit, Type
from compiler.symtab import SymTab

def typecheck(node: ast.Expression, typetab: SymTab) -> Type:
  match node:
    case ast.BinaryOp():
      t1 = typecheck(node.left, typetab)
      t2 = typecheck(node.right, typetab)
      
      tab = typetab
      while node.op not in typetab.locals.keys():
        if tab.parent:
          tab = tab.parent
        else:
          raise Exception

      if typetab.locals[node.op].params != (t1, t2):
        raise Exception
      
      return typetab.locals[node.op].rtype
    
    case ast.Literal():
      if isinstance(node.value, int):
        return Int
      if isinstance(node.value, bool):
        return Bool
      if node.value is None:
        return Unit
      
    case ast.Identifier():
      while node.name  not in typetab.locals.keys():
        if tab.parent:
          tab = tab.parent
        else:
          raise Exception
      return typetab.locals[node.name]
    
    case ast.Declaration():
      typetab.locals[node.name.name] = typecheck(node.val, typetab)
      return Unit
    
    case _:
      raise NotImplemented