class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.output = []

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level -= 1

    def write(self, line):
        self.output.append('    ' * self.indent_level + line)

    def generate(self, ast):
        if ast[0] == 'program':
            for declaration in ast[1]:
                self.generate_declaration(declaration)
        return '\n'.join(self.output)

    def generate_declaration(self, declaration):
        if declaration[0] == 'var_declaration':
            self.generate_var_declaration(declaration)
        elif declaration[0] == 'fun_declaration':
            self.generate_fun_declaration(declaration)

    def generate_var_declaration(self, declaration):
        var_type = declaration[1]
        var_name = declaration[2]
        self.write(f"{var_type} {var_name};")

    def generate_fun_declaration(self, declaration):
        fun_type = declaration[1]
        fun_name = declaration[2]
        params = declaration[3]
        body = declaration[4]

        # Generate function header
        param_str = ', '.join(f"{p[1]} {p[2]}" for p in params)
        self.write(f"{fun_type} {fun_name}({param_str}) {{")
        self.indent()

        # Generate function body
        self.generate_compound_stmt(body)

        self.dedent()
        self.write("}")

    def generate_compound_stmt(self, stmt):
        if stmt[0] != 'compound_stmt':
            return

        # Generate local declarations
        for decl in stmt[1]:
            self.generate_declaration(decl)

        # Generate statements
        for stmt in stmt[2]:
            self.generate_statement(stmt)

    def generate_statement(self, stmt):
        if stmt[0] == 'expression_stmt':
            if len(stmt) > 1:
                expr = self.generate_expression(stmt[1])
                self.write(f"{expr};")
        elif stmt[0] == 'return_stmt':
            if stmt[1] is None:
                self.write("return;")
            else:
                expr = self.generate_expression(stmt[1])
                self.write(f"return {expr};")
        elif stmt[0] == 'if_stmt':
            self.generate_if_stmt(stmt)
        elif stmt[0] == 'if_else_stmt':
            self.generate_if_else_stmt(stmt)
        elif stmt[0] == 'while_stmt':
            self.generate_while_stmt(stmt)
        elif stmt[0] == 'compound_stmt':
            self.write("{")
            self.indent()
            self.generate_compound_stmt(stmt)
            self.dedent()
            self.write("}")

    def generate_if_stmt(self, stmt):
        condition = self.generate_expression(stmt[1])
        self.write(f"if ({condition}) {{")
        self.indent()
        self.generate_statement(stmt[2])
        self.dedent()
        self.write("}")

    def generate_if_else_stmt(self, stmt):
        condition = self.generate_expression(stmt[1])
        self.write(f"if ({condition}) {{")
        self.indent()
        self.generate_statement(stmt[2])
        self.dedent()
        self.write("} else {")
        self.indent()
        self.generate_statement(stmt[3])
        self.dedent()
        self.write("}")

    def generate_while_stmt(self, stmt):
        condition = self.generate_expression(stmt[1])
        self.write(f"while ({condition}) {{")
        self.indent()
        self.generate_statement(stmt[2])
        self.dedent()
        self.write("}")

    def generate_expression(self, expr):
        if isinstance(expr, tuple):
            if expr[0] == 'assign':
                left = self.generate_expression(expr[1])
                right = self.generate_expression(expr[2])
                return f"{left} = {right}"
            elif expr[0] == 'relop':
                left = self.generate_expression(expr[2])
                op = expr[1]
                right = self.generate_expression(expr[3])
                return f"{left} {op} {right}"
            elif expr[0] == 'addop':
                left = self.generate_expression(expr[2])
                op = expr[1]
                right = self.generate_expression(expr[3])
                return f"{left} {op} {right}"
            elif expr[0] == 'mulop':
                left = self.generate_expression(expr[2])
                op = expr[1]
                right = self.generate_expression(expr[3])
                return f"{left} {op} {right}"
            elif expr[0] == 'call':
                return self.generate_call(expr)
            elif expr[0] == 'var':
                return expr[1]
        return str(expr)

    def generate_var(self, var):
        return var[1]

    def generate_call(self, call):
        fun_name = call[1]
        args = [self.generate_expression(arg) for arg in call[2]]
        return f"{fun_name}({', '.join(args)})"

# Test the code generator
if __name__ == '__main__':
    from parser import parser
    
    test_program = '''
    int main() {
        int x = 5;
        if (x > 0) {
            return x;
        }
        return 0;
    }
    '''
    
    ast = parser.parse(test_program)
    generator = CodeGenerator()
    output = generator.generate(ast)
    print(output) 