# Example Lua code:
code = ''' function add(a, b) c = a + b end '''

import ply.lex as lex
import ply.yacc as yacc

# Lexer

tokens = (
    'FUNCTION',
    'END',
    'ID',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'ASSIGN',
    'PLUS'
)

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_ASSIGN = r'='
t_PLUS = r'\+'
t_ID = r'[a-zA-Z_]\w*'

t_ignore = ' \t\n'

def t_FUNCTION(t):
    r'function'
    return t

def t_END(t):
    r'end'
    return t

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
    '''statement : function_def
                 | assignment'''
    p[0] = p[1]

def p_function_def(p):
    'function_def : FUNCTION ID LPAREN params RPAREN statements END'
    p[0] = ('function', p[2], p[4], p[6])

def p_params_multi(p):
    'params : params COMMA ID'
    p[0] = p[1] + [p[3]]

def p_params_single(p):
    'params : ID'
    p[0] = [p[1]]

def p_params_empty(p):
    'params :'
    p[0] = []

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_assignment(p):
    'assignment : ID ASSIGN expr'
    p[0] = ('assign', p[1], p[3])

def p_expr(p):
    '''expr : ID
            | expr PLUS expr'''
    if len(p) == 4:
        p[0] = ('+', p[1], p[3])
    else:
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