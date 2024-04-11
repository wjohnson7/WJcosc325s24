class ASTNode:
    def execute(self):
        raise NotImplementedError("Execute method must be implemented by subclasses.")
    
class PrintStatement(ASTNode):
    def __init__(self, expressions):
        self.expressions = expressions  # List of expressions to print

    def execute(self):
        # Execution logic to evaluate expressions and print them
        output = ' '.join(str(expr.evaluate()) for expr in self.expressions)
        print(output)

class IfStatement(ASTNode):
    def __init__(self, left_expr, operator, right_expr, statement):
        self.left_expr = left_expr
        self.operator = operator
        self.right_expr = right_expr
        self.statement = statement

    def execute(self):
        # Evaluate condition
        if self.operator.evaluate(self.left_expr, self.right_expr):
            self.statement.execute()

class GotoStatement(ASTNode):
    def __init__(self, line_number):
        self.line_number = line_number

    def execute(self):
        # Logic to jump to another line in the program (handled by control flow manager)
        control_flow.jump(self.line_number.evaluate())

class InputStatement(ASTNode):
    def __init__(self, variables):
        self.variables = variables  # List of variables to input

    def execute(self):
        for var in self.variables:
            var.set_value(input(f"Enter value for {var.name}: "))

class LetStatement(ASTNode):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression

    def execute(self):
        # Evaluate expression and assign to variable
        self.variable.set_value(self.expression.evaluate())

class GosubStatement(ASTNode):
    def __init__(self, line_number):
        self.line_number = line_number

    def execute(self):
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
        # Logic to return from a subroutine (handled by control flow manager)
        control_flow.return_from_subroutine()

class EndStatement(ASTNode):
    def execute(self):
        # Logic to end the program execution
        control_flow.end_program()

class ExpressionList(ASTNode):
    def __init__(self, expressions):
        self.expressions = expressions  # List of Expression or String

    def evaluate(self):
        return [expr.evaluate() for expr in self.expressions]

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

class Factor(ASTNode):
    def __init__(self, value):
        self.value = value  # Can be Var, Number, Expression, or FunctionCall

    def evaluate(self):
        return self.value.evaluate()

class FunctionCall(ASTNode):
    def __init__(self, function_name, args):
        self.function_name = function_name
        self.args = args  # ExpressionList

    def evaluate(self):
        if self.function_name == 'RND':
            return random.choice(self.args.evaluate())
        elif self.function_name == 'USR':
            # Implementation depends on what USR is supposed to do
            pass
