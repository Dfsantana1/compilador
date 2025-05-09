import sys
from lexer import lexer
from parser import parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator

def compile_file(input_file):
    try:
        # Read input file
        with open(input_file, 'r') as f:
            source_code = f.read()

        # Lexical analysis
        lexer.input(source_code)
        tokens = list(lexer)
        
        # Parsing
        ast = parser.parse(source_code)
        if ast is None:
            print("Parsing failed")
            return

        # Semantic analysis
        analyzer = SemanticAnalyzer()
        errors = analyzer.analyze(ast)
        if errors:
            print("Semantic errors found:")
            for error in errors:
                print(error)
            return

        # Code generation
        generator = CodeGenerator()
        output_code = generator.generate(ast)

        # Write output to file
        output_file = input_file.rsplit('.', 1)[0] + '.c'
        with open(output_file, 'w') as f:
            f.write(output_code)

        print(f"Compilation successful. Output written to {output_file}")

    except Exception as e:
        print(f"Error during compilation: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    compile_file(input_file) 