class Statement:
    def __init__(self, linenumber):
        self._linenumber = linenumber

    def execute(self):
        print("ERROR: statement.execute() never should have been called")

class PrintStatement(Statement):
    def __init__(self, linenumber):
        Statement.__init__(self, linenumber)

    def __str__(self):
        return "print"

    def execute(self):
        pass
    
class InputStatement(Statement):
    def __init__(self, linenumber):
        Statement.__init__(self, linenumber)

    def __str__(self):
        return "input"

    def execute(self):
        pass

class IfStatement(Statement):
    def __init__(self, linenumber):
        Statement.__init__(self, linenumber)

    def __str__(self):
        return "if"

    def execute(self):
        pass

class FunctionStatement(Statement):
    def __init__(self, linenumber):
        Statement.__init__(self, linenumber)

    def __str__(self):
        return "function"

    def execute(self):
        print("Error: this should never be called")

class UsrStatement(FunctionStatement):
    def __init__(self, linenumber):
        Statement.__init__(self, linenumber)

    def __str__(self):
        return "usr function"

    def execute(self):
        pass

class RndStatement(FunctionStatement):
    def __init__(self, linenumber):
        Statement.__init__(self, linenumber)

    def __str__(self):
        return "usr function"

    def execute(self):
        pass

class RemStatement(Statement):
    def __init__(self, linenumber):
        Statement.__init__(self, linenumber)

    def __str__(self):
        return "rem"

    def execute(self):
        pass

class LetStatement(Statement):
    def __init__(self, linenumber):
        Statement.__init__(self, linenumber)

    def __str__(self):
        return "let"

    def execute(self):
        pass