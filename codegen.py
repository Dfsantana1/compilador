class CodeGenerator:
    def __init__(self):
        self.indent_level = 0
        self.output = []
        self.label_counter = 0
        self.current_function = None
        self.variables = {}  # Variable to register mapping
        self.registers = ['t0', 't1', 't2', 't3', 't4', 't5', 't6']
        self.used_registers = set()
        self.stack_offset = 0

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
        # Si es una instrucción (no un label o comentario), formatear con tabs
        if line.strip() and not line.strip().endswith(':'):
            # Separar la instrucción y el comentario
            parts = line.split('#')
            instr = parts[0].strip()
            comment = '#' + parts[1] if len(parts) > 1 else ''
            
            # Formatear la instrucción con tabs después de las comas
            instr_parts = instr.split(',')
            formatted_instr = instr_parts[0].strip()
            for part in instr_parts[1:]:
                formatted_instr += ',\t' + part.strip()
            
            # Reconstruir la línea con el comentario
            line = formatted_instr + ('\t' + comment if comment else '')
        
        self.output.append(line)

    def generate(self, ast):
        # Generate all functions
        for declaration in ast[1]:
            if declaration[0] == 'fun_declaration':
                self.generate_fun_declaration(declaration)
        
        return '\n'.join(self.output)

    def reg_name(self, reg):
        # Convert register names to x-numbers
        reg_map = {
            'zero': 'x0',
            'ra': 'x1',
            'sp': 'x2',
            's0': 'x8',
            's1': 'x9',
            'a0': 'x10',
            'a1': 'x11',
            't0': 'x5',
            't1': 'x6',
            't2': 'x7',
            't3': 'x12',
            't4': 'x13',
            't5': 'x14',
            't6': 'x15'
        }
        return reg_map.get(reg, reg)

    def generate_fun_declaration(self, declaration):
        fun_type = declaration[1]
        fun_name = declaration[2]
        params = declaration[3]
        body = declaration[4]
        
        self.current_function = fun_name
        self.write(f"{fun_name.upper()}:")
        
        # Calculate stack size needed for this function
        self.stack_offset = 0
        for var in self.variables.values():
            self.stack_offset += 8  # Each variable takes 8 bytes
        
        # Add space for saved registers
        self.stack_offset += 40  # Space for ra, s0-s1, a0-a1
        
        # Prologue
        self.write(f"addi\tx2,\tx2,\t-{self.stack_offset}\t# Reservar espacio en la pila")
        self.write("sd\tx1,\t32(x2)\t# Guardar RA")
        self.write("sd\tx8,\t24(x2)\t# Guardar s0")
        self.write("sd\tx9,\t16(x2)\t# Guardar s1")
        self.write("sd\tx10,\t8(x2)\t# Guardar a0")
        self.write("sd\tx11,\t0(x2)\t# Guardar a1")
        self.write("")
        
        # Generate function body
        self.generate_compound_stmt(body)
        
        # Epilogue
        self.write("")
        self.write(f"{fun_name.upper()}_END:")
        self.write("ld\tx1,\t32(x2)\t# Restaurar RA")
        self.write("ld\tx8,\t24(x2)\t# Restaurar s0")
        self.write("ld\tx9,\t16(x2)\t# Restaurar s1")
        self.write("ld\tx10,\t8(x2)\t# Restaurar a0")
        self.write("ld\tx11,\t0(x2)\t# Restaurar a1")
        self.write(f"addi\tx2,\tx2,\t{self.stack_offset}")
        self.write("jalr\tx0,\t0(x1)\t# Retornar")

    def generate_compound_stmt(self, stmt):
        if stmt[0] != 'compound_stmt':
            return
        
        # Generate statements
        for statement in stmt[2]:
            self.generate_statement(statement)

    def generate_statement(self, stmt):
        stmt_type = stmt[0]
        
        if stmt_type == 'return':
            expr = stmt[1]
            if expr:
                self.generate_expr(expr)
            self.write("jal\tx0,\t" + self.current_function.upper() + "_END")
            
        elif stmt_type == 'if':
            condition = stmt[1]
            then_stmt = stmt[2]
            else_stmt = stmt[3] if len(stmt) > 3 else None
            
            # Generate condition
            self.generate_expr(condition)
            self.write("beq\tx10,\tx0,\t" + self.current_function.upper() + "_ELSE")
            
            # Generate then statement
            self.generate_statement(then_stmt)
            if else_stmt:
                self.write("jal\tx0,\t" + self.current_function.upper() + "_END")
                self.write(self.current_function.upper() + "_ELSE:")
                self.generate_statement(else_stmt)
            
        elif stmt_type == 'while':
            condition = stmt[1]
            body = stmt[2]
            
            self.write(self.current_function.upper() + "_WHILE:")
            self.generate_expr(condition)
            self.write("beq\tx10,\tx0,\t" + self.current_function.upper() + "_END")
            self.generate_statement(body)
            self.write("jal\tx0,\t" + self.current_function.upper() + "_WHILE")
            
        elif stmt_type == 'compound':
            self.generate_compound_stmt(stmt)
            
        elif stmt_type == 'expr':
            self.generate_expr(stmt[1])
            
        elif stmt_type == 'for':
            init = stmt[1]
            condition = stmt[2]
            update = stmt[3]
            body = stmt[4]
            
            # Generate initialization
            if init:
                self.generate_statement(init)
            
            self.write(self.current_function.upper() + "_FOR:")
            # Generate condition
            self.generate_expr(condition)
            self.write("beq\tx10,\tx0,\t" + self.current_function.upper() + "_END")
            
            # Generate body
            self.generate_statement(body)
            
            # Generate update
            if update:
                self.generate_statement(update)
            
            self.write("jal\tx0,\t" + self.current_function.upper() + "_FOR")

    def generate_expr(self, expr):
        if isinstance(expr, tuple):
            op = expr[0]
            
            if op == 'num':
                self.write(f"addi\tx10,\tx0,\t{expr[1]}\t# Cargar constante")
                
            elif op == 'id':
                var_offset = self.variables[expr[1]]
                self.write(f"ld\tx10,\t{var_offset}(x2)\t# Cargar variable {expr[1]}")
                
            elif op == 'call':
                fun_name = expr[1]
                args = expr[2]
                
                # Save caller-saved registers
                self.write("addi\tx2,\tx2,\t-64\t# Reservar espacio para registros")
                self.write("sd\tx5,\t0(x2)\t# Guardar registro t0")
                self.write("sd\tx6,\t8(x2)\t# Guardar registro t1")
                self.write("sd\tx7,\t16(x2)\t# Guardar registro t2")
                self.write("sd\tx12,\t24(x2)\t# Guardar registro t3")
                self.write("sd\tx13,\t32(x2)\t# Guardar registro t4")
                self.write("sd\tx14,\t40(x2)\t# Guardar registro t5")
                self.write("sd\tx15,\t48(x2)\t# Guardar registro t6")
                
                # Generate arguments
                for i, arg in enumerate(args):
                    self.generate_expr(arg)
                    if i == 0:
                        self.write("addi\tx10,\tx10,\t0\t# Pasar argumento 0")
                    elif i == 1:
                        self.write("addi\tx11,\tx10,\t0\t# Pasar argumento 1")
                
                # Call function
                self.write(f"jal\tx1,\t{fun_name.upper()}\t# Llamar función")
                
                # Restore caller-saved registers
                self.write("ld\tx5,\t0(x2)\t# Restaurar registro t0")
                self.write("ld\tx6,\t8(x2)\t# Restaurar registro t1")
                self.write("ld\tx7,\t16(x2)\t# Restaurar registro t2")
                self.write("ld\tx12,\t24(x2)\t# Restaurar registro t3")
                self.write("ld\tx13,\t32(x2)\t# Restaurar registro t4")
                self.write("ld\tx14,\t40(x2)\t# Restaurar registro t5")
                self.write("ld\tx15,\t48(x2)\t# Restaurar registro t6")
                self.write("addi\tx2,\tx2,\t64\t# Liberar espacio de registros")
                
            elif op in ['+', '-', '*', '/', '%']:
                self.generate_expr(expr[1])
                self.write("addi\tx5,\tx10,\t0\t# Guardar primer operando")
                self.generate_expr(expr[2])
                
                if op == '+':
                    self.write("add\tx10,\tx5,\tx10\t# Suma")
                elif op == '-':
                    self.write("sub\tx10,\tx5,\tx10\t# Resta")
                elif op == '*':
                    self.write("mul\tx10,\tx5,\tx10\t# Multiplicación")
                elif op == '/':
                    self.write("div\tx10,\tx5,\tx10\t# División")
                elif op == '%':
                    self.write("rem\tx10,\tx5,\tx10\t# Módulo")
                    
            elif op in ['<', '<=', '>', '>=', '==', '!=']:
                self.generate_expr(expr[1])
                self.write("addi\tx5,\tx10,\t0\t# Guardar primer operando")
                self.generate_expr(expr[2])
                
                if op == '<':
                    self.write("slt\tx10,\tx5,\tx10\t# Menor que")
                elif op == '<=':
                    self.write("slt\tx6,\tx10,\tx5\t# Mayor que")
                    self.write("xori\tx10,\tx6,\t1\t# Menor o igual que")
                elif op == '>':
                    self.write("slt\tx10,\tx10,\tx5\t# Mayor que")
                elif op == '>=':
                    self.write("slt\tx6,\tx5,\tx10\t# Menor que")
                    self.write("xori\tx10,\tx6,\t1\t# Mayor o igual que")
                elif op == '==':
                    self.write("sub\tx10,\tx5,\tx10\t# Resta")
                    self.write("sltiu\tx10,\tx10,\t1\t# Igual que")
                elif op == '!=':
                    self.write("sub\tx10,\tx5,\tx10\t# Resta")
                    self.write("sltu\tx10,\tx0,\tx10\t# Diferente que")
        elif isinstance(expr, int):
            self.write(f"addi\t{self.reg_name(target_reg)},\tx0,\t{expr}\t# Cargar constante")
        elif isinstance(expr, str) and len(expr) == 1:  # Character literal
            self.write(f"addi\t{self.reg_name(target_reg)},\tx0,\t{ord(expr)}\t# Cargar carácter")

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