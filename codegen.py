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

    def write(self, line, comment=None):
        """Write a line of assembly code with an optional comment"""
        if comment:
            self.output.append(f"{line}    # {comment}")
        else:
            self.output.append(line)

    def get_new_label(self):
        self.label_counter += 1
        return f".L{self.label_counter}"

    def generate(self, ast):
        if not ast:
            return ""
        
        # Add data section
        self.write(".section .data", "Sección de datos globales")
        self.write("    # Variables globales si las hubiera")
        self.write("")
        
        # Add text section
        self.write(".section .text", "Sección de código")
        self.write(".globl main", "Declaración de la función main como global")
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
        self.write(f"{fun_name}:", f"Inicio de la función {fun_name}")
        
        # Prologue - Save callee-saved registers
        frame_size = 32  # Base frame size
        self.write(f"        addi    sp,sp,-{frame_size}", "Reservar espacio en el stack")
        self.write("        sd      ra,24(sp)", "Guardar return address")
        self.write("        sd      s0,16(sp)", "Guardar frame pointer")
        self.write(f"        addi    s0,sp,{frame_size}", "Configurar nuevo frame pointer")
        
        # Process parameters
        for i, param in enumerate(params):
            if param[0] == 'param':
                param_name = param[2]
                self.variables[param_name] = self.current_offset
                self.current_offset += 4  # 4 bytes for 32-bit values
                # Save parameter from argument register to stack
                if i == 0:
                    self.write(f"        sw      a0,{self.variables[param_name]}(s0)", f"Guardar parámetro {param_name} en el stack")
                else:
                    self.write(f"        sw      a1,{self.variables[param_name]}(s0)", f"Guardar parámetro {param_name} en el stack")
        
        # Generate code for function body
        self.generate_compound_stmt(body)
        
        # Epilogue
        self.write("        ld      ra,24(sp)", "Restaurar return address")
        self.write("        ld      s0,16(sp)", "Restaurar frame pointer")
        self.write(f"        addi    sp,sp,{frame_size}", "Liberar espacio en el stack")
        self.write("        jr      ra", "Retornar de la función")

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
            self.write(f"        sw      a5,{self.variables[var_name]}(s0)", f"Guardar valor en variable {var_name}")

    def generate_statement(self, stmt):
        stmt_type = stmt[0]
        
        if stmt_type == 'expression_stmt':
            if len(stmt) > 1:  # Not an empty statement
                self.generate_expression(stmt[1])
        
        elif stmt_type == 'return_stmt':
            if stmt[1]:  # Has return expression
                self.generate_expression(stmt[1])
                self.write("        mv      a0,a5", "Mover resultado a a0")
            self.write("        j       .L3", "Salto a etiqueta .L3")
        
        elif stmt_type == 'if_stmt':
            else_label = self.get_new_label()
            end_label = self.get_new_label()
            
            # Generate condition
            self.generate_expression(stmt[1])
            self.write("        sext.w  a4,a5", "Extender a 64 bits")
            self.write("        li      a5,0", "Cargar 0 en a5")
            self.write(f"        ble     a4,a5,{else_label}", f"Comparar y saltar a {else_label} si a4 <= a5")
            
            # Generate then part
            self.generate_statement(stmt[2])
            self.write(f"        j       {end_label}", f"Salto a {end_label}")
            
            # Generate else part
            self.write(f"{else_label}:", f"Inicio de la sección else")
            if len(stmt) > 3:  # Has else part
                self.generate_statement(stmt[3])
            self.write(f"{end_label}:", "Fin de la sección if")
        
        elif stmt_type == 'while_stmt':
            start_label = self.get_new_label()
            end_label = self.get_new_label()
            
            self.write(f"{start_label}:", f"Inicio de la sección while")
            self.generate_expression(stmt[1])
            self.write("        sext.w  a4,a5", "Extender a 64 bits")
            self.write("        li      a5,0", "Cargar 0 en a5")
            self.write(f"        ble     a4,a5,{end_label}", f"Comparar y saltar a {end_label} si a4 <= a5")
            self.generate_statement(stmt[2])
            self.write(f"        j       {start_label}", f"Salto a {start_label}")
            self.write(f"{end_label}:", "Fin de la sección while")
            
        elif stmt_type == 'for_stmt':
            init = stmt[1]
            condition = stmt[2]
            update = stmt[3]
            body = stmt[4]
            
            start_label = self.get_new_label()
            end_label = self.get_new_label()
            
            # Generate initialization
            self.generate_statement(init)
            
            # Generate start of loop
            self.write(f"{start_label}:", f"Inicio de la sección for")
            
            # Generate condition
            self.generate_statement(condition)
            self.write("        sext.w  a4,a5", "Extender a 64 bits")
            self.write("        li      a5,0", "Cargar 0 en a5")
            self.write(f"        ble     a4,a5,{end_label}", f"Comparar y saltar a {end_label} si a4 <= a5")
            
            # Generate body
            self.generate_statement(body)
            
            # Generate update
            self.generate_expression(update)
            
            # Jump back to start
            self.write(f"        j       {start_label}", f"Salto a {start_label}")
            self.write(f"{end_label}:", "Fin de la sección for")

    def generate_expression(self, expr):
        if not isinstance(expr, tuple):
            # Handle literal values
            if isinstance(expr, int):
                self.write(f"        li      a5,{expr}", f"Cargar constante {expr}")
            return
            
        expr_type = expr[0]
        
        if expr_type == 'NUMBER':
            self.write(f"        li      a5,{expr[1]}", f"Cargar constante {expr[1]}")
        
        elif expr_type == 'var':
            var_name = expr[1]
            if var_name in self.variables:
                self.write(f"        lw      a5,{self.variables[var_name]}(s0)", f"Cargar variable {var_name}")
        
        elif expr_type == 'assign':
            var = expr[1][1]  # Get variable name from ('var', name)
            self.generate_expression(expr[2])  # Generate right side
            if var in self.variables:
                self.write(f"        sw      a5,{self.variables[var]}(s0)", f"Guardar valor en variable {var}")
        
        elif expr_type == 'call':
            fun_name = expr[1]
            args = expr[2] if expr[2] else []
            
            # Generate code for arguments
            for i, arg in enumerate(args):
                self.generate_expression(arg)
                if i == 0:
                    # Save first argument in a temporary location
                    self.write("        sw      a5,0(sp)", "Guardar primer argumento temporalmente")
                else:
                    # Move second argument to a1
                    self.write("        mv      a1,a5", "Mover segundo argumento a a1")
            
            # Move first argument to a0
            if len(args) > 0:
                self.write("        lw      a0,0(sp)", "Cargar primer argumento en a0")
            
            # Make the call
            self.write(f"        call    {fun_name}", f"Llamar a función {fun_name}")
            self.write("        mv      a5,a0", "Guardar resultado de la función")
        
        elif expr_type in ['addop', 'mulop']:
            # Generate left operand
            self.generate_expression(expr[2])
            # Save left operand in a temporary register
            self.write("        mv      a4,a5", "Guardar primer operando")
            
            # Generate right operand
            self.generate_expression(expr[3])
            
            # Perform operation based on type and operator
            if expr_type == 'addop':
                if expr[1] == '+':
                    self.write("        addw    a5,a4,a5", "Suma de operandos")
                else:  # '-'
                    self.write("        subw    a5,a4,a5", "Resta de operandos")
            else:  # mulop
                if expr[1] == '*':
                    self.write("        mulw    a5,a4,a5", "Multiplicación de operandos")
                else:  # '/'
                    self.write("        divw    a5,a4,a5", "División de operandos")
        
        elif expr_type == 'relop':
            # Generate left operand
            self.generate_expression(expr[2])
            self.write("        mv      a4,a5", "Guardar primer operando")
            
            # Generate right operand
            self.generate_expression(expr[3])
            
            # Compare based on operator using RV64I instructions
            if expr[1] == '<':
                self.write("        slt     a5,a4,a5", "Comparación menor que")
            elif expr[1] == '<=':
                self.write("        slt     t0,a5,a4", "Comparación menor o igual que")
                self.write("        xori    a5,t0,1", "Invertir resultado")
            elif expr[1] == '>':
                self.write("        slt     a5,a5,a4", "Comparación mayor que")
            elif expr[1] == '>=':
                self.write("        slt     t0,a4,a5", "Comparación mayor o igual que")
                self.write("        xori    a5,t0,1", "Invertir resultado")
            elif expr[1] == '==':
                self.write("        sub     t0,a4,a5", "Comparación igual que")
                self.write("        sltiu   a5,t0,1", "Convertir resultado a booleano")
            elif expr[1] == '!=':
                self.write("        sub     t0,a4,a5", "Comparación diferente que")
                self.write("        sltu    a5,zero,t0", "Convertir resultado a booleano")

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