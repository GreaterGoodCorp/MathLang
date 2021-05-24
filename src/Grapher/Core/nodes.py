from __future__ import annotations
import abc

from sympy import sympify

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
    return {"INTEGER": "int", "REAL": "float"}[t]


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
        return f"import sympy as _s;_p=print;_i=input;{get_symbol('x')}=_s.Symbol(\"x\");"

    @staticmethod
    def finalise_code(code):
        del_str = "\ndel _s,_p,_i,"
        del_str += ",".join([get_symbol(i) for i in global_symbol_match]) + ";"
        return code + del_str

    def codify(self):
        code = Program.init_code()
        for stmt in self.stmts:
            if isinstance(stmt, (If, While)):
                code += str(stmt.codify())
                continue
            code += str(stmt.codify())
        return Program.finalise_code(code.strip("\n\t"))

    def serialise(self):
        return {"type": "Program", "params": {"stmts": self.stmts}}


class Assignment(AST):
    def __init__(self, name, expr, cast):
        self.name = name
        self.expr = expr
        self.cast = cast

    def codify(self):
        while type(self.expr) != str and self.expr is not None:
            self.expr = self.expr.codify()
        if self.cast is not None:
            self.expr = f"{lookup_type(self.cast)}({self.expr})"
        return f"{get_symbol(self.name)}={self.expr};"

    def serialise(self):
        return {"type": "Assignment", "params": {"name": self.name, "expr": self.expr, "cast": self.cast}}


class Evaluation(AST):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

    def codify(self):
        while type(self.expr) != str and self.expr is not None:
            self.expr = self.expr.codify()
        if self.expr in global_symbol_match:
            self.expr = get_symbol(self.expr)
        d = {"x": str(sympify(self.expr)).replace(" ", "")}
        return f"{get_symbol(self.name)}.subs({str(d)})"

    def serialise(self):
        return {"type": "Evaluation", "params": {"name": self.name, "expr": self.expr}}


class Print(AST):
    def __init__(self, expr):
        self.expr = expr

    def codify(self):
        while type(self.expr) != str and self.expr is not None:
            self.expr = self.expr.codify()
        if self.expr in global_symbol_match:
            self.expr = get_symbol(self.expr)
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
            input_call = f"_i({self.prompt})"
        else:
            input_call = "_i()"
        if self.cast is not None:
            input_call = f"{lookup_type(self.cast)}({input_call})"
        return f"{get_symbol(self.name)}={input_call};"

    def serialise(self):
        return {"type": "Input", "params": {"name": self.name, "prompt": self.prompt, "cast": self.cast}}


class If(AST):
    def __init__(self, condition, true_block, false_block):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def codify(self):
        global current_indent
        flag = True
        newline = "\n" + "\t" * (current_indent + 1)
        code = newline[:-1] + f"if {self.condition.codify()}:"
        for stmt in self.true_block:
            if isinstance(stmt, (If, While)):
                current_indent += 1
                code += str(stmt.codify())
                current_indent -= 1
                flag = False
                continue
            elif flag:
                code += newline
                flag = False
            code += str(stmt.codify())
        if self.false_block is None:
            return code + newline[:-1]
        flag = True
        code += newline[:-1] + "else:"
        for stmt in self.false_block:
            if isinstance(stmt, (If, While)):
                current_indent += 1
                code += str(stmt.codify())
                current_indent -= 1
                flag = False
                continue
            elif flag:
                code += newline
                flag = False
            code += str(stmt.codify())
        return code + newline[:-1]

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
        global current_indent
        newline = "\n" + "\t" * (current_indent + 1)
        flag = True
        code = newline[:-1] + f"while {self.condition.codify()}:" + newline
        for stmt in self.code_block:
            if isinstance(stmt, (If, While)):
                current_indent += 1
                code += str(stmt.codify())
                current_indent -= 1
                flag = False
                continue
            elif flag:
                code += newline
                flag = False
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
        return str(sympify(f"({self.left}){self.op}({self.right})")).replace(" ", "")

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
