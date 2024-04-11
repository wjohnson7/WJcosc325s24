# PART 2 solution - recursive descent top-down parser by hand
from lexicalanalysis import build_the_lexer
from statements import *

lexer = build_the_lexer()

# define all the non terminal parsing functions
def tokerror(tok, exp):
  print(f"Unexpected token found: {tok.type}, Expecting: {exp} on LINE {tok.lineno}")
  print("INVALID")
  exit(1)

def program(tok):
  actual_statement(tok)
  tok = lexer.token()
  while tok is not None:
    actual_statement(tok)
    tok = lexer.token()
  print(len(statements))
  print("VALID")

def actual_statement(tok):
  if tok.type != "NUMBER":
    tokerror(tok, "NUMBER")
  linenum = tok.value
  tok = statement(lexer.token(), linenum)
  if tok is None:
    print("EOF wihthout a newline character at the end")
    print("INVALID")
    exit(1)
  elif tok.type != "NEWLINE":
    tokerror(tok, "NEWLINE")

# note for all of these different types of statements
# we are creating a global stmt variable that can be referenced whenever we need it 
def statement(tok, linenum):
  # look for a statement
  if tok.type == "PRINT":
    statements.append(PrintStatement(linenum))
    tok = myprint(tok)
  elif tok.type == "INPUT":
    statements.append(InputStatement(linenum))
    tok = myinput(tok)
  elif tok.type == "LET":
    statements.append(LetStatement(linenum))
    tok = let(tok)
  elif tok.type == "GOTO":
    tok = goto(tok)
  elif tok.type == "GOSUB":
    tok = gosub(tok)
  elif tok.type == "IF":
    statements.append(IfStatement(linenum))
    tok = myif(tok, linenum)
  elif tok.type == "END":
    tok = lexer.token()
  elif tok.type == "RETURN":
    tok = lexer.token()
  elif tok.type == "REM":
    statements.append(RemStatement(linenum))
    tok = lexer.token()
  else:
    tokerror(tok, "PRINT, INPUT, RETURN, END, ...")
  return tok

def function(tok):
  tok = lexer.token()
  if tok.type != "LPAREN":
    tokerror(tok, "(")
  tok = expr_list(lexer.token())
  if tok.type != "RPAREN":
    tokerror(tok, ")")

def myif(tok, linenum):
  tok = lexer.token()
  tok = expression(tok)
  tok = relop(tok)
  tok = expression(tok)
  if tok.type != "THEN":
    tokerror(tok,"THEN")
  tok = lexer.token()
  tok = statement(tok, linenum)
  return tok

def relop(tok):
  if tok.type == "LESS":
    tok = lexer.token()
    if tok.type == "GREATER" or tok.type == "EQUALS":
      tok = lexer.token() # grab the nextra token since the token we just "consumed" (i.e., checked) was part of the relop
  elif tok.type == "GREATER":
    tok = lexer.token()
    if tok.type == "LESS" or tok.type == "EQUALS":
      tok = lexer.token() # grab the nextra token since the token we just "consumed" (i.e., checked) was part of the relop
  elif tok.type == "EQUALS":
    tok = lexer.token() # nothing to check for here so we need to grab an extra token in order to return an "extra" token
  else:
    tokerror(tok, "LESS, GREATER, EQUALS")
  return tok

def gosub(tok):
  tok = expression(lexer.token())
  return tok

def goto(tok):
  tok = expression(lexer.token())
  return tok

def let(tok):
  tok = lexer.token()
  if tok.type != "VAR":
    tokerror(tok, "VAR")
  tok = lexer.token()
  if tok.type != "EQUALS":
    tokerror(tok, "EQUALS")
  tok = lexer.token()
  tok = expression(tok)
  return tok  

def myinput(tok):
  tok = var_list(lexer.token())
  return tok

def myprint(tok):
  # no need to check for print token itself again, as that's the only way this function ends up being called
  tok = expr_list(lexer.token())
  return tok

def expr_list(tok):
  # look for an expression list
  if tok.type != "STRING":
    tok = expression(tok)
  else:
    tok = lexer.token()
  while tok is not None and (tok.type == "COMMA" or tok.type == "SEMICOLON"):
    tok = lexer.token()
    if tok.type != "STRING":
      tok = expression(tok)
    else:
      tok = lexer.token()
  return tok

def var_list(tok):
  # look for a var first and ERROR out if we don't have a var
  if tok.type != "VAR":
    tokerror(tok, 'VAR')
  tok = lexer.token()
  while tok is not None and tok.type == "COMMA":
    tok = lexer.token()
    if tok.type != "VAR":
      tokerror(tok, 'VAR')
  return tok

# note that expression MUST make an extra call to lex before it finishes
# so we need to return that token to whoever called expression
def expression(tok):
  if tok.type == "PLUS" or tok.type == "MINUS":
    tok = lexer.token()
  tok = term(tok)
  while tok is not None and (tok.type == "PLUS" or tok.type == "MINUS"):
    tok = term(lexer.token())
  return tok

def term(tok):
  factor(tok)
  tok = lexer.token()
  while tok.type == "TIMES" or tok.type == "DIVIDE":
    factor(lexer.token())
    tok = lexer.token()
    if tok is None or tok.type == "NEWLINE":
      break
  return tok

def factor(tok):
  if tok.type != "RND" and tok.type != "USR" and tok.type != "VAR" and tok.type != "NUMBER" and tok.type != "LPAREN":
    tokerror(tok, "RND, USR, VAR, NUMBER, LPAREN")
  if tok.type == "RND" or tok.type == "USR":
    function(tok)
  if tok.type == "LPAREN":
    tok = lexer.token()
    tok = expression(tok)
    if tok.type != "RPAREN":
      tokerror(tok, "RPAREN")

# now, open a program and parse it
thesourcecode = open("examplecode/tb/ifsonly.tb", "r")
#lexer.input("A=3\nB=4\nPRINT A+B")
lexer.input(thesourcecode.read())
statements = []
program(lexer.token())

# by this point, statements should be fully populated
for stmt in statements:
  print(f"Executing {stmt} at line # {stmt._linenumber}")
  stmt.execute()
