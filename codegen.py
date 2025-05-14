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
        return f".L{self.label_counter}"

    def generate(self, ast):
        if not ast:
            return ""
        
        # Add data section
        self.write(".section .data")
        self.write("    # Variables globales si las hubiera")
        self.write("")
        
        # Add text section
        self.write(".section .text")
        self.write(".globl main")
        self.write("")
        
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
        self.write(f"        addi    sp,sp,-{frame_size}")
        self.write("        sd      ra,24(sp)")
        self.write("        sd      s0,16(sp)")
        self.write(f"        addi    s0,sp,{frame_size}")
        
        # Process parameters
        for i, param in enumerate(params):
            if param[0] == 'param':
                param_name = param[2]
                self.variables[param_name] = self.current_offset
                self.current_offset += 4  # 4 bytes for 32-bit values
                # Save parameter from argument register to stack
                if i == 0:
                    self.write(f"        sw      a0,{self.variables[param_name]}(s0)")
                else:
                    self.write(f"        sw      a1,{self.variables[param_name]}(s0)")
        
        # Generate code for function body
        self.generate_compound_stmt(body)
        
        # Epilogue
        self.write("        ld      ra,24(sp)")
        self.write("        ld      s0,16(sp)")
        self.write(f"        addi    sp,sp,{frame_size}")
        self.write("        jr      ra")

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
        self.current_offset += 4  # 4 bytes for 32-bit values
        
        if len(decl) > 3:  # Has initialization
            self.generate_expression(decl[3])
            self.write(f"        sw      a5,{self.variables[var_name]}(s0)")

    def generate_statement(self, stmt):
        stmt_type = stmt[0]
        
        if stmt_type == 'expression_stmt':
            if len(stmt) > 1:  # Not an empty statement
                self.generate_expression(stmt[1])
        
        elif stmt_type == 'return_stmt':
            if stmt[1]:  # Has return expression
                self.generate_expression(stmt[1])
                self.write("        mv      a0,a5")
            self.write("        j       .L3")
        
        elif stmt_type == 'if_stmt':
            else_label = self.get_new_label()
            end_label = self.get_new_label()
            
            # Generate condition
            self.generate_expression(stmt[1])
            self.write("        sext.w  a4,a5")
            self.write("        li      a5,0")
            self.write(f"        ble     a4,a5,{else_label}")
            
            # Generate then part
            self.generate_statement(stmt[2])
            self.write(f"        j       {end_label}")
            
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
            self.write("        sext.w  a4,a5")
            self.write("        li      a5,0")
            self.write(f"        ble     a4,a5,{end_label}")
            self.generate_statement(stmt[2])
            self.write(f"        j       {start_label}")
            self.write(f"{end_label}:")

    def generate_expression(self, expr):
        if not isinstance(expr, tuple):
            # Handle literal values
            if isinstance(expr, int):
                self.write(f"        li      a5,{expr}")
            return
            
        expr_type = expr[0]
        
        if expr_type == 'NUMBER':
            self.write(f"        li      a5,{expr[1]}")
        
        elif expr_type == 'var':
            var_name = expr[1]
            if var_name in self.variables:
                self.write(f"        lw      a5,{self.variables[var_name]}(s0)")
        
        elif expr_type == 'assign':
            var = expr[1][1]  # Get variable name from ('var', name)
            self.generate_expression(expr[2])  # Generate right side
            if var in self.variables:
                self.write(f"        sw      a5,{self.variables[var]}(s0)")
        
        elif expr_type == 'call':
            fun_name = expr[1]
            args = expr[2] if expr[2] else []
            
            # Generate code for arguments
            for i, arg in enumerate(args):
                self.generate_expression(arg)
                if i == 0:
                    # Save first argument in a temporary location
                    self.write("        sw      a5,0(sp)")
                else:
                    # Move second argument to a1
                    self.write("        mv      a1,a5")
            
            # Move first argument to a0
            if len(args) > 0:
                self.write("        lw      a0,0(sp)")
            
            # Make the call
            self.write(f"        call    {fun_name}")
            self.write("        mv      a5,a0")
        
        elif expr_type in ['addop', 'mulop']:
            # Generate left operand
            self.generate_expression(expr[2])
            # Save left operand in a temporary register
            self.write("        mv      a4,a5")
            
            # Generate right operand
            self.generate_expression(expr[3])
            
            # Perform operation based on type and operator
            if expr_type == 'addop':
                if expr[1] == '+':
                    self.write("        addw    a5,a4,a5")
                else:  # '-'
                    self.write("        subw    a5,a4,a5")
            else:  # mulop
                if expr[1] == '*':
                    self.write("        mulw    a5,a4,a5")
                else:  # '/'
                    self.write("        divw    a5,a4,a5")
        
        elif expr_type == 'relop':
            # Generate left operand
            self.generate_expression(expr[2])
            self.write("        mv      a4,a5")
            
            # Generate right operand
            self.generate_expression(expr[3])
            
            # Compare based on operator using RV64I instructions
            if expr[1] == '<':
                self.write("        slt     a5,a4,a5")
            elif expr[1] == '<=':
                self.write("        slt     t0,a5,a4")
                self.write("        xori    a5,t0,1")
            elif expr[1] == '>':
                self.write("        slt     a5,a5,a4")
            elif expr[1] == '>=':
                self.write("        slt     t0,a4,a5")
                self.write("        xori    a5,t0,1")
            elif expr[1] == '==':
                self.write("        sub     t0,a4,a5")
                self.write("        sltiu   a5,t0,1")
            elif expr[1] == '!=':
                self.write("        sub     t0,a4,a5")
                self.write("        sltu    a5,zero,t0")

# Test the code generator
if __name__ == '__main__':
    from parser import parser
    
    test_program = '''
    int main() {
        int x = 5;
        int y = 3;
        if (x > y) {
            return x;
        }
        return y;
    }
    '''
    
    ast = parser.parse(test_program)
    generator = CodeGenerator()
    output = generator.generate(ast)
    
    # Escribir la salida en test.asm
    with open('test.asm', 'w') as f:
        f.write(output)
    print("Código generado y guardado en test.asm") 