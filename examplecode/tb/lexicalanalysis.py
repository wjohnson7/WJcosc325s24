import ply.lex as lex

# -----------------------------------------------------------------------------
# tiny basic tokenizer
#
# -----------------------------------------------------------------------------

tokens = (
    'VAR','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',
    'COMMA','SEMICOLON','LESS','GREATER',
    'PRINT', 'INPUT', 'LET', 'GOTO', 'GOSUB', 'IF', 'REM', 'END', 'RETURN',
    'STRING'
    )

# Tokens

t_VAR    = r'[A-Z]'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA = r','
t_SEMICOLON = r';'
t_LESS = r'<'
t_GREATER = r'>'
t_PRINT = r'PRINT|PR'
t_INPUT = r'INPUT'
t_LET = r'LET'
t_GOTO = r'GOTO'
t_GOSUB = r'GOSUB'
t_IF = r'IF'
t_REM = r'REM'
t_END = r'END'
t_RETURN = r'RETURN'
t_STRING = r'"(^["])*"'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
sampletb = open("hexdump.tb", "r")
#lexer.input("A=3\nB=4\nPRINT A+B")
lexer.input(sampletb.read())
# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)

  






















