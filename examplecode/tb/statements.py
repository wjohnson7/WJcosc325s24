class Statement:
    def __init__(self, linenumber):
        self._linenumber = linenumber
        self._tokens = []

    def addtoken(self, token):
        self._tokens.append(token)

    def execute(self):
        print("ERROR: statement.execute() never should have been called")

class PrintStatement(Statement):
    def __init__(self, linenumber):
        Statement.__init__(self, linenumber)

    def execute(self):
        print("Called print execute")
    