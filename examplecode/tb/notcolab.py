# PART 2 solution - recursive descent top-down parser by hand
from lexicalanalysis import build_the_lexer
lexer = build_the_lexer()

# define all the non terminal parsing functions
def tokerror(tok, exp):
  print(f"Unexpected token found: {tok.type}, Expecting: {exp}")

def program(tok):
  actual_statement(tok)
  tok = lexer.token()
  while tok != None:
    actual_statement(tok)
    tok = lexer.token()

def actual_statement(tok):
  if tok.type != "NUMBER":
    tokerror(tok, "NUMBER")
  tok = statement(lexer.token())
  if tok.type != "NEWLINE":
    tokerror(tok, "NEWLINE")

def statement(tok):
  # look for a statement
  if tok.type == "PRINT":
    tok = myprint(tok)
  elif tok.type == "INPUT":
    tok = myinput(tok)
  elif tok.type == "LET":
    let(tok)
    tok = lexer.token()
  elif tok.type == "GOTO":
    goto(tok)
    tok = lexer.token()
  elif tok.type == "GOSUB":
    gosub(tok)
    tok = lexer.token()
  elif tok.type == "IF":
    myif(tok)
    tok = lexer.token()
  elif tok.type == "END":
    tok = lexer.token()
  elif tok.type == "RETURN":
    tok = lexer.token()
  elif tok.type == "RND" or tok.type == "USR":
    function(tok)
    tok = lexer.token()
  elif tok.type == "REM":
    tok = lexer.token()
  else:
    tokerror(tok, "PRINT, INPUT, RETURN, END, ...")
  return tok

def function(tok):
  tok = lexer.token()
  # insert your code here

def myif(tok):
  tok = lexer.token()
  # insert your code here

def gosub(tok):
  tok = lexer.token()
  # insert your code here

def goto(tok):
  tok = lexer.token()
  # insert your code here

def let(tok):
  tok = lexer.token()
  # insert your code here

def myinput(tok):
  tok = lexer.token()
  # insert your code here

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
  while tok.type == "COMMA" or tok.type == "SEMICOLON":
    tok = expression(lexer.token())
  return tok

# note that expression MUST make an extra call to lex before it finishes
# so we need to return that token to whoever called expression
def expression(tok):
  if tok.type == "PLUS" or tok.type == "MINUS":
    tok = lexer.token()
  tok = term(tok)
  while tok.type == "PLUS" or tok.type == "MINUS":
    tok = term(lexer.token())
  return tok

def term(tok):
  factor(tok)
  tok = lexer.token()
  while tok.type == "TIMES" or tok.type == "DIVIDE":
    factor(lexer.token())
    tok = lexer.token()
    if tok is None:
      break
    else:
      print("uhoh")
  return tok

def factor(tok):
  if tok.type != "VAR" and tok.type != "NUMBER" and tok.type != "LPAREN":
    tokerror(tok, "VAR, NUMBER, LPAREN")
  if tok.type == "LPAREN":
    tok = lexer.token()
    tok = expression(tok)
    if tok.type != "RPAREN":
      tokerror(tok, "RPAREN")

# now, open a program and parse it
thesourcecode = open("printsonly.tb", "r")
#lexer.input("A=3\nB=4\nPRINT A+B")
lexer.input(thesourcecode.read())
program(lexer.token())