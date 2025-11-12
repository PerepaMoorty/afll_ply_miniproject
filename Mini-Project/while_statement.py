# Example Lua code:
code = ''' while x < 10 do x = x + 1 end '''

import ply.lex as lex
import ply.yacc as yacc

# Lexer

tokens = (
    'WHILE',
    'DO',
    'END',
    'ID',
    'NUMBER',
    'OP',
    'ASSIGN',
    'PLUS'
)

t_ID = r'[a-zA-Z_]\w*'
t_OP = r'[<>]=?|==|~='
t_ASSIGN = r'='
t_PLUS = r'\+'
t_NUMBER = r'\d+'

t_ignore = ' \t\n'

def t_WHILE(t):
    r'while'
    return t

def t_DO(t):
    r'do'
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
    '''statement : while_loop
                 | assignment'''
    p[0] = p[1]

def p_while_loop(p):
    'while_loop : WHILE condition DO statements END'
    p[0] = ('while', p[2], p[4])

def p_condition(p):
    'condition : ID OP expr'
    p[0] = (p[1], p[2], p[3])

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_assignment(p):
    'assignment : ID ASSIGN expr'
    p[0] = ('assign', p[1], p[3])

def p_expr(p):
    '''expr : NUMBER
            | ID
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