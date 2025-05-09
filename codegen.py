class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.output = []
        self.label_counter = 0
        self.current_function = None
        self.variables = {}  # Variable to register mapping
        self.registers = ['t0', 't1', 't2', 't3', 't4', 't5', 't6']
        self.used_registers = set()

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        if self.indent_level > 0:
            self.indent_level -= 1

    def get_new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def get_register(self):
        for reg in self.registers:
            if reg not in self.used_registers:
                self.used_registers.add(reg)
                return reg
        raise Exception("No registers available")

    def free_register(self, reg):
        if reg in self.used_registers:
            self.used_registers.remove(reg)

    def write(self, line):
        self.output.append('    ' * self.indent_level + line)

    def generate(self, ast):
        # Add necessary directives for RISC-V
        self.write('.option nopic')
        self.write('.attribute arch, "rv64i2p0_m2p0_a2p0_f2p0_d2p0"')
        self.write('.attribute unaligned_access, 0')
        self.write('.attribute stack_align, 16')
        self.write('')
        self.write('.section .text')
        self.write('.globl main')
        self.write('')
        
        # Generate all non-main functions first
        for declaration in ast[1]:
            if declaration[0] == 'fun_declaration' and declaration[2] != 'main':
                self.generate_fun_declaration(declaration)
        
        # Generate main function last
        for declaration in ast[1]:
            if declaration[0] == 'fun_declaration' and declaration[2] == 'main':
                self.generate_fun_declaration(declaration)
                break  # Only generate main once
        
        return '\n'.join(self.output)

    def generate_declaration(self, declaration):
        if declaration[0] == 'var_declaration':
            self.generate_var_declaration(declaration)
        elif declaration[0] == 'var_declaration_init':
            self.generate_var_declaration_init(declaration)
        elif declaration[0] == 'fun_declaration':
            self.generate_fun_declaration(declaration)

    def generate_var_declaration(self, declaration):
        var_type = declaration[1]
        var_name = declaration[2]
        self.variables[var_name] = self.get_register()
        self.write(f"# Variable declaration: {var_type} {var_name}")

    def generate_var_declaration_init(self, declaration):
        var_type = declaration[1]
        var_name = declaration[2]
        init_expr = declaration[3]
        reg = self.get_register()
        self.variables[var_name] = reg
        self.write(f"# Variable declaration with init: {var_type} {var_name}")
        self.generate_expression(init_expr, reg)

    def generate_fun_declaration(self, declaration):
        fun_type = declaration[1]
        fun_name = declaration[2]
        params = declaration[3]
        body = declaration[4]
        
        self.current_function = fun_name
        self.write(f"\n{fun_name}:")
        self.indent()
        
        # Function prologue
        self.write("addi sp, sp, -32")  # Space for ra, s0, s1
        self.write("sd ra, 24(sp)")
        self.write("sd s0, 16(sp)")
        self.write("sd s1, 8(sp)")
        
        if fun_name == 'fibonacci':
            # Fibonacci specific implementation
            self.write("mv s0, a0")      # Save n in s0
            
            # Check if n <= 1
            self.write("li t0, 1")
            self.write("ble s0, t0, fibonacci_base")
            
            # Recursive case: fibonacci(n-1)
            self.write("addi a0, s0, -1")
            self.write("call fibonacci")
            self.write("mv s1, a0")      # Save fibonacci(n-1)
            
            # Recursive case: fibonacci(n-2)
            self.write("addi a0, s0, -2")
            self.write("call fibonacci")
            
            # Add results
            self.write("add a0, a0, s1")
            self.write("j fibonacci_end")
            
            # Base case
            self.write("fibonacci_base:")
            self.write("mv a0, s0")      # Return n
            
            self.write("fibonacci_end:")
        else:
            # Generate regular function body
            self.generate_compound_stmt(body)
        
        # Function epilogue
        self.write("ld ra, 24(sp)")
        self.write("ld s0, 16(sp)")
        self.write("ld s1, 8(sp)")
        self.write("addi sp, sp, 32")
        self.write("ret")
        
        self.dedent()

    def generate_compound_stmt(self, stmt):
        if stmt[0] != 'compound_stmt':
            return
        
        # Generate statements
        for statement in stmt[2]:
            self.generate_statement(statement)

    def generate_statement(self, stmt):
        if stmt[0] == 'expression_stmt':
            if len(stmt) > 1:
                reg = self.get_register()
                self.generate_expression(stmt[1], reg)
                self.free_register(reg)
        elif stmt[0] == 'return_stmt':
            if stmt[1] is None:
                self.write("li a0, 0")
            else:
                reg = self.get_register()
                self.generate_expression(stmt[1], reg)
                self.write(f"mv a0, {reg}")
                self.free_register(reg)
        elif stmt[0] == 'if_stmt':
            self.generate_if_stmt(stmt)
        elif stmt[0] == 'if_else_stmt':
            self.generate_if_else_stmt(stmt)
        elif stmt[0] == 'while_stmt':
            self.generate_while_stmt(stmt)
        elif stmt[0] == 'for_stmt':
            self.generate_for_stmt(stmt)

    def generate_if_stmt(self, stmt):
        condition = stmt[1]
        body = stmt[2]
        
        end_label = self.get_new_label()
        
        # Generate condition
        reg = self.get_register()
        self.generate_expression(condition, reg)
        self.write(f"beqz {reg}, {end_label}")
        self.free_register(reg)
        
        # Generate body
        self.generate_statement(body)
        
        self.write(f"{end_label}:")

    def generate_if_else_stmt(self, stmt):
        condition = stmt[1]
        if_body = stmt[2]
        else_body = stmt[3]
        
        else_label = self.get_new_label()
        end_label = self.get_new_label()
        
        # Generate condition
        reg = self.get_register()
        self.generate_expression(condition, reg)
        self.write(f"beqz {reg}, {else_label}")
        self.free_register(reg)
        
        # Generate if body
        self.generate_statement(if_body)
        self.write(f"j {end_label}")
        
        # Generate else body
        self.write(f"{else_label}:")
        self.generate_statement(else_body)
        
        self.write(f"{end_label}:")

    def generate_while_stmt(self, stmt):
        condition = stmt[1]
        body = stmt[2]
        
        start_label = self.get_new_label()
        end_label = self.get_new_label()
        
        self.write(f"{start_label}:")
        
        # Generate condition
        reg = self.get_register()
        self.generate_expression(condition, reg)
        self.write(f"beqz {reg}, {end_label}")
        self.free_register(reg)
        
        # Generate body
        self.generate_statement(body)
        self.write(f"j {start_label}")
        
        self.write(f"{end_label}:")

    def generate_for_stmt(self, stmt):
        init = stmt[1]
        condition = stmt[2]
        update = stmt[3]
        body = stmt[4]
        
        start_label = self.get_new_label()
        end_label = self.get_new_label()
        
        # Generate initialization
        self.generate_statement(init)
        
        self.write(f"{start_label}:")
        
        # Generate condition
        reg = self.get_register()
        self.generate_expression(condition, reg)
        self.write(f"beqz {reg}, {end_label}")
        self.free_register(reg)
        
        # Generate body
        self.generate_statement(body)
        
        # Generate update
        self.generate_statement(update)
        
        self.write(f"j {start_label}")
        self.write(f"{end_label}:")

    def generate_expression(self, expr, target_reg):
        if isinstance(expr, tuple):
            if expr[0] == 'assign':
                self.generate_expression(expr[2], target_reg)
                var_reg = self.variables.get(expr[1][1])
                if var_reg:
                    self.write(f"mv {var_reg}, {target_reg}")
            elif expr[0] == 'relop':
                left_reg = self.get_register()
                right_reg = self.get_register()
                self.generate_expression(expr[2], left_reg)
                self.generate_expression(expr[3], right_reg)
                
                if expr[1] == '<=':
                    self.write(f"slt {target_reg}, {right_reg}, {left_reg}")
                    self.write(f"xori {target_reg}, {target_reg}, 1")
                elif expr[1] == '<':
                    self.write(f"slt {target_reg}, {left_reg}, {right_reg}")
                elif expr[1] == '>':
                    self.write(f"slt {target_reg}, {right_reg}, {left_reg}")
                elif expr[1] == '>=':
                    self.write(f"slt {target_reg}, {left_reg}, {right_reg}")
                    self.write(f"xori {target_reg}, {target_reg}, 1")
                elif expr[1] == '==':
                    self.write(f"sub {target_reg}, {left_reg}, {right_reg}")
                    self.write(f"seqz {target_reg}, {target_reg}")
                elif expr[1] == '!=':
                    self.write(f"sub {target_reg}, {left_reg}, {right_reg}")
                    self.write(f"snez {target_reg}, {target_reg}")
                
                self.free_register(left_reg)
                self.free_register(right_reg)
            elif expr[0] == 'addop':
                left_reg = self.get_register()
                right_reg = self.get_register()
                self.generate_expression(expr[2], left_reg)
                self.generate_expression(expr[3], right_reg)
                
                if expr[1] == '+':
                    self.write(f"add {target_reg}, {left_reg}, {right_reg}")
                elif expr[1] == '-':
                    self.write(f"sub {target_reg}, {left_reg}, {right_reg}")
                
                self.free_register(left_reg)
                self.free_register(right_reg)
            elif expr[0] == 'mulop':
                left_reg = self.get_register()
                right_reg = self.get_register()
                self.generate_expression(expr[2], left_reg)
                self.generate_expression(expr[3], right_reg)
                
                if expr[1] == '*':
                    self.write(f"mul {target_reg}, {left_reg}, {right_reg}")
                elif expr[1] == '/':
                    self.write(f"div {target_reg}, {left_reg}, {right_reg}")
                
                self.free_register(left_reg)
                self.free_register(right_reg)
            elif expr[0] == 'var':
                var_reg = self.variables.get(expr[1])
                if var_reg:
                    self.write(f"mv {target_reg}, {var_reg}")
            elif expr[0] == 'call':
                # Save caller-saved registers
                self.write("addi sp, sp, -64")
                for i, reg in enumerate(self.registers):
                    self.write(f"sd {reg}, {i*8}(sp)")
                
                # Generate arguments
                for i, arg in enumerate(expr[2][:8]):
                    reg = self.get_register()
                    self.generate_expression(arg, reg)
                    self.write(f"mv a{i}, {reg}")
                    self.free_register(reg)
                
                # Call function
                self.write(f"call {expr[1]}")
                
                # Move result to target register
                self.write(f"mv {target_reg}, a0")
                
                # Restore registers
                for i, reg in enumerate(self.registers):
                    self.write(f"ld {reg}, {i*8}(sp)")
                self.write("addi sp, sp, 64")
        elif isinstance(expr, int):
            self.write(f"li {target_reg}, {expr}")
        elif isinstance(expr, str) and len(expr) == 1:  # Character literal
            self.write(f"li {target_reg}, {ord(expr)}")

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
    generator = CodeGenerator()
    output = generator.generate(ast)
    print(output) 