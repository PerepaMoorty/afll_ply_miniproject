# Example Lua code:
code = ''' if x < 5 ;then y = 2 else y = y + 1 end '''

import ply.lex as lex
import ply.yacc as yacc

# Lexer

tokens = (
    'IF',
    'THEN',
    'ELSE',
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

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_THEN(t):
    r'then'
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
    '''statement : if_statement
                 | assignment'''
    p[0] = p[1]

def p_if_statement(p):
    '''if_statement : IF condition THEN statements END
                    | IF condition THEN statements ELSE statements END'''
    if len(p) == 6:
        p[0] = ('if', p[2], p[4])
    else:
        p[0] = ('if-else', p[2], p[4], p[6])

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
