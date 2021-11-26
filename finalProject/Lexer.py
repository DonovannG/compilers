import ply.lex as lex

literals = ['=', '+', '-', '*', '/', '(', ')','"', ';','<','>','{','}','!']
reserved = { 
    'int' : 'INTDEC',
    'float' : 'FLOATDEC',
    'print' : 'PRINT',
    'boolean' : 'BOOLDEC',
    'string' : 'STRINGDEC',
    'and' : 'AND',
    'or' : 'OR',
    'if' : 'IF',
    'elif' : 'ELIF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR'
 }

tokens = [
    'INUMBER', 'FNUMBER', 'NAME', 'STRING', 'BOOLEAN'
] + list(reserved.values())


# Tokens

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')     
    return t

def t_FNUMBER(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'".*"'
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_BOOLEAN(t):
    r'false | true'


# Build the lexer
lexer = lex.lex()
