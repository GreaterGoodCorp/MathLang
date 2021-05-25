from rply import ParserGenerator

from Grapher.Core import Lexer
from Grapher.Core.nodes import *


class Parser:
    def __init__(self, tokens):
        self.pg = ParserGenerator(tokens)
        self.symbol_table = []
        self.populate_symbol_table()
        self.make_production()
        self.parser = self.pg.build()

    def populate_symbol_table(self):
        # Implicit x
        self.symbol_table.append("x")

    def make_production(self):
        @self.pg.production("prog : stmts")
        def program(p):
            return Program(p[0])

        @self.pg.production("stmts : stmt")
        @self.pg.production("stmts : stmts stmt")
        def single_statement(p):
            if len(p) == 1:
                return [p[0]]
            return p[0] + [p[1]]

        @self.pg.production("stmt : compound_stmt")
        @self.pg.production("stmt : simple_stmt SEMICOLON")
        def statement(p):
            return p[0]

        @self.pg.production("simple_stmt : assignment")
        @self.pg.production("simple_stmt : print_stmt")
        @self.pg.production("simple_stmt : plot_stmt")
        @self.pg.production("simple_stmt : input_stmt")
        def simple_statement(p):
            return p[0]

        @self.pg.production("compound_stmt : if_stmt")
        @self.pg.production("compound_stmt : while_stmt")
        def compound_statement(p):
            return p[0]

        @self.pg.production("assignment : ID EQUAL expr")
        def assignment(p):
            if len(p) == 3:
                if p[0].value not in self.symbol_table:
                    self.symbol_table.append(p[0].value)
                return Assignment(p[0].value, p[2])

        @self.pg.production("print_stmt : PRINT expr")
        def print_statement(p):
            return Print(p[1])

        @self.pg.production("plot_stmt : PLOT expr")
        def plot_statement(p):
            return Plot(p[1])

        @self.pg.production("input_stmt : INPUT MORE ID")
        @self.pg.production("input_stmt : INPUT str_expr MORE ID")
        def input_statement(p):
            if len(p) == 3:
                if p[2].value not in self.symbol_table:
                    self.symbol_table.append(p[2].value)
                return Input(p[2].value, None)
            else:
                if p[3].value not in self.symbol_table:
                    self.symbol_table.append(p[3].value)
                return Input(p[3].value, p[1])

        @self.pg.production("if_stmt : IF LPAREN expr RPAREN block")
        @self.pg.production("if_stmt : IF LPAREN expr RPAREN block ELSE block")
        def if_statement(p):
            if len(p) == 5:
                return If(p[2], p[4], None)
            return If(p[2], p[4], p[6])

        @self.pg.production("while_stmt : WHILE LPAREN expr RPAREN block")
        def while_stmt(p):
            return While(p[2], p[4])

        @self.pg.production("expr : str_expr")
        @self.pg.production("expr : bool_expr")
        @self.pg.production("expr : solve_expr")
        @self.pg.production("expr : math_expr")
        @self.pg.production("expr : expr AS num_type")
        def expression(p):
            if len(p) == 1:
                return p[0]
            else:
                return Cast(p[0], p[2])

        @self.pg.production("str_expr : str_term")
        @self.pg.production("str_expr : str_expr PLUS str_term")
        @self.pg.production("str_expr : str_expr COMMA str_term")
        def string_expression(p):
            if len(p) == 1:
                return p[0]
            elif p[1].name == "PLUS":
                return StringAdd(p[0], p[2], False)
            else:
                return StringAdd(p[0], p[2], True)

        @self.pg.production("str_term : STRING_LITERAL")
        @self.pg.production("str_term : expr AS STRING")
        def string_term(p):
            if len(p) == 1:
                return p[0].value
            return Cast(p[0], p[2].value)

        @self.pg.production("bool_expr : math_expr EQUALITY math_expr")
        @self.pg.production("bool_expr : math_expr LEQ math_expr")
        @self.pg.production("bool_expr : math_expr GEQ math_expr")
        @self.pg.production("bool_expr : math_expr LESS math_expr")
        @self.pg.production("bool_expr : math_expr MORE math_expr")
        def bool_expression(p):
            return Comparison(p[0], p[1].value, p[2])

        @self.pg.production("solve_expr : SOLVE math_expr")
        @self.pg.production("solve_expr : SOLVE math_expr AS num_type")
        def solve_statement(p):
            if len(p) == 2:
                return Solve(p[1], None)
            return Solve(p[1], p[3])

        @self.pg.production("math_expr : math_term")
        @self.pg.production("math_expr : math_expr PLUS math_term")
        @self.pg.production("math_expr : math_expr MINUS math_term")
        def math_expression(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinaryOps(p[0], p[1].value, p[2])

        @self.pg.production("math_term : math_factor")
        @self.pg.production("math_term : math_term TIMES math_factor")
        @self.pg.production("math_term : math_term DIVIDE math_factor")
        def term(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinaryOps(p[0], p[1].value, p[2])

        @self.pg.production("math_factor : power")
        @self.pg.production("math_factor : PLUS math_factor")
        @self.pg.production("math_factor : MINUS math_factor")
        def factor(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinaryOps(0, p[0].value, p[1])

        @self.pg.production("power : primary")
        @self.pg.production("power : primary CARAT math_factor")
        def power(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinaryOps(p[0], p[1].value, p[2])

        @self.pg.production("primary : ID")
        @self.pg.production("primary : NUMBER")
        @self.pg.production("primary : group")
        @self.pg.production("primary : primary group")
        def primary(p):
            if hasattr(p[0], "value"):
                return p[0].value
            elif len(p) == 2:
                return Evaluation(p[0], p[1])
            return p[0]

        @self.pg.production("group : LPAREN expr RPAREN")
        def group(p):
            return p[1]

        @self.pg.production("block : stmt")
        @self.pg.production("block : LCURLY stmts RCURLY")
        def block(p):
            if len(p) == 1:
                return [p[0]]
            return p[1]

        @self.pg.production("num_type : INTEGER")
        @self.pg.production("num_type : REAL")
        def num_type(p):
            return p[0].value

        @self.pg.error
        def error_handle(token):
            raise InvalidToken(token)

    def parse(self, tokens):
        return self.parser.parse(tokens)


def generate_ast(source):
    lexer = Lexer()
    parser = Parser(lexer.tokens)
    ast = parser.parse(lexer.lex(source))
    populate_matching_table(parser.symbol_table)
    return ast
