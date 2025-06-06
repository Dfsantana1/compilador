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
        self.current_function = None
        self.errors = []
        self.function_params = {}  # Store function parameters

    def analyze(self, ast):
        if ast[0] == 'program':
            for declaration in ast[1]:
                self.analyze_declaration(declaration)
        return len(self.errors) == 0

    def analyze_declaration(self, declaration):
        if declaration[0] == 'var_declaration':
            self.analyze_var_declaration(declaration)
        elif declaration[0] == 'var_declaration_init':
            self.analyze_var_declaration_init(declaration)
        elif declaration[0] == 'fun_declaration':
            self.analyze_fun_declaration(declaration)

    def analyze_var_declaration(self, declaration):
        var_type = declaration[1]
        var_name = declaration[2]
        
        if var_name in self.symbol_table:
            self.errors.append(f"Variable '{var_name}' already declared")
        else:
            self.symbol_table[var_name] = {
                'type': var_type,
                'is_array': False,
                'size': None
            }

    def analyze_var_declaration_init(self, declaration):
        var_type = declaration[1]
        var_name = declaration[2]
        init_expr = declaration[3]
        
        if var_name in self.symbol_table:
            self.errors.append(f"Variable '{var_name}' already declared")
        else:
            self.symbol_table[var_name] = {
                'type': var_type,
                'is_array': False,
                'size': None
            }
            
            # Check initialization type
            init_type = self.get_expression_type(init_expr)
            if init_type != var_type:
                self.errors.append(f"Type mismatch in initialization of '{var_name}': expected {var_type}, got {init_type}")

    def analyze_fun_declaration(self, declaration):
        fun_type = declaration[1]
        fun_name = declaration[2]
        params = declaration[3]
        body = declaration[4]
        
        if fun_name in self.symbol_table:
            self.errors.append(f"Function '{fun_name}' already declared")
        else:
            self.symbol_table[fun_name] = {
                'type': fun_type,
                'params': params,
                'is_function': True
            }
            
            # Store parameters in symbol table
            self.function_params[fun_name] = {}
            for param in params:
                param_type = param[1]
                param_name = param[2]
                self.function_params[fun_name][param_name] = param_type
            
            # Analyze function body
            self.current_function = fun_name
            self.analyze_compound_stmt(body)
            self.current_function = None

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
            if len(stmt) > 1:
                self.get_expression_type(stmt[1])
        elif stmt[0] == 'return_stmt':
            if stmt[1] is not None:
                return_type = self.get_expression_type(stmt[1])
                if self.current_function:
                    fun_type = self.symbol_table[self.current_function]['type']
                    if return_type != fun_type:
                        self.errors.append(f"Return type mismatch in function '{self.current_function}': expected {fun_type}, got {return_type}")
        elif stmt[0] == 'if_stmt':
            self.analyze_if_stmt(stmt)
        elif stmt[0] == 'if_else_stmt':
            self.analyze_if_else_stmt(stmt)
        elif stmt[0] == 'while_stmt':
            self.analyze_while_stmt(stmt)
        elif stmt[0] == 'for_stmt':
            self.analyze_for_stmt(stmt)

    def analyze_if_stmt(self, stmt):
        condition = stmt[1]
        body = stmt[2]
        
        # Check condition type
        cond_type = self.get_expression_type(condition)
        if cond_type != 'int':
            self.errors.append(f"Condition must be of type 'int', got {cond_type}")
            
        self.analyze_statement(body)

    def analyze_if_else_stmt(self, stmt):
        condition = stmt[1]
        if_body = stmt[2]
        else_body = stmt[3]
        
        # Check condition type
        cond_type = self.get_expression_type(condition)
        if cond_type != 'int':
            self.errors.append(f"Condition must be of type 'int', got {cond_type}")
            
        self.analyze_statement(if_body)
        self.analyze_statement(else_body)

    def analyze_while_stmt(self, stmt):
        condition = stmt[1]
        body = stmt[2]
        
        # Check condition type
        cond_type = self.get_expression_type(condition)
        if cond_type != 'int':
            self.errors.append(f"Condition must be of type 'int', got {cond_type}")
            
        self.analyze_statement(body)

    def analyze_for_stmt(self, stmt):
        init = stmt[1]
        condition = stmt[2]
        update = stmt[3]
        body = stmt[4]

        # Analizar inicialización: puede ser declaración o statement
        if isinstance(init, tuple) and (init[0] == 'var_declaration' or init[0] == 'var_declaration_init'):
            self.analyze_declaration(init)
        else:
            self.analyze_statement(init)

        # Analizar condición (puede ser statement vacío)
        cond_type = None
        if isinstance(condition, tuple) and condition[0] == 'expression_stmt':
            if len(condition) > 1 and condition[1] is not None:
                cond_type = self.get_expression_type(condition[1])
        elif condition is not None:
            cond_type = self.get_expression_type(condition)
        if cond_type is not None and cond_type != 'int':
            self.errors.append(f"Condition must be of type 'int', got {cond_type}")

        # Analizar cuerpo y actualización
        self.analyze_statement(body)
        if update is not None:
            if isinstance(update, tuple) and update[0] == 'expression_stmt':
                if len(update) > 1 and update[1] is not None:
                    self.get_expression_type(update[1])
            else:
                self.analyze_statement(update)

    def get_expression_type(self, expr):
        if isinstance(expr, tuple):
            if expr[0] == 'assign':
                left_type = self.get_var_type(expr[1])
                right_type = self.get_expression_type(expr[2])
                if left_type != right_type:
                    self.errors.append(f"Type mismatch in assignment: expected {left_type}, got {right_type}")
                return left_type
            elif expr[0] == 'relop':
                left_type = self.get_expression_type(expr[2])
                right_type = self.get_expression_type(expr[3])
                if left_type != 'int' or right_type != 'int':
                    self.errors.append("Relational operators require integer operands")
                return 'int'
            elif expr[0] == 'addop':
                left_type = self.get_expression_type(expr[2])
                right_type = self.get_expression_type(expr[3])
                if left_type != 'int' or right_type != 'int':
                    self.errors.append("Arithmetic operators require integer operands")
                return 'int'
            elif expr[0] == 'mulop':
                left_type = self.get_expression_type(expr[2])
                right_type = self.get_expression_type(expr[3])
                if left_type != 'int' or right_type != 'int':
                    self.errors.append("Arithmetic operators require integer operands")
                return 'int'
            elif expr[0] == 'binop':
                left_type = self.get_expression_type(expr[2])
                right_type = self.get_expression_type(expr[3])
                operator = expr[1]
                
                if operator in ('&&', '||'):
                    if left_type != 'int' or right_type != 'int':
                        self.errors.append("Logical operators require integer operands")
                    return 'int'
                elif operator in ('+', '-', '*', '/', '%'):
                    if left_type != 'int' or right_type != 'int':
                        self.errors.append("Arithmetic operators require integer operands")
                    return 'int'
                elif operator in ('==', '!=', '<', '<=', '>', '>='):
                    if left_type != 'int' or right_type != 'int':
                        self.errors.append("Relational operators require integer operands")
                    return 'int'
            elif expr[0] == 'var':
                return self.get_var_type(expr)
            elif expr[0] == 'call':
                return self.get_call_type(expr)
        elif isinstance(expr, int):
            return 'int'
        elif isinstance(expr, str) and len(expr) == 1:  # Character literal
            return 'char'
        return None

    def get_var_type(self, var):
        if var[0] == 'var':
            var_name = var[1]
            # Check if variable is a function parameter
            if self.current_function and var_name in self.function_params.get(self.current_function, {}):
                return self.function_params[self.current_function][var_name]
            if var_name not in self.symbol_table:
                self.errors.append(f"Undefined variable '{var_name}'")
                return None
            return self.symbol_table[var_name]['type']
        elif var[0] == 'array_var':
            var_name = var[1]
            if var_name not in self.symbol_table:
                self.errors.append(f"Undefined array '{var_name}'")
                return None
            if not self.symbol_table[var_name]['is_array']:
                self.errors.append(f"'{var_name}' is not an array")
                return None
            return self.symbol_table[var_name]['type']
        return None

    def get_call_type(self, call):
        fun_name = call[1]
        args = call[2]
        
        if fun_name not in self.symbol_table:
            self.errors.append(f"Undefined function '{fun_name}'")
            return None
            
        fun_info = self.symbol_table[fun_name]
        if not fun_info.get('is_function'):
            self.errors.append(f"'{fun_name}' is not a function")
            return None
            
        # Check argument types
        params = fun_info['params']
        if len(args) != len(params):
            self.errors.append(f"Function '{fun_name}' expects {len(params)} arguments, got {len(args)}")
            return None
            
        for i, (arg, param) in enumerate(zip(args, params)):
            arg_type = self.get_expression_type(arg)
            param_type = param[1]
            if arg_type != param_type:
                self.errors.append(f"Argument {i+1} of function '{fun_name}' has wrong type: expected {param_type}, got {arg_type}")
                
        return fun_info['type']

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