import ply.lex as lex

# -----------------------------------------------------------------------------
# tiny basic tokenizer
#
# -----------------------------------------------------------------------------

tokens = (
    'NEWLINE',
    'NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',
    'COMMA','SEMICOLON','LESS','GREATER',
    'PRINT', 'INPUT', 'LET', 'GOTO', 'GOSUB', 'IF', 'THEN', 'REM', 'END', 'RETURN', 
    'STRING', 'VAR', 'RND', 'USR'
    )

# Tokens

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
t_INPUT = r'\bINPUT\b'
t_LET = r'\bLET\b'
t_GOTO = r'\bGOTO\b'
t_GOSUB = r'\bGOSUB\b'
t_IF = r'\bIF\b'
t_THEN = r'\bTHEN\b'
t_END = r'\bEND\b'
t_RETURN = r'\bRETURN\b'
t_RND = r'\bRND\b'
t_USR = r'\bUSR\b'
t_STRING = r'"([^"])*"'
t_VAR    = r'[A-Z]'

def t_REM(t):
  r'REM([^\n])*'
  return t

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

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
def build_the_lexer():
  lexer = lex.lex()
  return lexer
  






















