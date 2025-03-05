from compiler.ir import IRVar
from compiler.types import Int, Bool, Unit

root_types = {
  IRVar('+'): Int,
  IRVar('-'): Int,
  IRVar('*'): Int,
  IRVar('/'): Int,
  IRVar('%'): Int,
  IRVar('>'): Bool,
  IRVar('>='): Bool,
  IRVar('<'): Bool,
  IRVar('<='): Bool,
  IRVar('=='): Bool,
  IRVar('!='): Bool,
  IRVar('or'): Bool,
  IRVar('and'): Bool,
  IRVar('unary_-'): Int,
  IRVar('unary_not'): Bool,
  IRVar('print_int'): Unit,
  IRVar('print_bool'): Unit,
  IRVar('read_int'): Int
}