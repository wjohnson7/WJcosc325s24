import myast

# -----------------------------------------------------------------------------
# tiny basic tokenizer
#
# -----------------------------------------------------------------------------

tokens = (
    'NEWLINE',
    'NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',
    'COMMA','SEMICOLON',
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
t_RELOP = r'<>|<=|>=|<|>'

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


def p_program(p):
    '''program : actual_statement
               | program actual_statement'''
    if len(p) == 2:
        p[0] = [p[1]]  # Start a new list with the first statement
    else:
        p[0] = p[1] + [p[2]]  # Append the new statement to the existing list

def p_actual_statement(p):
    'actual_statement : NUMBER statement NEWLINE'
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
    p[0] = myast.PrintStatement(p[2])

def p_input_statement(p):
    'input_statement : INPUT var_list'
    p[0] = myast.InputStatement(p[2])

def p_if_statement(p):
    '''if_statement : IF expression RELOP expression THEN statement
                    | IF expression EQUALS expression THEN statement'''
    p[0] = myast.IfStatement(p[2], p[3], p[4], p[6])

def p_goto_statement(p):
    'goto_statement : GOTO expression'
    p[0] = myast.GotoStatement(p[2])

def p_let_statement(p):
    'let_statement : LET VAR EQUALS expression'
    p[0] = myast.LetStatement(p[2], p[4])

def p_gosub_statement(p):
    'gosub_statement : GOSUB expression'
    p[0] = myast.GosubStatement(p[2])

def p_rem_statement(p):
    'rem_statement : REM'
    p[0] = myast.RemStatement("")

def p_return_statement(p):
    'return_statement : RETURN'
    p[0] = myast.ReturnStatement()

def p_end_statement(p):
    'end_statement : END'
    p[0] = myast.EndStatement()

def p_expr_list(p):
    '''expr_list : expr_list_item
                 | expr_list COMMA expr_list_item
                 | expr_list SEMICOLON expr_list_item'''
    if len(p) == 2:
        # Start a new list with the first item
        p[0] = myast.ExpressionList([p[1]])
    else:
        # Append the new item to the existing list
        p[1].expressions.append(p[3])
        p[0] = p[1]

def p_expr_list_item(p):
    '''expr_list_item : expression
                      | STRING'''
    p[0] = p[1]

def p_var_list(p):
    '''var_list : VAR
                | var_list COMMA VAR'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = myast.VarList([p[1]])

def p_expression(p):
    '''expression : term
                  | expression PLUS term
                  | expression MINUS term'''
    if len(p) == 4:
        p[0] = myast.Expression([p[1], p[3]], [p[2]])
    else:
        p[0] = p[1]

def p_term(p):
    '''term : factor
            | term TIMES factor
            | term DIVIDE factor'''

    if len(p) == 4:
        p[0] = myast.Term([p[1], p[3]], [p[2]])
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : VAR
              | NUMBER
              | LPAREN expression RPAREN
              | PLUS factor 
              | MINUS factor
              | function'''
    if len(p) == 4:
        p[0] = myast.Factor(p[2])
    elif len(p) == 3:
        # Handle unary operators, assuming you want to transform their effects into the AST structure
        if p[1] == '+':
            p[0] = p[2]  # Unary plus (could be redundant, depends on AST structure)
        elif p[1] == '-':
            # Unary minus needs to negate the factor
            p[0] = myast.UnaryExpression(p[2], operator='-')
    else:
        p[0] = myast.Factor(p[1])

def p_function(p):
    '''function : RND LPAREN expr_list RPAREN
                | USR LPAREN expr_list RPAREN'''
    p[0] = myast.FunctionCall(p[1], p[3])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# initalize the symbol table

import ply.lex as lex
lexer = lex.lex()
thesourcecode = open("examplecode/tbi/random.tb", "r")
import ply.yacc as yacc 
parser = yacc.yacc()
program = parser.parse(thesourcecode.read())
for tuple in program:
    print(tuple)

myast.run_program(program)