from compiler.symtab import SymTab

TypeTab = SymTab({
  '+': lambda a, b: a + b,
  '-': lambda a, b: a - b,
  '*': lambda a, b: a * b,
  '/': lambda a, b: a / b,
  '%': lambda a, b: a % b,
  '==': lambda a, b: a == b,
  '!=': lambda a, b: a != b,
  '>': lambda a, b: a > b,
  '>=': lambda a, b: a >= b,
  '<': lambda a, b: a < b,
  '<=': lambda a, b: a <= b,
  'or': lambda a, b: a or b,
  'and': lambda a, b: a and b,
  'unary_-': lambda a: -a,
  'unary_not': lambda a: not a,
})