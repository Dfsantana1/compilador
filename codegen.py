class CodeGenerator:
    def __init__(self):
        self.output = []
        self.label_counter = 0
        self.current_function = None
        self.variables = {}  # Variable to stack offset mapping
        self.current_offset = 0
        self.temp_counter = 0

    def get_temp(self):
        """Get a new temporary register number"""
        self.temp_counter += 1
        return self.temp_counter

    def write(self, line):
        self.output.append(line)

    def get_new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def generate(self, ast):
        if not ast:
            return ""
        # AST is ('program', [declarations])
        for declaration in ast[1]:
            if declaration[0] == 'fun_declaration':
                self.generate_fun_declaration(declaration)
        return '\n'.join(self.output)

    def generate_fun_declaration(self, declaration):
        # ('fun_declaration', type, name, params, body)
        fun_name = declaration[2]
        params = declaration[3]
        body = declaration[4]
        
        self.current_function = fun_name
        self.variables = {}  # Reset variables for new function
        self.current_offset = 0
        
        # Function label
        self.write(f"{fun_name}:")
        
        # Prologue - Save callee-saved registers
        frame_size = 32  # Base frame size
        self.write(f"addi\tx2,\tx2,\t-{frame_size}\t# Allocate stack frame")
        self.write("sd\tx1,\t24(x2)\t# Save return address")
        self.write("sd\tx8,\t16(x2)\t# Save frame pointer")
        self.write("sd\tx9,\t8(x2)\t# Save saved register")
        self.write(f"addi\tx8,\tx2,\t{frame_size}\t# Set up frame pointer")
        
        # Process parameters
        for i, param in enumerate(params):
            if param[0] == 'param':
                param_name = param[2]
                self.variables[param_name] = self.current_offset
                self.current_offset += 8
                # Save parameter from argument register to stack
                if i == 0:
                    self.write(f"sd\tx10,\t{self.variables[param_name]}(x2)\t# Store parameter {param_name}")
                else:
                    self.write(f"sd\tx11,\t{self.variables[param_name]}(x2)\t# Store parameter {param_name}")
        
        # Generate code for function body
        self.generate_compound_stmt(body)
        
        # Epilogue
        self.write(f"{fun_name}_END:")
        self.write("ld\tx1,\t24(x2)\t# Restore return address")
        self.write("ld\tx8,\t16(x2)\t# Restore frame pointer")
        self.write("ld\tx9,\t8(x2)\t# Restore saved register")
        self.write(f"addi\tx2,\tx2,\t{frame_size}\t# Deallocate stack frame")
        self.write("jalr\tx0,\t0(x1)\t# Return")

    def generate_compound_stmt(self, stmt):
        # ('compound_stmt', local_declarations, statement_list)
        local_decls = stmt[1]
        stmt_list = stmt[2]
        
        # Process local declarations
        for decl in local_decls:
            self.generate_var_declaration(decl)
        
        # Process statements
        for stmt in stmt_list:
            self.generate_statement(stmt)

    def generate_var_declaration(self, decl):
        # ('var_declaration', type, name) or ('var_declaration_init', type, name, init_expr)
        var_name = decl[2]
        self.variables[var_name] = self.current_offset
        self.current_offset += 8
        
        if len(decl) > 3:  # Has initialization
            self.generate_expression(decl[3])
            self.write(f"sd\tx10,\t{self.variables[var_name]}(x2)\t# Initialize {var_name}")

    def generate_statement(self, stmt):
        stmt_type = stmt[0]
        
        if stmt_type == 'expression_stmt':
            if len(stmt) > 1:  # Not an empty statement
                self.generate_expression(stmt[1])
        
        elif stmt_type == 'return_stmt':
            if stmt[1]:  # Has return expression
                self.generate_expression(stmt[1])
            self.write(f"jal\tx0,\t{self.current_function}_END")
        
        elif stmt_type == 'if_stmt':
            else_label = self.get_new_label()
            end_label = self.get_new_label()
            
            # Generate condition
            self.generate_expression(stmt[1])
            self.write(f"beq\tx10,\tx0,\t{else_label}")
            
            # Generate then part
            self.generate_statement(stmt[2])
            self.write(f"jal\tx0,\t{end_label}")
            
            # Generate else part
            self.write(f"{else_label}:")
            if len(stmt) > 3:  # Has else part
                self.generate_statement(stmt[3])
            self.write(f"{end_label}:")
        
        elif stmt_type == 'while_stmt':
            start_label = self.get_new_label()
            end_label = self.get_new_label()
            
            self.write(f"{start_label}:")
            self.generate_expression(stmt[1])
            self.write(f"beq\tx10,\tx0,\t{end_label}")
            self.generate_statement(stmt[2])
            self.write(f"jal\tx0,\t{start_label}")
            self.write(f"{end_label}:")

    def generate_expression(self, expr):
        if not isinstance(expr, tuple):
            # Handle literal values
            if isinstance(expr, int):
                self.write(f"addi\tx10,\tx0,\t{expr}\t# Load immediate")
            return
            
        expr_type = expr[0]
        
        if expr_type == 'NUMBER':
            self.write(f"addi\tx10,\tx0,\t{expr[1]}\t# Load constant")
        
        elif expr_type == 'var':
            var_name = expr[1]
            if var_name in self.variables:
                self.write(f"ld\tx10,\t{self.variables[var_name]}(x2)\t# Load {var_name}")
        
        elif expr_type == 'assign':
            var = expr[1][1]  # Get variable name from ('var', name)
            self.generate_expression(expr[2])  # Generate right side
            if var in self.variables:
                self.write(f"sd\tx10,\t{self.variables[var]}(x2)\t# Store to {var}")
        
        elif expr_type == 'call':
            fun_name = expr[1]
            args = expr[2] if expr[2] else []
            
            # Save temporary registers that might be needed after the call
            temp = self.get_temp()
            
            # Generate code for arguments
            for i, arg in enumerate(args):
                self.generate_expression(arg)
                if i == 0:
                    # Save first argument in a temporary location
                    self.write("sd\tx10,\t0(x2)\t# Save first argument")
                else:
                    # Move second argument to x11
                    self.write("addi\tx11,\tx10,\t0\t# Move second argument to x11")
            
            # Move first argument to x10
            if len(args) > 0:
                self.write("ld\tx10,\t0(x2)\t# Restore first argument to x10")
            
            # Make the call
            self.write(f"jal\tx1,\t{fun_name}")
        
        elif expr_type in ['addop', 'mulop']:
            # Generate left operand
            self.generate_expression(expr[2])
            # Save left operand in a temporary register
            temp_reg = self.get_temp()
            self.write(f"addi\tx{temp_reg},\tx10,\t0\t# Save left operand")
            
            # Generate right operand
            self.generate_expression(expr[3])
            
            # Perform operation based on type and operator
            if expr_type == 'addop':
                if expr[1] == '+':
                    self.write(f"add\tx10,\tx{temp_reg},\tx10\t# Add")
                else:  # '-'
                    self.write(f"sub\tx10,\tx{temp_reg},\tx10\t# Subtract")
            else:  # mulop
                if expr[1] == '*':
                    self.write(f"mul\tx10,\tx{temp_reg},\tx10\t# Multiply")
                else:  # '/'
                    # Check for division by zero
                    zero_label = self.get_new_label()
                    continue_label = self.get_new_label()
                    self.write(f"beq\tx10,\tx0,\t{zero_label}\t# Check for division by zero")
                    self.write(f"div\tx10,\tx{temp_reg},\tx10\t# Divide")
                    self.write(f"jal\tx0,\t{continue_label}")
                    self.write(f"{zero_label}:")
                    self.write("addi\tx10,\tx0,\t0\t# Return 0 for division by zero")
                    self.write(f"{continue_label}:")
        
        elif expr_type == 'relop':
            # Generate operands
            self.generate_expression(expr[2])
            self.write("sd\tx10,\t0(x2)\t# Save left operand")
            self.generate_expression(expr[3])
            self.write("addi\tx5,\tx10,\t0\t# Move right operand")
            self.write("ld\tx10,\t0(x2)\t# Restore left operand")
            
            # Compare based on operator
            if expr[1] in ['<', '<=', '>', '>=']:
                self.write("sub\tx10,\tx10,\tx5\t# Compare")
                false_label = self.get_new_label()
                true_label = self.get_new_label()
                done_label = self.get_new_label()
                
                if expr[1] in ['>', '>=']:
                    # Para '>' verificamos si la resta es mayor que 0
                    self.write(f"beq\tx10,\tx0,\t{false_label}\t# Branch if equal to zero")
                    self.write("addi\tx5,\tx0,\t0\t# Load 0")
                    self.write(f"blt\tx5,\tx10,\t{true_label}\t# Branch if greater than zero")
                    self.write(f"{false_label}:")
                    self.write("addi\tx10,\tx0,\t0\t# False")
                    self.write(f"jal\tx0,\t{done_label}")
                    self.write(f"{true_label}:")
                    self.write("addi\tx10,\tx0,\t1\t# True")
                    self.write(f"{done_label}:")
                else:  # '<' o '<='
                    # Para '<' verificamos si la resta es menor que 0
                    self.write(f"beq\tx10,\tx0,\t{false_label}\t# Branch if equal to zero")
                    self.write("addi\tx5,\tx0,\t0\t# Load 0")
                    self.write(f"blt\tx10,\tx5,\t{true_label}\t# Branch if less than zero")
                    self.write(f"{false_label}:")
                    self.write("addi\tx10,\tx0,\t0\t# False")
                    self.write(f"jal\tx0,\t{done_label}")
                    self.write(f"{true_label}:")
                    self.write("addi\tx10,\tx0,\t1\t# True")
                    self.write(f"{done_label}:")
            elif expr[1] in ['==', '!=']:
                self.write("sub\tx10,\tx10,\tx5\t# Compare equal")
                false_label = self.get_new_label()
                true_label = self.get_new_label()
                done_label = self.get_new_label()
                
                if expr[1] == '==':
                    self.write(f"beq\tx10,\tx0,\t{true_label}\t# Branch if equal")
                    self.write("addi\tx10,\tx0,\t0\t# False")
                    self.write(f"jal\tx0,\t{done_label}")
                    self.write(f"{true_label}:")
                    self.write("addi\tx10,\tx0,\t1\t# True")
                    self.write(f"{done_label}:")
                else:  # '!='
                    self.write(f"bne\tx10,\tx0,\t{true_label}\t# Branch if not equal")
                    self.write("addi\tx10,\tx0,\t0\t# False")
                    self.write(f"jal\tx0,\t{done_label}")
                    self.write(f"{true_label}:")
                    self.write("addi\tx10,\tx0,\t1\t# True")
                    self.write(f"{done_label}:")

# Test the code generator
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
    print("AST:", ast)  # Debug print
    generator = CodeGenerator()
    output = generator.generate(ast)
    print(output) 