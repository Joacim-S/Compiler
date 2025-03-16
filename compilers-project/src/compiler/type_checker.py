import compiler.ast as ast
from compiler.types import Int, Bool, Unit, Type
from compiler.symtab import SymTab

def typecheck(mod: ast.Module, typetab: SymTab) -> Type:
  def typecheck_node(node: ast.Expression, typetab: SymTab) -> Type:
    def get_type() -> Type:
      def get_from_tab(key: str, params: tuple) -> Type:
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
          t1 = typecheck_node(node.left, typetab)
          t2 = typecheck_node(node.right, typetab)
          tab = typetab
          
          if node.op == '=':
            if t1 != t2:
              raise Exception(f"{node.location}, expected matching types for '=', got {t1} and {t2}")
            return t2
          
          if node.op in ['==', '!=']:
            if t1 != t2:
              raise Exception(f"{node.location}, expected matching types for {node.op}, got {t1} and {t2}")
            return Bool
            
          return get_from_tab(node.op, (t1, t2))
        
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
          t1 = typecheck_node(node.val, typetab)
          if node.declared_type is not None and node.declared_type != t1:
            raise Exception(f"{node.location}, unmatched declared type and value type: {node.declared_type} != {t1}")
          if typetab.locals.get(node.name.name) != None:
            raise Exception(f"{node.location}, Variable already delcared in this scope '{node.name.name}'")
          typetab.locals[node.name.name] = t1
          return Unit
        
        case ast.Block():
          local_tab = SymTab['str']({}, typetab)
          for expr in node.content:
            typecheck_node(expr, local_tab)
          
          return typecheck_node(node.val, local_tab)
        
        case ast.Unary():
          t1 = typecheck_node(node.val, typetab)
          op = f'unary_{node.op}'
          return get_from_tab(op, (t1,))

        
        case ast.FunctionCall():
          param_types = tuple([typecheck_node(param, typetab) for param in node.params])
          return get_from_tab(node.name.name, param_types)
        
        case ast.Condition():
          t1 = typecheck_node(node.con, typetab)
          if t1 is not Bool:
            raise Exception(f"{node.location}, expected {Bool} got {t1}")
          
          t2 = typecheck_node(node.then, typetab)
          if node.el is None:
            return t2
          t3 = typecheck_node(node.el, typetab)
          if t2 != t3:
            raise Exception(f"{node.location}, expected matching types for both branches of if, got {t1} and {t2}")
          return t2
        
        case ast.Loop():
          t1 = typecheck_node(node.condition, typetab)
          if t1 is not Bool:
            raise Exception(f"{node.location}, expected {Bool} got {t1}")
          t2 = typecheck_node(node.do, typetab)
          return t2

        case _:
          raise NotImplemented

    t = get_type()
    node.type = t
    return t
  
  return typecheck_node(mod.body, typetab)
  