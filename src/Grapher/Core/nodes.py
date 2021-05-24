from __future__ import annotations
import abc

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


class AST(metaclass=abc.ABCMeta):
    """Parent class of all AST nodes."""

    @abc.abstractmethod
    def codify(self) -> str:
        """Turn this node into Python code."""

    @abc.abstractmethod
    def serialise(self) -> dict:
        """Serialise this node in to JSON object."""

    def __eq__(self, other: AST):
        if not isinstance(other, AST):
            raise TypeError("Must be compared with another AST")
        return self.codify() == other.codify()


class Program(AST):
    def __init__(self, stmts):
        self.stmts = stmts

    @staticmethod
    def init_code():
        return f"import sympy as _sp;_p=print;_i=input;{get_symbol('x')}=_sp.Symbol(\"x\");"

    def codify(self):
        code = Program.init_code()
        for stmt in self.stmts:
            if isinstance(stmt, (If, While)):
                code += "\n" + str(stmt.codify())
                continue
            code += str(stmt.codify())
        return code

    def serialise(self):
        return {"type": "Program", "params": {"stmts": self.stmts}}


class Assignment(AST):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def codify(self):
        while type(self.expr) != str and self.expr is not None:
            self.expr = self.expr.codify()
        return f"{get_symbol(self.name)}={self.expr};"

    def serialise(self):
        return {"type": "Assignment", "params": {"name": self.name, "expr": self.expr}}


class Evaluation(AST):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def codify(self):
        while type(self.expr) != str and self.expr is not None:
            self.expr = self.expr.codify()
        d = {"x": sympify(self.expr)}
        return f"{get_symbol(self.name)}.subs({str(d)})"

    def serialise(self):
        return {"type": "Evaluation", "params": {"name": self.name, "expr": self.expr}}


class Print(AST):
    def __init__(self, expr):
        self.expr = expr

    def codify(self):
        while type(self.expr) != str and self.expr is not None:
            self.expr = self.expr.codify()
        return f"_p({self.expr});"

    def serialise(self):
        return {"type": "Print", "params": {"expr": self.expr}}


class Plot(AST):
    def __init__(self, expr, domain):
        self.expr = expr
        self.domain = domain

    def codify(self):
        pass

    def serialise(self):
        return {"type": "Plot", "params": {"expr": self.expr, "domain": self.domain}}


class Solve(AST):
    def __init__(self, expr, domain):
        self.expr = expr
        self.domain = domain

    def codify(self):
        pass

    def serialise(self):
        return {"type": "Solve", "params": {"expr": self.expr, "domain": self.domain}}


class Input(AST):
    def __init__(self, name, prompt, cast):
        self.name = name
        self.prompt = prompt
        self.cast = cast

    def codify(self):
        if self.prompt is not None:
            return f"{get_symbol(self.name)}=_i({self.prompt});"
        return f"{get_symbol(self.name)}=_i();"

    def serialise(self):
        return {"type": "Input", "params": {"name": self.name, "prompt": self.prompt, "cast": self.cast}}


class If(AST):
    def __init__(self, condition, true_block, false_block):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def codify(self):
        code = f"if {self.condition.codify()}:\n\t"
        for stmt in self.true_block:
            if isinstance(stmt, (If, While)):
                code += str(stmt.codify())
                continue
            code += str(stmt.codify())
        if self.false_block is None:
            return code
        code += "\nelse:\n\t"
        for stmt in self.false_block:
            if isinstance(stmt, (If, While)):
                code += str(stmt.codify())
                continue
            code += str(stmt.codify())
        return code

    def serialise(self):
        return {
            "type": "If",
            "params": {
                "condition": self.condition,
                "true_block": self.true_block,
                "false_block": self.false_block
            }
        }


class While(AST):
    def __init__(self, condition, code_block):
        self.condition = condition
        self.code_block = code_block

    def codify(self):
        code = f"if {self.condition.codify()}:\n\t"
        for stmt in self.code_block:
            if isinstance(stmt, (If, While)):
                code += str(stmt.codify())
                continue
            code += str(stmt.codify())
        return code

    def serialise(self):
        return {
            "type": "While",
            "params": {
                "condition": self.condition,
                "code_block": self.code_block
            }
        }


class BinaryOps(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def codify(self):
        while type(self.left) != str and self.left is not None:
            self.left = self.left.codify()
        while type(self.right) != str and self.right is not None:
            self.right = self.right.codify()
        if self.left in global_symbol_match:
            self.left = get_symbol(self.left)
        if self.right in global_symbol_match:
            self.right = get_symbol(self.right)
        self.op = "**" if self.op == "^" else self.op
        return str(sympify(f"({self.left}){self.op}({self.right})"))

    def serialise(self):
        return {
            "type": "BinaryOps",
            "params": {
                "left": self.left,
                "op": self.op,
                "right": self.right
            }
        }


class Comparison(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def codify(self):
        while type(self.left) != str and self.left is not None:
            self.left = self.left.codify()
        while type(self.right) != str and self.right is not None:
            self.right = self.right.codify()
        if self.left in global_symbol_match:
            self.left = get_symbol(self.left)
        if self.right in global_symbol_match:
            self.right = get_symbol(self.right)
        return f"{self.left}{self.op}{self.right}"

    def serialise(self):
        return {
            "type": "Comparison",
            "params": {
                "left": self.left,
                "op": self.op,
                "right": self.right
            }
        }


class InvalidToken(BaseException):
    def __init__(self, token, *args):
        self.token = token
        super().__init__(*args)

    def __str__(self):
        if self.token.type == "$end":
            return "Unexpected EOF"
        return f"Invalid token: '{self.token.value}' at line {self.token.source_pos.lineno}"


class UndefinedName(BaseException):
    def __init__(self, token, *args):
        self.token = token
        super().__init__(*args)

    def __str__(self):
        return f"Undefined name '{self.token.value}' at line {self.token.source_pos.lineno}"


def generate_python_code(ast):
    return ast.codify()
