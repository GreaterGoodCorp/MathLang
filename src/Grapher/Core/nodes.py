from __future__ import annotations
import abc

import sympy

global_symbol_match = list()
current_indent = 0


def populate_matching_table(table):
    global global_symbol_match
    global_symbol_match = table


def get_symbol(symbol):
    if symbol in global_symbol_match:
        return f"_{global_symbol_match.index(symbol)}"
    global_symbol_match.append(symbol)
    return f"_{len(global_symbol_match) - 1}"


def lookup_type(t):
    return {"INTEGER": "int", "REAL": "float", "STRING": "str"}[t]


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
        return f"import sympy as _s;{get_symbol('x')}=_s.Symbol(\"x\")" \
               f";_s.init_printing(pretty_print=True);_p=print;_i=input;"

    @staticmethod
    def finalise_code(code: str):
        return code + "del _s,_p,_i," + ",".join([get_symbol(i) for i in global_symbol_match]) + ";"

    def codify(self):
        code = Program.init_code()
        for stmt in self.stmts:
            code += str(stmt.codify())
        return Program.finalise_code(code.strip("\n\t"))

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
        if self.expr in global_symbol_match:
            self.expr = get_symbol(self.expr)
        return get_symbol(self.name) + ".subs({'x':" + str(sympy.sympify(self.expr)).replace(' ', '') + "})"

    def serialise(self):
        return {"type": "Evaluation", "params": {"name": self.name, "expr": self.expr}}


class Print(AST):
    def __init__(self, args):
        self.args = args

    def codify(self):
        while type(self.expr) != str and self.expr is not None:
            self.expr = self.expr.codify()
        if self.expr in global_symbol_match:
            self.expr = get_symbol(self.expr)
        return f"_p({self.expr});"

    def serialise(self):
        return {"type": "Print", "params": {"expr": self.expr}}


class Plot(AST):
    def __init__(self, args):
        self.args = args

    def codify(self):
        while type(self.expr) != str and self.expr is not None:
            self.expr = self.expr.codify()
        if self.expr in global_symbol_match:
            self.expr = get_symbol(self.expr)
        return f"_s.plot({self.expr});"

    def serialise(self):
        return {"type": "Plot", "params": {"expr": self.expr}}


class Solve(AST):
    def __init__(self, expr, domain):
        self.expr = expr
        self.domain = domain

    def codify(self):
        domain_map = {
            "INTEGER": "_s.Integers",
            "REAL": "_s.Reals",
        }
        if self.expr in global_symbol_match:
            self.expr = get_symbol(self.expr)
        return f"list(_s.solveset({self.expr},domain={domain_map.get(self.expr, '_s.Reals')}))"

    def serialise(self):
        return {"type": "Solve", "params": {"expr": self.expr, "domain": self.domain}}


class Input(AST):
    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt

    def codify(self):
        if self.prompt is not None:
            input_call = f"_i({self.prompt})"
        else:
            input_call = "_i()"
        return f"{get_symbol(self.name)}={input_call};"

    def serialise(self):
        return {"type": "Input", "params": {"name": self.name, "prompt": self.prompt}}


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
        return str(sympy.sympify(f"({self.left}){self.op}({self.right})")).replace(" ", "")

    def serialise(self):
        return {
            "type": "BinaryOps",
            "params": {
                "left": self.left,
                "op": self.op,
                "right": self.right
            }
        }


class StringAdd(AST):
    def __init__(self, left, right, pad):
        self.left = left
        self.right = right
        self.pad = pad

    def codify(self) -> str:
        while type(self.left) != str and self.left is not None:
            self.left = self.left.codify()
        while type(self.right) != str and self.right is not None:
            self.right = self.right.codify()
        if self.left in global_symbol_match:
            self.left = get_symbol(self.left)
        if self.right in global_symbol_match:
            self.right = get_symbol(self.right)
        if self.pad:
            return f"{str(self.left)}+\" \"+{str(self.right)}"
        return f"{str(self.left)}+{str(self.right)}"

    def serialise(self):
        return {
            "type": "StringAdd",
            "params": {
                "left": self.left,
                "right": self.right,
                "pad": self.pad
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


class Cast(AST):
    def __init__(self, expr, cast):
        self.expr = expr
        self.cast = cast

    def codify(self) -> str:
        while type(self.expr) != str and self.expr is not None:
            self.expr = self.expr.codify()
        if self.expr in global_symbol_match:
            self.expr = get_symbol(self.expr)
        return f"{lookup_type(self.cast)}({self.expr})"

    def serialise(self) -> dict:
        return {
            "type": "Cast",
            "params": {
                "expr": self.expr,
                "cast": self.cast,
            }
        }


class InvalidToken(BaseException):
    def __init__(self, token, *args):
        self.token = token
        super().__init__(*args)

    def __str__(self):
        if self.token.name == "$end":
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
