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
        self.symbol_table = {}  # Global symbol table
        self.function_params = {}
        self.current_function = None
        self.errors = []
        self.current_scope = 'global'  # Track current scope

    def analyze(self, ast):
        if ast[0] != 'program':
            return False
            
        for declaration in ast[1]:
            self.analyze_declaration(declaration)
            
        return len(self.errors) == 0

    def analyze_declaration(self, declaration):
        if declaration[0] == 'var_declaration':
            self.analyze_var_declaration(declaration)
        elif declaration[0] == 'fun_declaration':
            self.analyze_fun_declaration(declaration)

    def analyze_var_declaration(self, declaration):
        var_type = declaration[1]
        var_name = declaration[2]
        
        # Check if variable is already declared in current scope
        if self.current_scope == 'global':
            if var_name in self.symbol_table:
                self.errors.append(f"Variable '{var_name}' already declared in global scope")
                return
        else:  # Function scope
            if var_name in self.function_params.get(self.current_function, {}):
                self.errors.append(f"Variable '{var_name}' already declared as parameter")
                return
            if var_name in self.symbol_table:
                self.errors.append(f"Variable '{var_name}' already declared in function scope")
                return
        
        # Add variable to appropriate symbol table
        if self.current_scope == 'global':
            self.symbol_table[var_name] = {
                'type': var_type,
                'is_function': False,
                'scope': 'global'
            }
        else:
            self.symbol_table[var_name] = {
                'type': var_type,
                'is_function': False,
                'scope': self.current_function
            }
            
        # Si hay una inicialización, analizarla
        if len(declaration) > 3:
            init_expr = declaration[3]
            init_type = self.get_expression_type(init_expr)
            if init_type != var_type and not (var_type == 'int' and init_type == 'char'):
                self.errors.append(f"Type mismatch in initialization of '{var_name}': expected {var_type}, got {init_type}")

    def analyze_fun_declaration(self, declaration):
        fun_type = declaration[1]
        fun_name = declaration[2]
        params = declaration[3]
        body = declaration[4]
        
        if fun_name in self.symbol_table:
            self.errors.append(f"Function '{fun_name}' already declared")
            return
            
        self.symbol_table[fun_name] = {
            'type': fun_type,
            'params': params,
            'is_function': True,
            'scope': 'global'
        }
        
        # Store parameters in function_params
        self.function_params[fun_name] = {}
        for param in params:
            param_type = param[1]
            param_name = param[2]
            self.function_params[fun_name][param_name] = param_type
        
        # Analyze function body
        self.current_function = fun_name
        self.current_scope = fun_name
        self.analyze_compound_stmt(body)
        self.current_function = None
        self.current_scope = 'global'

    def analyze_compound_stmt(self, stmt):
        if stmt[0] != 'compound_stmt':
            return
            
        # Analyze local declarations
        for decl in stmt[1]:
            self.analyze_declaration(decl)
            
        # Analyze statements
        for stmt in stmt[2]:
            self.analyze_statement(stmt)

    def analyze_statement(self, stmt):
        if stmt[0] == 'expression_stmt':
            self.analyze_expression(stmt[1])
        elif stmt[0] == 'return_stmt':
            if stmt[1] is not None:
                self.analyze_expression(stmt[1])
        elif stmt[0] == 'compound_stmt':
            self.analyze_compound_stmt(stmt)

    def analyze_expression(self, expr):
        if isinstance(expr, tuple):
            if expr[0] == 'assign':
                left_type = self.get_var_type(expr[1])
                right_type = self.get_expression_type(expr[2])
                if left_type != right_type and not (left_type == 'int' and right_type == 'char'):
                    self.errors.append(f"Type mismatch in assignment: expected {left_type}, got {right_type}")
            elif expr[0] == 'addop':
                left_type = self.get_expression_type(expr[2])
                right_type = self.get_expression_type(expr[3])
                if not ((left_type == 'int' and right_type == 'int') or 
                       (left_type == 'int' and right_type == 'char') or
                       (left_type == 'char' and right_type == 'int')):
                    self.errors.append("Arithmetic operators require integer or character operands")
            elif expr[0] == 'var':
                self.get_var_type(expr)
            elif expr[0] == 'call':
                self.get_call_type(expr)

    def get_var_type(self, var):
        var_name = var[1]
        # Check if variable is a function parameter
        if self.current_function and var_name in self.function_params.get(self.current_function, {}):
            return self.function_params[self.current_function][var_name]
        if var_name not in self.symbol_table:
            self.errors.append(f"Variable '{var_name}' not declared")
            return None
        return self.symbol_table[var_name]['type']

    def get_call_type(self, call):
        fun_name = call[1]
        if fun_name not in self.symbol_table:
            self.errors.append(f"Function '{fun_name}' not declared")
            return None
        return self.symbol_table[fun_name]['type']

    def get_expression_type(self, expr):
        if isinstance(expr, tuple):
            if expr[0] == 'assign':
                return self.get_var_type(expr[1])
            elif expr[0] == 'addop':
                return 'int'  # Result of arithmetic is always int
            elif expr[0] == 'var':
                return self.get_var_type(expr)
            elif expr[0] == 'call':
                return self.get_call_type(expr)
        elif isinstance(expr, int):
            return 'int'
        elif isinstance(expr, str) and len(expr) == 1:  # Character literal
            return 'char'
        return None

# Test the semantic analyzer
if __name__ == '__main__':
    from parser import parser
    
    test_program = '''
    int main() {
        char c = 'a';
        int x = 5;
        for(int i = 0; i < 10; i++) {
            if (x > 0) {
                return x;
            }
        }
        return 0;
    }
    '''
    
    ast = parser.parse(test_program)
    analyzer = SemanticAnalyzer()
    if analyzer.analyze(ast):
        print("Semantic analysis passed!")
    else:
        print("Semantic analysis failed!")
        for error in analyzer.errors:
            print(f"Error: {error}") 