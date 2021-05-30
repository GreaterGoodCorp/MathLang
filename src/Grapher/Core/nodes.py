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


def get_str(obj):
    while True:
        if isinstance(obj, AST):
            obj = obj.codify()
        elif obj in global_symbol_match:
            return get_symbol(obj)
        else:
            return obj


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
        return f"{get_str(self.name)}={get_str(self.expr)};"

    def serialise(self):
        return {"type": "Assignment", "params": {"name": self.name, "expr": self.expr}}


class Evaluation(AST):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def codify(self):
        return get_str(self.name) + ".subs({'x':" + str(sympy.sympify(get_str(self.expr))).replace(' ', '') + "})"

    def serialise(self):
        return {"type": "Evaluation", "params": {"name": self.name, "expr": self.expr}}


class Print(AST):
    def __init__(self, args):
        self.args = args

    def codify(self):
        self.args = list(map(get_str, self.args))
        return f"_p({','.join(self.args)});"

    def serialise(self):
        return {"type": "Print", "params": {"args": self.args}}


class Plot(AST):
    def __init__(self, args):
        self.args = args

    def codify(self):
        self.args = list(map(get_str, self.args))
        code = f"_s.plot({','.join(self.args)});"
        return code

    def serialise(self):
        return {"type": "Plot", "params": {"args": self.args}}


class Solve(AST):
    def __init__(self, expr, domain):
        self.expr = expr
        self.domain = domain

    def codify(self):
        domain_map = {
            "INTEGER": "_s.Integers",
            "REAL": "_s.Reals",
        }
        return f"list(_s.solveset({get_str(self.expr)},domain={domain_map.get(get_str(self.domain), '_s.Reals')}))"

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
        return f"{get_str(self.name)}={input_call};"

    def serialise(self):
        return {"type": "Input", "params": {"name": self.name, "prompt": self.prompt}}


class BinaryOps(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def codify(self):
        self.op = "**" if self.op == "^" else self.op
        return str(sympy.sympify(f"({get_str(self.left)}){self.op}({get_str(self.right)})")).replace(" ", "")

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
