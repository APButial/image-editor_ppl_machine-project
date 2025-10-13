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
    'PERCENT',
    'NUMBER',
    'STRING',
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

def t_COMMAND(t):
    r'[A-Za-z0-9_]+'
    
    # reject commands with digit
    if any(ch.isdigit() for ch in t.value):
        print(f"Invalid command: '{t.value}' (commands cannot contain digits)")
        return None

    t.value = t.value.lower()
    if t.value in reserved:
        t.is_reserved = True
    else:
        t.is_reserved = False
    t.type = 'COMMAND'
    return t

def t_PERCENT(t):
    r'(\d+(\.\d+)?)%'
    t.value = float(t.value[:-1])  # exclude percent sign
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    # string must be wrapped with double quotation
    r'"([^"\\]|\\.)*"'
    t.value = bytes(t.value[1:-1], "utf-8").decode("unicode_escape")
    return t

def infer_command(text):
    """
        infers entered command for auto-completion
    """    
    matches = [cmd for cmd in reserved.keys() if cmd.startswith(text)]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print(f"Ambiguous command '{text}'. Possible matches: {matches}")
        return None
    else:
        return None

    # # command inference # disabled for now, use in parser
    # inferred = infer_command(t.value)

    # if inferred:
    #     # match found
    #     t.type = 'COMMAND'
    #     t.value = inferred
    # else:
    #     # inference failed, try if in reserved
    #     if t.value in reserved:
    #         t.type = 'COMMAND'
    #         t.value = t.value
    #     else:
    #         # unrecognized command
    #         t.type = 'COMMAND'
    # return t

def t_OPTION(t):
    r'-[a-z]+'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)