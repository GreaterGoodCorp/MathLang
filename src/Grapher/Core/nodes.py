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

    @staticmethod
    def init_code():
        return "import sympy as _sp;_p=print;_i=input;x=_sp.Symbol(\"x\");"

    def translate(self):
        code = Program.init_code()
        for stmt in self.stmts:
            if isinstance(stmt, (If, While)):
                code += "\n" + stmt.translate()
                continue
            code += stmt.codify()
        return code


class Assignment:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def codify(self):
        while type(self.expr) != str:
            self.expr = self.expr.codify()
        return f"{get_symbol(self.name)}={self.expr};"


class Evaluation:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr


class Print:
    def __init__(self, expr):
        self.expr = expr

    def codify(self):
        while type(self.expr) != str:
            self.expr = self.expr.codify()
        return f"_p({self.expr});"


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

    def codify(self):
        return f"{get_symbol(self.name)}=_i({self.prompt});"


class If:
    def __init__(self, condition, true_block, false_block):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def translate(self):
        code = f"if {self.condition.codify()}:\n\t"
        for stmt in self.true_block:
            if isinstance(stmt, (If, While)):
                code += stmt.translate()
                continue
            code += stmt.codify()
        if self.false_block is None:
            return code
        code += "\nelse:\n\t"
        for stmt in self.false_block:
            if isinstance(stmt, (If, While)):
                code += stmt.translate()
                continue
            code += stmt.codify()
        return code


class While:
    def __init__(self, condition, code_block):
        self.condition = condition
        self.code_block = code_block

    def translate(self):
        code = f"if {self.condition.codify()}:\n\t"
        for stmt in self.code_block:
            if isinstance(stmt, (If, While)):
                code += stmt.translate()
                continue
            code += stmt.codify()
        return code


class BinaryOps:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def codify(self):
        while type(self.left) != str:
            self.left = self.left.codify()
        while type(self.right) != str:
            self.right = self.right.codify()
        if self.left in global_symbol_match:
            self.left = get_symbol(self.left)
        if self.right in global_symbol_match:
            self.right = get_symbol(self.right)
        self.op = "**" if self.op == "^" else self.op
        return str(sympify(f"({self.left}){self.op}({self.right})"))


class Comparison:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def codify(self):
        while type(self.left) != str:
            self.left = self.left.codify()
        while type(self.right) != str:
            self.right = self.right.codify()
        if self.left in global_symbol_match:
            self.left = get_symbol(self.left)
        if self.right in global_symbol_match:
            self.right = get_symbol(self.right)
        return f"{self.left}{self.op}{self.right}"


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


def generate_python_code(ast):
    return ast.translate()
