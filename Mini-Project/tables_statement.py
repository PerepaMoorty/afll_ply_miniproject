# Example Lua code:
code = ''' mytable = {a = 1, b = {x = 2, y = 3}, [5] = 10} '''

import ply.lex as lex
import ply.yacc as yacc

# Lexer

tokens = (
    'LBRACE',
    'RBRACE',
    'LBRACKET',
    'RBRACKET',
    'ID',
    'NUMBER',
    'EQUAL',
    'COMMA'
)

t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_EQUAL = r'='
t_COMMA = r','
t_ID = r'[a-zA-Z_]\w*'
t_NUMBER = r'\d+'

t_ignore = ' \t\n'

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at position {t.lexpos}")
    t.lexer.skip(1)
    exit()

lexer = lex.lex()
lexer.input(code)

print("Tokenization Part:")
while True:
    token = lexer.token()
    if not token:
        break
    print(token)

# Parser

def p_statement(p):
    'statement : assignment'
    p[0] = p[1]

def p_assignment(p):
    'assignment : ID EQUAL table'
    p[0] = ('assign', p[1], p[3])

def p_table(p):
    '''table : LBRACE fields RBRACE
             | LBRACE RBRACE'''
    if len(p) == 4:
        p[0] = ('table', p[2])
    else:
        p[0] = ('table', [])

def p_fields_multi(p):
    'fields : fields COMMA field'
    p[0] = p[1] + [p[3]]

def p_fields_single(p):
    'fields : field'
    p[0] = [p[1]]

def p_field(p):
    '''field : ID EQUAL value
             | LBRACKET value RBRACKET EQUAL value'''
    if len(p) == 4:
        p[0] = (p[1], p[3])
    else:
        p[0] = (p[2], p[5])

def p_value(p):
    '''value : NUMBER
             | ID
             | table'''
    p[0] = p[1]

# Error handler
def p_error(p):
    if p:
        print(f"Syntax error at token '{p.type}' with value '{p.value}' (line unknown)")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

print("\nParser Part:")
try:
    result = parser.parse(code)
    if result:
        print("Parsed successfully:")
        print(result)
    else:
        print("Parsing failed: Invalid syntax or empty parse result")
except Exception as e:
    print("Parsing failed with error:", e)