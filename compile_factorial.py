import sys
from parser import parser
from codegen import CodeGenerator

def compile_c_to_asm(input_file, output_file):
    # Read the input C file
    with open(input_file, 'r') as f:
        program = f.read()
    
    # Parse the program
    ast = parser.parse(program)
    print("AST:", ast)  # Debug print
    
    # Generate RISC-V assembly
    generator = CodeGenerator()
    output = generator.generate(ast)
    
    # Write the output to the .asm file
    with open(output_file, 'w') as f:
        f.write(output)
    
    print(f"\nCompilation successful!")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 compile_factorial.py input.c output.asm")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not input_file.endswith('.c'):
        print("Error: Input file must have .c extension")
        sys.exit(1)
    
    if not output_file.endswith('.asm'):
        print("Error: Output file must have .asm extension")
        sys.exit(1)
    
    compile_c_to_asm(input_file, output_file) 