#Manual tests: Print stuff that's supposed to look similar to reference outputs.
from compiler.ir_generator import generate_ir
from compiler.types import FunType, Int, Bool, Unit
from compiler.ir import IRVar
from compiler import ast
from compiler.location import L

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
}


result = generate_ir(root_types, (ast.Module([], ast.BinaryOp(
  L,
  ast.Literal(L, 1),
  '+',
  ast.BinaryOp(
    L,
    ast.Literal(L, 2),
    '*',
    ast.Literal(L, 3)
  )
))))

print('1+2*3')
for row in result:
  print(row)
print()
  
  
result = generate_ir(root_types, ast.Module([], ast.Literal(L, 5)))

print('5')
for row in result:
  print(row)
print()

result = generate_ir(root_types, ast.Module([], ast.Literal(L, True)))

print('true')
for row in result:
  print(row)
print()

result = generate_ir(root_types, ast.Module([], ast.Condition(
      L,
      ast.Literal(L, False),
      ast.Literal(L, 2),
      None
      )))

print('if false 2')
for row in result:
  print(row)
print()

result = generate_ir(root_types, ast.Module([], ast.Block(L,[
      ast.Declaration(L,
        ast.Identifier(L, 'a'),
        ast.Literal(L, 5)
      ),
      ast.BinaryOp(L,
      ast.Identifier(L, 'a'),
      '=',
      ast.Literal(L, 100),
    )
      ],
      ast.BinaryOp(L,
      ast.Identifier(L, 'a'),
      '*',
      ast.Literal(L, 10),
    )
    )))

print('var a = 5; a = 100; a * 10')
for row in result:
  print(row)
print()

result = generate_ir(
  root_types,
  ast.Module([],
  ast.Block(
    L,
    [
      ast.Declaration(
        L,
        ast.Identifier(L, 'evr'),
        ast.Literal(L, False)
      ),
      ast.BinaryOp(
        L,
        ast.Literal(L, True),
        'or',
        ast.Block(
          L,
          [
            ast.BinaryOp(
              L,
              ast.Identifier(L, 'evr'),
              '=',
              ast.Literal(L, True)
            )
          ],
          ast.Literal(L, True)
        )
      )
    ],
    ast.Identifier(L, 'evr')
  )
))

print('''var evr = false;
true or { evr = true; true };
evr''')
for row in result:
  print(row)
print()

result = generate_ir(
  root_types,
  ast.Module([],
  ast.Condition(
    L,
    ast.Literal(L, False),
    ast.Literal(L, 2),
    ast.Literal(L, 3)
    )
))
for row in result:
  print(row)
print()

result = generate_ir(root_types, ast.Module([], ast.Block(L,[
      ast.Declaration(L,
        ast.Identifier(L, 'a'),
        ast.Literal(L, False)
      )
    ], 
      ast.BinaryOp(L,
      ast.Literal(L, True),
      'or',
      ast.Identifier(L, 'a'),
      ))))

print('''var a = false;
true or a;''')
for row in result:
  print(row)
print()

result = generate_ir(root_types, ast.Module([], ast.Block(L,[
      ast.Declaration(L,
        ast.Identifier(L, 'a'),
        ast.Literal(L, False)
      )
    ], 
      ast.BinaryOp(L,
      ast.Literal(L, True),
      'and',
      ast.Identifier(L, 'a'),
      ))))

print('''var a = false;
true and a;''')
for row in result:
  print(row)
print()

result = generate_ir(root_types, ast.Module([], ast.Block(L,[
      ast.Declaration(L,
        ast.Identifier(L, 'a'),
        ast.Literal(L, False)
      )
    ], 
      ast.BinaryOp(L,
      ast.Literal(L, True),
      '==',
      ast.Identifier(L, 'a'),
      ))))

print('''var a = false;
true == a;''')
for row in result:
  print(row)
print()

result = generate_ir(
  root_types,
  ast.Module([],
  ast.FunctionCall(
    L,
    ast.Identifier(L, 'print_int'),
    [ast.BinaryOp(
      L,
      ast.Literal(L, 2),
      '+',
      ast.Literal(L, 3)
    )]
  ))
)

print('''print_int(2+3)''')
for row in result:
  print(row)
print()

result = generate_ir(
  root_types,
  ast.Module([],
  ast.Unary(L, 'not', ast.Literal(L, True))
))

print('''not true''')
for row in result:
  print(row)
print()

result = generate_ir(
  root_types,
  ast.Module([],
  ast.Unary(L, '-', ast.Literal(L, 5))
))

print('''-5''')
for row in result:
  print(row)
print()

result = generate_ir(
  root_types,
  ast.Module([],
  ast.Loop(
    L,
    ast.BinaryOp(
      L,
      ast.Literal(L, 1),
      '<',
      ast.Literal(L, 0)
    ),
    ast.Literal(L, 1)
  ))
)

print('''while 1 < 0 do 1''')
for row in result:
  print(row)
print()

