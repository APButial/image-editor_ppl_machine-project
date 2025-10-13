"""
    parser.py defines the grammar rules for the parser
"""

from lexer import tokens # parser needs access to valid tokens

## Expression ##############################

def p_expression_add(p):
    'expression : expression PLUS expression'
    p[0] = p[1] + p[3]

def p_expression_sub(p):
    'expression : expression MINUS expression'
    p[0] = p[1] - p[3]

def p_expression_mul(p):
    'expression : expression TIMES expression'
    p[0] = p[1] * p[3]

def p_expression_div(p):
    'expression : expression DIVIDE expression'
    if p[3] != 0:
        p[0] = p[1] / p[3]
    else:
        raise ZeroDivisionError("division by zero")
    
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_num(p):
    'expression : NUMBER'
    p[0] = p[1]

#############################################

## Argument ################################

def p_argument(p):
    '''argument : expression
                | FILENAME
    '''
    p[0] = p[1]

#############################################

## Statement ################################

def p_statement_cmd(p):
    'statement : COMMAND'
    p[0] = (p[1],)

def p_statement_cmd_opt(p):
    'statement : COMMAND OPTION'
    p[0] = (p[1], p[2])

def p_statement_cmd_arg(p):
    'statement : COMMAND argument'
    p[0] = (p[1], p[2])
    

def p_statement_cmd_opt_arg(p):
    'statement : COMMAND OPTION argument'
    p[0] = (p[1], p[2], p[3])


#############################################

## Program ##################################

def p_program_single(p):
    'program : statement'
    p[0] = [p[1]]

def p_program_multi(p):
    'program : program COMMA statement'
    p[0] = p[1] + [p[3]]