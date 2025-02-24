import compiler.ast as ast
from compiler.types import Int, Bool, Unit, Type
from compiler.symtab import SymTab

def typecheck(node: ast.Expression, typetab: SymTab) -> Type:
  def get_type(key: str, params: tuple) -> Type:
    tab = typetab
    while key not in tab.locals.keys():
      if tab.parent:
        tab = tab.parent
      else:
        raise Exception(f"{node.location}: '{key}' is not defined")
    f = tab.locals[key]
    
    if params != f.params:
      raise Exception(f"{node.location}: Unsupported parameters for '{key}' Expected: {f.params} got: {params}")
    
    return f.rtype
  
  match node:
    case ast.BinaryOp():
      t1 = typecheck(node.left, typetab)
      t2 = typecheck(node.right, typetab)
      tab = typetab
      
      if node.op == '=':
        if t1 != t2:
          raise Exception(f"{node.location}, expected matching types for '=', got {t1} and {t2}")
        return t2
      
      if node.op in ['==, !=']:
        if t1 != t2:
          raise Exception(f"{node.location}, expected matching types for {node.op}, got {t1} and {t2}")
        return Bool
        
      return get_type(node.op, (t1, t2))
    
    case ast.Literal():
      if isinstance(node.value, bool):
        return Bool
      if node.value is None:
        return Unit
      if isinstance(node.value, int):
        return Int
      
    case ast.Identifier():
      tab = typetab
      while node.name  not in tab.locals.keys():
        if tab.parent:
          tab = tab.parent
        else:
          raise Exception
      return tab.locals[node.name]
    
    case ast.Declaration():
      typetab.locals[node.name.name] = typecheck(node.val, typetab)
      return typetab.locals[node.name.name]
    
    case ast.Block():
      local_tab = SymTab({}, typetab)
      for expr in node.content:
        typecheck(expr, local_tab)
      
      return typecheck(node.val, local_tab)
    
    case ast.Unary():
      t1 = typecheck(node.val, typetab)
      op = f'unary_{node.op}'
      return get_type(op, (t1,))

    
    case ast.FunctionCall():
      param_types = tuple([typecheck(param, typetab) for param in node.params])
      return get_type(node.name.name, param_types)

    case _:
      raise NotImplemented

