from compiler.types import TypeTab
from compiler.root_types import root_types
from compiler.tokenizer import tokenize
from compiler.parser import parse
from compiler.type_checker import typecheck
from compiler.ir_generator import generate_ir
from compiler.assembly_generator import generate_assembly
from compiler.assembler import assemble

def generate(source_code: str, debug: bool = False) -> str:
  tokens = tokenize(source_code)
  parsed = parse(tokens)
  checked = typecheck(parsed, TypeTab)
  ir = generate_ir(root_types, parsed)
  assembly = generate_assembly(ir)
  if debug:
    for t in tokens:
      print(t)
    print()
    print(parsed)
    print()
    print(checked)
    print()
    for i in ir:
      print(i)
    print()
  return assembly

result = generate('''
false or true
''', )
print(result)
assemble(result, './src/compiler/compiled')
