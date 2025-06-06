from ply import yacc
from lexer import tokens

# Grammar rules
def p_program(p):
    '''program : declaration_list'''
    p[0] = ('program', p[1])

def p_declaration_list(p):
    '''declaration_list : declaration
                       | declaration_list declaration'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_declaration(p):
    '''declaration : var_declaration
                  | fun_declaration'''
    p[0] = p[1]

def p_var_declaration(p):
    '''var_declaration : type_specifier ID SEMICOLON
                      | type_specifier ID ASSIGN expression SEMICOLON'''
    if len(p) == 4:
        p[0] = ('var_declaration', p[1], p[2])
    else:
        p[0] = ('var_declaration', p[1], p[2], p[4])

def p_type_specifier(p):
    '''type_specifier : INT
                     | CHAR
                     | VOID'''
    p[0] = p[1]

def p_fun_declaration(p):
    '''fun_declaration : type_specifier ID LPAREN params RPAREN compound_stmt'''
    p[0] = ('fun_declaration', p[1], p[2], p[4], p[6])

def p_params(p):
    '''params : param_list
              | VOID
              | empty'''
    if p[1] == 'void':
        p[0] = []
    elif p[1] is None:
        p[0] = []
    else:
        p[0] = p[1]

def p_param_list(p):
    '''param_list : param
                 | param_list COMMA param'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_param(p):
    '''param : type_specifier ID'''
    p[0] = ('param', p[1], p[2])

def p_compound_stmt(p):
    '''compound_stmt : LBRACE local_declarations statement_list RBRACE'''
    p[0] = ('compound_stmt', p[2], p[3])

def p_local_declarations(p):
    '''local_declarations : empty
                         | local_declarations var_declaration'''
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_statement_list(p):
    '''statement_list : empty
                     | statement_list statement'''
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : expression_stmt
                | compound_stmt
                | return_stmt
                | if_stmt'''
    p[0] = p[1]

def p_expression_stmt(p):
    '''expression_stmt : expression SEMICOLON
                      | SEMICOLON'''
    if len(p) == 3:
        p[0] = ('expression_stmt', p[1])
    else:
        p[0] = ('empty_stmt',)

def p_return_stmt(p):
    '''return_stmt : RETURN SEMICOLON
                  | RETURN expression SEMICOLON'''
    if len(p) == 3:
        p[0] = ('return_stmt', None)
    else:
        p[0] = ('return_stmt', p[2])

def p_if_stmt(p):
    '''if_stmt : IF LPAREN expression RPAREN statement
               | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = ('if_stmt', p[3], p[5])
    else:
        p[0] = ('if_else_stmt', p[3], p[5], p[7])

def p_expression(p):
    '''expression : var ASSIGN expression
                 | logical_or_expression'''
    if len(p) == 4:
        p[0] = ('assign', p[1], p[3])
    else:
        p[0] = p[1]

def p_logical_or_expression(p):
    '''logical_or_expression : logical_or_expression OR logical_and_expression
                            | logical_and_expression'''
    if len(p) == 4:
        p[0] = ('or', p[1], p[3])
    else:
        p[0] = p[1]

def p_logical_and_expression(p):
    '''logical_and_expression : logical_and_expression AND equality_expression
                             | equality_expression'''
    if len(p) == 4:
        p[0] = ('and', p[1], p[3])
    else:
        p[0] = p[1]

def p_equality_expression(p):
    '''equality_expression : equality_expression EQ relational_expression
                          | equality_expression NE relational_expression
                          | relational_expression'''
    if len(p) == 4:
        p[0] = ('relop', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_relational_expression(p):
    '''relational_expression : relational_expression LT additive_expression
                            | relational_expression LE additive_expression
                            | relational_expression GT additive_expression
                            | relational_expression GE additive_expression
                            | additive_expression'''
    if len(p) == 4:
        p[0] = ('relop', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_additive_expression(p):
    '''additive_expression : additive_expression PLUS multiplicative_expression
                          | additive_expression MINUS multiplicative_expression
                          | multiplicative_expression'''
    if len(p) == 4:
        p[0] = ('addop', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_multiplicative_expression(p):
    '''multiplicative_expression : multiplicative_expression TIMES unary_expression
                                | multiplicative_expression DIVIDE unary_expression
                                | unary_expression'''
    if len(p) == 4:
        p[0] = ('mulop', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_unary_expression(p):
    '''unary_expression : factor'''
    p[0] = p[1]

def p_factor(p):
    '''factor : LPAREN expression RPAREN
              | var
              | call
              | NUMBER
              | CHAR_LITERAL'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_var(p):
    '''var : ID'''
    p[0] = ('var', p[1])

def p_call(p):
    '''call : ID LPAREN args RPAREN'''
    p[0] = ('call', p[1], p[3])

def p_args(p):
    '''args : arg_list
            | empty'''
    p[0] = p[1]

def p_arg_list(p):
    '''arg_list : expression
                | arg_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_empty(p):
    'empty :'
    p[0] = None

# Error handling
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Test the parser
if __name__ == '__main__':
    data = '''
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
    result = parser.parse(data)
    print(result) 