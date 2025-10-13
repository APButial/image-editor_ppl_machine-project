"""
    lexer.py defines the rules of the lexer
"""
reserved = {
    'blur': 'BLUR',
    'brightness': 'BRIGHTNESS',
    'contrast': 'CONTRAST',
    'convert': 'CONVERT',
    'crop': 'CROP',
    'exit': 'EXIT',
    'export': 'EXPORT',
    'exposure': 'EXPOSURE',
    'help': 'HELP',
    'open': 'OPEN',
    'redo': 'REDO',
    'remove_bg': 'REMOVE_BG',
    'resize': 'RESIZE',
    'rotate': 'ROTATE',
    'saturation': 'SATURATION',
    'sharpness': 'SHARPNESS',
    'temperature': 'TEMPERATURE',
    'undo': 'UNDO',
    'vibrance': 'VIBRANCE',
    'vignette': 'VIGNETTE',
}

tokens = (
    'NUMBER',
    'FILENAME',
    'COMMAND',
    'OPTION',
    'COMMA',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN'
)

t_COMMA = r','
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_INVALID_NUMBER(t):
    r'\d+[A-Za-z_]\w*'
    print(f"Invalid numeric literal: '{t.value}' (digits cannot contain alphabetic characters)")
    t.lexer.skip(1)
    return None

def t_COMMAND(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    
    # reject commands with digit
    if any(ch.isdigit() for ch in t.value):
        print(f"Invalid command: '{t.value}' (commands cannot contain digits)")
        t.lexer.skip(1)
        return None

    # change to lowercase for case-insensitivity
    t.value = t.value.lower()

    # for auto-completion
    matches = [cmd for cmd in reserved if cmd.startswith(t.value)]

    if len(matches) == 1:
        # unique
        t.value = matches[0]
        t.type = 'COMMAND'
        return t
    elif len(matches) > 1:
        # ambiguous
        print(f"Ambiguous command '{t.value}': possible matches {', '.join(matches)}")
        t.lexer.skip(1)
        return None
    else:
        # unknown command
        print(f"Unknown command: '{t.value}'")
        t.lexer.skip(1)
        return None

def t_FILENAME(t):
    # filename must be wrapped with double quotation
    r'"([^"\\]|\\.)*"'
    t.value = bytes(t.value[1:-1], "utf-8").decode("unicode_escape")
    return t

def t_OPTION(t):
    r'-[a-z]+'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)