# PART 2 solution - recursive descent top-down parser by hand
from lexicalanalysis import build_the_lexer

lexer = build_the_lexer()

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
  'program : actual_statement | program actual_statement'
  print("yay, valid program")

def p_actual_statement(p):
  'actual_statement : NUMBER statement NEWLINE'
  statements += [{"num":p[1].value, "p":p}]

def p_statement(p):
  ' statement : print | if | goto | gosub | input | let | rem | return | end '
  pass

def p_print(p):
  ' print : PRINT expr_list | PR expr_list'
  print(p[1])

def p_if(p):
  ' if : IF expression RELOP expression THEN statement '
  pass

def p_goto(p):
  ' goto : GOTO NUMBER '
  pass

def p_gosub(p):
  ' gosub : GOSUB NUMBER '
  pass

def p_input(p):
  ' input : INPUT var_list '
  for varname in p[1]:
    symboltable[varname] = input("?")

def p_let(p):
  ' let : LET VAR EQUALS expression'
  pass

def p_rem(p):
  ' rem : REM'
  pass

def p_return(p):
  ' return : RETURN'
  pass

def p_end(p):
  ' end : END'
  pass

# Assuming 'expression' and 'string' rules are already defined elsewhere in your parser
# You might have rules for expression like:
# def p_expression(p):
#     '''
#     expression : term PLUS term
#                | term MINUS term
#                ...
#     '''
#     # Implementation here
#
# And for string, you could directly use the STRING token from the lexer
# Assuming STRING tokens are handled in the lexer to match string literals

def p_expr_list(p):
    '''
    expr_list : expr_item expr_list_tail
    '''
    # Assuming you're building some form of AST or evaluation, you could append or extend
    p[0] = [p[1]] + p[2]

def p_expr_list_tail(p):
    '''
    expr_list_tail : comma_or_semi expr_item expr_list_tail
                   | 
    '''
    if len(p) == 1:  # The empty rule
        p[0] = []
    else:
        p[0] = [p[2]] + p[3]

def p_comma_or_semi(p):
    '''
    comma_or_semi : COMMA
                  | SEMICOLON
    '''
    # This rule just recognizes commas or semicolons. You might not need to do anything with it.

def p_expr_item(p):
    '''
    expr_item : STRING
              | expression
    '''
    # Here, you would handle the logic for what constitutes an expr_item, possibly building a part of an AST
    p[0] = p[1]

# Assuming your lexer has tokens for COMMA, SEMICOLON, STRING, and all tokens needed by 'expression'



