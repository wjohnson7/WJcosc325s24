import random
import controlflow

# control execution including support for GOTO, GOSUB
control_flow = controlflow.ControlFlow()

# symbol table for all the vars
symbol_table = {}

class ASTNode:
    def execute(self):
        raise NotImplementedError("Execute method must be implemented by subclasses.")
    
class PrintStatement(ASTNode):
    def __init__(self, expressions):
        self.expressions = expressions  # List of expressions to print

    def execute(self):
        # Execution logic to evaluate expressions and print them
        for expr in self.expressions.evaluate():
            print(expr)

class IfStatement(ASTNode):
    def __init__(self, left_expr, operator, right_expr, statement):
        self.left_expr = left_expr
        self.operator = operator
        self.right_expr = right_expr
        self.statement = statement

    def execute(self):
        # Evaluate condition ... demorgan to the extreme
        if self.operator == "=":
            if self.left_expr.evaluate() != self.right_expr.evaluate():
                return
        elif self.operator == "<":
            if self.left_expr.evaluate() >= self.right_expr.evaluate():
                return
        elif self.operator == ">":
            if self.left_expr.evaluate() <= self.right_expr.evaluate():
                return
        elif self.operator == ">=":
            if self.left_expr.evaluate() < self.right_expr.evaluate():
                return
        elif self.operator == "<=":
            if self.left_expr.evaluate() > self.right_expr.evaluate():
                return
        elif self.operator == "<>":
            if self.left_expr.evaluate() == self.right_expr.evaluate():
                return
        else:
            raise ValueError(f"Invalid operator: {self.operator}")  
        self.statement.execute()

class GotoStatement(ASTNode):
    def __init__(self, line_number):
        self.line_number = line_number

    def execute(self):
        global control_flow
        # Logic to jump to another line in the program (handled by control flow manager)
        control_flow.jump(self.line_number.evaluate())

class InputStatement(ASTNode):
    def __init__(self, varlist):
        self.varlist = varlist  # List of variables to input

    def execute(self):
        global symbol_table
        for var in self.varlist.variables:
            symbol_table[var] = int(input(f"Enter value for {var}: "))

class LetStatement(ASTNode):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def execute(self):
        # Evaluate expression and assign to variable
        global symbol_table
        symbol_table[self.variable] = self.expression.evaluate()

class GosubStatement(ASTNode):
    def __init__(self, line_number):
        self.line_number = line_number

    def execute(self):
        global control_flow
        # Similar to GOTO but needs to remember return address
        control_flow.call_subroutine(self.line_number.evaluate())

class RemStatement(ASTNode):
    def __init__(self, comment):
        self.comment = comment  # REM statement is essentially a comment

    def execute(self):
        # REM statements do not perform any operation during execution
        pass

class ReturnStatement(ASTNode):
    def execute(self):
        global control_flow
        # Logic to return from a subroutine (handled by control flow manager)
        control_flow.return_from_subroutine()

class EndStatement(ASTNode):
    def execute(self):
        global control_flow
        # Logic to end the program execution
        control_flow.end_program()

class ExpressionList(ASTNode):
    def __init__(self, expressions):
        self.expressions = expressions  # List of Expression or String

    def evaluate(self):
        return [expr.evaluate() if not isinstance(expr, str) else expr for expr in self.expressions]

class VarList(ASTNode):
    def __init__(self, variables):
        self.variables = variables  # List of Var instances

    def execute(self):
        # Typically used for input, so might not directly evaluate here
        pass

class Expression(ASTNode):
    def __init__(self, terms, operators):
        self.terms = terms  # List of Term instances
        self.operators = operators  # List of '+' or '-' between terms

    def evaluate(self):
        result = self.terms[0].evaluate()
        for op, term in zip(self.operators, self.terms[1:]):
            if op == '+':
                result += term.evaluate()
            elif op == '-':
                result -= term.evaluate()
        return result

class UnaryExpression:
    def __init__(self, operand, operator):
        """
        Initialize a UnaryExpression.

        :param operand: The operand (expression) to which the unary operator is applied.
        :param operator: A string representing the unary operator ('+' or '-').
        """
        self.operand = operand
        self.operator = operator

    def evaluate(self):
        """
        Evaluate the unary expression based on the operator and operand.

        Returns the result of applying the unary operator to the operand.
        """
        if self.operator == '+':
            return +self.operand.evaluate()  # Unary plus (generally redundant)
        elif self.operator == '-':
            return -self.operand.evaluate()  # Unary minus (negation)

    def __str__(self):
        """
        Return a string representation of the unary expression for debugging.
        """
        return f"{self.operator}{self.operand}"

class Term(ASTNode):
    def __init__(self, factors, operators):
        self.factors = factors  # List of Factor instances
        self.operators = operators  # List of '*' or '/' between factors

    def evaluate(self):
        result = self.factors[0].evaluate()
        for op, factor in zip(self.operators, self.factors[1:]):
            if op == '*':
                result *= factor.evaluate()
            elif op == '/':
                result /= factor.evaluate()
        return result

def is_numeric(value):
    return isinstance(value, (int, float, complex))

class Factor(ASTNode):
    def __init__(self, value):
        self.value = value  # Can be Var, Number, Expression, or FunctionCall

    def evaluate(self):
        global symbol_table
        if is_numeric(self.value):
            return self.value
        elif isinstance(self.value, str):
            return symbol_table[self.value] if self.value in symbol_table else 0
        else:
            return self.value.evaluate()

class FunctionCall(ASTNode):
    def __init__(self, function_name, args):
        self.function_name = function_name
        self.args = args  # ExpressionList

    def evaluate(self):
        if self.function_name == 'RND':
            return random.randint(0, self.args.evaluate()[0])
        elif self.function_name == 'USR':
            # Implementation depends on what USR is supposed to do
            return 0

def run_program(program):
    control_flow.load_program(program)
    control_flow.run_program()