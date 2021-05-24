from sympy import sympify

global_symbol_match = list()


def populate_matching_table(table):
    global global_symbol_match
    global_symbol_match = table


def get_symbol(symbol):
    if symbol in global_symbol_match:
        return f"_{global_symbol_match.index(symbol)}"
    global_symbol_match.append(symbol)
    return f"_{len(global_symbol_match) - 1}"


class Program:
    def __init__(self, stmts):
        self.stmts = stmts


class Assignment:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class Evaluation:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class Print:
    def __init__(self, expr):
        self.expr = expr


class Plot:
    def __init__(self, expr, domain):
        self.expr = expr
        self.domain = domain


class Solve:
    def __init__(self, expr, domain):
        self.expr = expr
        self.domain = domain


class Input:
    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt


class If:
    def __init__(self, condition, true_block, false_block):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block


class While:
    def __init__(self, condition, code_block):
        self.condition = condition
        self.code_block = code_block


class BinaryOps:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Comparison:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class InvalidToken(BaseException):
    def __init__(self, token, *args):
        self.token = token
        super().__init__(*args)

    def __str__(self):
        return f"Invalid token: '{self.token.value}' at line {self.token.source_pos.lineno}"


class UndefinedName(BaseException):
    def __init__(self, token, *args):
        self.token = token
        super().__init__(*args)

    def __str__(self):
        return f"Undefined name '{self.token.value}' at line {self.token.source_pos.lineno}"
