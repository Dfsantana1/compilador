class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # List of dictionaries for nested scopes
        self.current_scope = 0

    def enter_scope(self):
        self.scopes.append({})
        self.current_scope += 1

    def exit_scope(self):
        if self.current_scope > 0:
            self.scopes.pop()
            self.current_scope -= 1

    def add_symbol(self, name, symbol_type, is_array=False):
        self.scopes[self.current_scope][name] = {
            'type': symbol_type,
            'is_array': is_array
        }

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.current_function = None
        self.errors = []

    def analyze(self, ast):
        if ast[0] == 'program':
            for declaration in ast[1]:
                self.analyze_declaration(declaration)
        return self.errors

    def analyze_declaration(self, declaration):
        if declaration[0] == 'var_declaration':
            self.analyze_var_declaration(declaration)
        elif declaration[0] == 'fun_declaration':
            self.analyze_fun_declaration(declaration)

    def analyze_var_declaration(self, declaration):
        var_type = declaration[1]
        var_name = declaration[2]
        
        # Check if variable is already declared in current scope
        if var_name in self.symbol_table.scopes[self.symbol_table.current_scope]:
            self.errors.append(f"Error: Variable '{var_name}' already declared in current scope")
        else:
            self.symbol_table.add_symbol(var_name, var_type)

    def analyze_fun_declaration(self, declaration):
        fun_type = declaration[1]
        fun_name = declaration[2]
        params = declaration[3]
        body = declaration[4]

        # Check if function is already declared
        if fun_name in self.symbol_table.scopes[0]:
            self.errors.append(f"Error: Function '{fun_name}' already declared")
            return

        # Add function to global scope
        self.symbol_table.add_symbol(fun_name, fun_type)
        self.current_function = fun_name

        # Enter new scope for function body
        self.symbol_table.enter_scope()

        # Add parameters to symbol table
        for param in params:
            param_type = param[1]
            param_name = param[2]
            self.symbol_table.add_symbol(param_name, param_type)

        # Analyze function body
        self.analyze_compound_stmt(body)

        # Exit function scope
        self.symbol_table.exit_scope()
        self.current_function = None

    def analyze_compound_stmt(self, stmt):
        if stmt[0] != 'compound_stmt':
            return

        # Enter new scope for compound statement
        self.symbol_table.enter_scope()

        # Analyze local declarations
        for decl in stmt[1]:
            self.analyze_declaration(decl)

        # Analyze statements
        for stmt in stmt[2]:
            self.analyze_statement(stmt)

        # Exit compound statement scope
        self.symbol_table.exit_scope()

    def analyze_statement(self, stmt):
        if stmt[0] == 'expression_stmt':
            if len(stmt) > 1:
                self.analyze_expression(stmt[1])
        elif stmt[0] == 'return_stmt':
            if stmt[1] is not None:
                self.analyze_expression(stmt[1])
        elif stmt[0] == 'if_stmt':
            self.analyze_expression(stmt[1])
            self.analyze_statement(stmt[2])
        elif stmt[0] == 'if_else_stmt':
            self.analyze_expression(stmt[1])
            self.analyze_statement(stmt[2])
            self.analyze_statement(stmt[3])
        elif stmt[0] == 'while_stmt':
            self.analyze_expression(stmt[1])
            self.analyze_statement(stmt[2])
        elif stmt[0] == 'compound_stmt':
            self.analyze_compound_stmt(stmt)

    def analyze_expression(self, expr):
        if isinstance(expr, tuple):
            if expr[0] == 'assign':
                self.analyze_expression(expr[1])
                self.analyze_expression(expr[2])
            elif expr[0] == 'relop':
                self.analyze_expression(expr[1])
                self.analyze_expression(expr[2])
            elif expr[0] == 'addop':
                self.analyze_expression(expr[1])
                self.analyze_expression(expr[2])
            elif expr[0] == 'mulop':
                self.analyze_expression(expr[1])
                self.analyze_expression(expr[2])
            elif expr[0] == 'call':
                self.analyze_call(expr)
            elif expr[0] == 'var':
                self.analyze_var(expr)

    def analyze_var(self, var):
        var_name = var[1]
        symbol = self.symbol_table.lookup(var_name)
        if symbol is None:
            self.errors.append(f"Error: Undefined variable '{var_name}'")

    def analyze_call(self, call):
        fun_name = call[1]
        args = call[2]

        # Check if function exists
        symbol = self.symbol_table.lookup(fun_name)
        if symbol is None:
            self.errors.append(f"Error: Undefined function '{fun_name}'")
            return

        # Analyze arguments
        for arg in args:
            self.analyze_expression(arg)

# Test the semantic analyzer
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
    analyzer = SemanticAnalyzer()
    errors = analyzer.analyze(ast)
    
    if errors:
        print("Semantic errors found:")
        for error in errors:
            print(error)
    else:
        print("No semantic errors found") 