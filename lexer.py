from ply import lex

# List of token names
tokens = (
    'ID',           # identifiers
    'NUMBER',       # integer literals
    'PLUS',         # +
    'MINUS',        # -
    'TIMES',        # *
    'DIVIDE',       # /
    'LPAREN',       # (
    'RPAREN',       # )
    'LBRACE',       # {
    'RBRACE',       # }
    'LBRACKET',     # [
    'RBRACKET',     # ]
    'SEMICOLON',    # ;
    'ASSIGN',       # =
    'EQ',           # ==
    'NE',           # !=
    'LT',           # <
    'LE',           # <=
    'GT',           # >
    'GE',           # >=
    'COMMA',        # ,
)

# Reserved words
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'int': 'INT',
    'return': 'RETURN',
    'void': 'VOID',
}

# Add reserved words to tokens
tokens = tokens + tuple(reserved.values())

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_SEMICOLON = r';'
t_ASSIGN = r'='
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_COMMA = r','

# Regular expression rule for identifiers
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Regular expression rule for numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Rule for tracking line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Test the lexer
if __name__ == '__main__':
    data = '''
    int main() {
        int x = 5;
        if (x > 0) {
            return x;
        }
        return 0;
    }
    '''
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok) 