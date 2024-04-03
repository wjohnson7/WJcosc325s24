# PART 2 solution - recursive descent top-down parser by hand
from lexicalanalysis import build_the_lexer

lexer = build_the_lexer()

# define all the non terminal parsing functions
def tokerror(tok, exp):
  print(f"Unexpected token found: {tok.type}, Expecting: {exp}")
  print("INVALID")
  exit(1)

