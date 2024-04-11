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
    'STRING', 'VAR', 'RND', 'USR',
    'RELOP'
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
t_RELOP = r'=|<>|<=|>=|<|>'

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

# define all the non terminal parsing functions
def tokerror(tok, exp):
  print(f"Unexpected token found: {tok.type}, Expecting: {exp}")
  print("INVALID")
  exit(1)

# store all the statements so we can support GOTO and GOSUB
statements = []

# list of return line numbers
returnstack = []

# symbol table for all the vars
symboltable = {}

def p_program(p):
    '''program : actual_statement
               | program actual_statement'''
    if len(p) == 2:
        p[0] = [p[1]]  # Start a new list with the first statement
    else:
        p[0] = p[1] + [p[2]]  # Append the new statement to the existing list

def p_actual_statement(p):
    'actual_statement : number statement CR'
    p[0] = (p[1], p[2])  # Tuple of line number and the statement

def p_statement(p):
    '''statement : print_statement
                 | input_statement
                 | if_statement
                 | goto_statement
                 | let_statement
                 | gosub_statement
                 | rem_statement
                 | return_statement
                 | end_statement'''
    p[0] = p[1]

def p_print_statement(p):
    'print_statement : PRINT expr_list'
    p[0] = PrintStatement(p[2])

def p_input_statement(p):
    'input_statement : INPUT var_list'
    p[0] = InputStatement(p[2])

def p_if_statement(p):
    'if_statement : IF expression RELOP expression THEN statement'
    p[0] = IfStatement(p[2], p[3], p[4], p[6])

def p_goto_statement(p):
    'goto_statement : GOTO expression'
    p[0] = GotoStatement(p[2])

def p_let_statement(p):
    'let_statement : LET var EQUALS expression'
    p[0] = LetStatement(p[2], p[4])

def p_gosub_statement(p):
    'gosub_statement : GOSUB expression'
    p[0] = GosubStatement(p[2])

def p_rem_statement(p):
    'rem_statement : REM'
    p[0] = RemStatement("")

def p_return_statement(p):
    'return_statement : RETURN'
    p[0] = ReturnStatement()

def p_end_statement(p):
    'end_statement : END'
    p[0] = EndStatement()

def p_number(p):
    'number : NUMBER'
    p[0] = p[1]  # Assuming NUMBER is a token returning actual numbers

def p_var(p):
    'var : VAR'
    p[0] = p[1]  # Assuming VAR is a token representing variable names

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")
