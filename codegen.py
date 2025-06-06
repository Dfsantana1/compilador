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

    def calculate_frame_size(self):
        """Calculate the required frame size for the current function"""
        # Base size for saved registers (ra, s0) = 8 bytes
        # Plus space for local variables and parameters
        total_size = 8 + self.current_offset
        # Round up to multiple of 8 for alignment
        return ((total_size + 7) // 8) * 8

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
        
        # Process parameters first to calculate their offsets
        for i, param in enumerate(params):
            if param[0] == 'param':
                param_name = param[2]
                self.variables[param_name] = self.current_offset
                self.current_offset += 4  # 4 bytes for 32-bit values
        
        # Calculate frame size based on variables and parameters
        frame_size = self.calculate_frame_size()
        
        # Prologue - Save callee-saved registers
        self.write(f"        addi    sp,sp,-{frame_size}", "Reservar espacio en el stack")
        self.write("        sw      ra,{}(sp)".format(frame_size - 4), "Guardar return address")
        self.write("        sw      s0,{}(sp)".format(frame_size - 8), "Guardar frame pointer")
        self.write(f"        addi    s0,sp,{frame_size}", "Configurar nuevo frame pointer")
        
        # Save parameters to stack
        for i, param in enumerate(params):
            if param[0] == 'param':
                param_name = param[2]
                if i == 0:
                    self.write(f"        sw      a0,{self.variables[param_name]}(s0)", f"Guardar parámetro {param_name} en el stack")
                else:
                    self.write(f"        sw      a1,{self.variables[param_name]}(s0)", f"Guardar parámetro {param_name} en el stack")
        
        # Generate code for function body
        self.generate_compound_stmt(body)
        
        # Epilogue
        self.write("        lw      ra,{}(sp)".format(frame_size - 4), "Restaurar return address")
        self.write("        lw      s0,{}(sp)".format(frame_size - 8), "Restaurar frame pointer")
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
            self.write("        li      a4,0", "Cargar 0 en a4")
            self.write(f"        ble     a5,a4,{else_label}", f"Comparar y saltar a {else_label} si a5 <= a4")
            
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
            self.write("        li      a4,0", "Cargar 0 en a4")
            self.write(f"        ble     a5,a4,{end_label}", f"Comparar y saltar a {end_label} si a5 <= a4")
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
            self.write("        li      a4,0", "Cargar 0 en a4")
            self.write(f"        ble     a5,a4,{end_label}", f"Comparar y saltar a {end_label} si a5 <= a4")
            
            # Generate body
            self.generate_statement(body)
            
            # Generate update
            self.generate_expression(update)
            
            # Jump back to start
            self.write(f"        j       {start_label}", f"Salto a {start_label}")
            self.write(f"{end_label}:", "Fin de la sección for")

    def generate_expression(self, expr):
        if expr is None:
            return ""
        
        if isinstance(expr, tuple):
            op = expr[0]
            if op == 'number':
                return f"    mov eax, {expr[1]}\n"
            elif op == 'id':
                return f"    mov eax, [{expr[1]}]\n"
            elif op == 'binop':
                left_code = self.generate_expression(expr[2])
                right_code = self.generate_expression(expr[3])
                operator = expr[1]
                
                if operator in ('&&', '||'):
                    # Para operadores lógicos, necesitamos evaluar el lado izquierdo primero
                    # y luego el derecho solo si es necesario
                    label_true = f"label_{self.label_counter}"
                    label_end = f"label_{self.label_counter + 1}"
                    self.label_counter += 2
                    
                    if operator == '&&':
                        # Para AND, si el izquierdo es falso, el resultado es falso
                        # Si el izquierdo es verdadero, evaluamos el derecho
                        return f"""{left_code}
    cmp eax, 0
    je {label_end}
{right_code}
{label_end}:
"""
                    else:  # operator == '||'
                        # Para OR, si el izquierdo es verdadero, el resultado es verdadero
                        # Si el izquierdo es falso, evaluamos el derecho
                        return f"""{left_code}
    cmp eax, 0
    jne {label_end}
{right_code}
{label_end}:
"""
                else:
                    # Para otros operadores, evaluamos ambos lados y aplicamos la operación
                    return f"""{left_code}
    push eax
{right_code}
    pop ebx
"""
                    if operator == '+':
                        return "    add eax, ebx\n"
                    elif operator == '-':
                        return "    sub eax, ebx\n"
                    elif operator == '*':
                        return "    mul ebx\n"
                    elif operator == '/':
                        return "    div ebx\n"
                    elif operator == '%':
                        return "    div ebx\n    mov eax, edx\n"  # El residuo queda en edx
                    elif operator == '==':
                        return "    cmp eax, ebx\n    sete al\n    movzx eax, al\n"
                    elif operator == '!=':
                        return "    cmp eax, ebx\n    setne al\n    movzx eax, al\n"
                    elif operator == '<':
                        return "    cmp eax, ebx\n    setl al\n    movzx eax, al\n"
                    elif operator == '<=':
                        return "    cmp eax, ebx\n    setle al\n    movzx eax, al\n"
                    elif operator == '>':
                        return "    cmp eax, ebx\n    setg al\n    movzx eax, al\n"
                    elif operator == '>=':
                        return "    cmp eax, ebx\n    setge al\n    movzx eax, al\n"
        return ""

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