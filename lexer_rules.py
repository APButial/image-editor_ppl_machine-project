tokens = (
    'NUMBER',
    'ID',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS',
    'LPAREN', 'RPAREN',
    'STRING', 'COMMENT', 'MULTICOMMENT',
    'IF', 'ELSE', 'WHILE'
)


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def find_column(text, lexpos):
    line_start = text.rfind('\n', 0, lexpos) + 1
    return (lexpos - line_start) + 1

def t_UNTERMINATED_MULTICOMMENT(t):
    r'/\*[\s\S]*$'
    column = find_column(t.lexer.lexdata, t.lexpos)
    print(f"Lexer error: unterminated comment '{t.value}' at line {t.lineno}, column {column}")
    t.lexer.skip(1)
    
def t_MULTICOMMENT(t):
    r'/\*[\s\S]*?\*/'
    return t

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ignore  = ' \t'

# Regular expression rules with some action code
def t_INVALID_NUMBER(t):
    r'\d+[A-Za-z_]+' # lookahead if digit is followed by an alphabetic character
    column = find_column(t.lexer.lexdata, t.lexpos)
    print(f"Lexer error: invalid numeric literal '{t.value}' at line {t.lineno}, column {column}")
    t.lexer.skip(1)

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    reserved = {'if': 'IF', 'else': 'ELSE', 'while': 'WHILE'}
    t.type = reserved.get(t.value, 'ID')
    return t

def t_STRING(t):
    r'".*?"'
    t.value = t.value[1:-1]
    return t

def t_COMMENT(t):
    r'\#.*'
    return t

# Error handling rule
def t_error(t):
    column = find_column(t.lexer.lexdata, t.lexpos)
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}, column {column}")
    t.lexer.skip(1)
