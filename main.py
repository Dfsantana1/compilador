import sys
import os
from lexer import lexer
from parser import parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator

def compile_file(input_file, output_file):
    try:
        # Asegurar que las carpetas existan
        os.makedirs('inputs', exist_ok=True)
        os.makedirs('outputs', exist_ok=True)
        
        # Construir rutas completas
        input_path = os.path.join('inputs', input_file)
        output_path = os.path.join('outputs', output_file)
        
        # Read input file
        with open(input_path, 'r') as f:
            source_code = f.read()
        
        # Lexical analysis
        lexer.input(source_code)
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(tok)
        
        # Syntax analysis
        ast = parser.parse(source_code)
        if ast is None:
            print("Syntax error in input file")
            return False
        
        # Semantic analysis
        analyzer = SemanticAnalyzer()
        if not analyzer.analyze(ast):
            print("Semantic errors found:")
            for error in analyzer.errors:
                print(f"Error: {error}")
            return False
        
        # Code generation
        generator = CodeGenerator()
        riscv_code = generator.generate(ast)
        
        # Write output file
        with open(output_path, 'w') as f:
            f.write(riscv_code)
        
        print(f"Compilation successful! Output written to {output_path}")
        return True
        
    except Exception as e:
        print(f"Error during compilation: {str(e)}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_file> <output_file>")
        print("Example: python main.py program.sc program.asm")
        print("Note: Input files should be in the 'inputs' directory")
        print("      Output files will be written to the 'outputs' directory")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not input_file.endswith('.sc'):
        print("Input file must have .sc extension")
        sys.exit(1)
    
    if not output_file.endswith('.asm'):
        print("Output file must have .asm extension")
        sys.exit(1)
    
    success = compile_file(input_file, output_file)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 