from rply import ParserGenerator

from MathLang.Core import Lexer
from MathLang.Core.nodes import *


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

        @self.pg.production("stmts : stmt_semicolon")
        @self.pg.production("stmts : stmts stmt_semicolon")
        def single_statement(p):
            if len(p) == 1:
                return [p[0]]
            return p[0] + [p[1]]

        @self.pg.production("stmt_semicolon : stmt SEMICOLON")
        def statement(p):
            return p[0]

        @self.pg.production("stmt : assignment")
        @self.pg.production("stmt : print_stmt")
        @self.pg.production("stmt : plot_stmt")
        def simple_statement(p):
            return p[0]

        @self.pg.production("assignment : ID EQUAL expr")
        def assignment(p):
            if p[0].value not in self.symbol_table:
                self.symbol_table.append(p[0].value)
            return Assignment(p[0].value, p[2])

        @self.pg.production("print_stmt : PRINT expr")
        @self.pg.production("print_stmt : print_stmt COMMA expr")
        def print_statement(p):
            if len(p) == 2:
                return Print([p[1]])
            else:
                return Print(p[0].args + [p[2]])

        @self.pg.production("plot_stmt : PLOT expr")
        @self.pg.production("plot_stmt : plot_stmt COMMA expr")
        def plot_statement(p):
            if len(p) == 2:
                return Plot([p[1]])
            else:
                return Plot(p[0].args + [p[2]])

        @self.pg.production("expr : m_expr")
        @self.pg.production("expr : solve_expr")
        def expression(p):
            return p[0]

        @self.pg.production("solve_expr : SOLVE ID IN set")
        def solve_statement(p):
            return Solve(p[1].value, p[3])

        @self.pg.production("set : REAL")
        @self.pg.production("set : RATIONAL")
        @self.pg.production("set : INTEGER")
        def num_set(p):
            return p[0].value

        @self.pg.production("m_expr : sum")
        @self.pg.production("m_expr : m_expr EQ sum")
        @self.pg.production("m_expr : m_expr NEQ sum")
        @self.pg.production("m_expr : m_expr LTE sum")
        @self.pg.production("m_expr : m_expr LT sum")
        @self.pg.production("m_expr : m_expr GTE sum")
        @self.pg.production("m_expr : m_expr GT sum")
        def bool_expression(p):
            if len(p) == 1:
                return p[0]
            return Comparison(p[0], p[1].value, p[2])

        @self.pg.production("sum : term")
        @self.pg.production("sum : sum PLUS term")
        @self.pg.production("sum : sum MINUS term")
        def math_expression(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinaryOps(p[0], p[1].value, p[2])

        @self.pg.production("term : factor")
        @self.pg.production("term : term TIMES factor")
        @self.pg.production("term : term DIVIDE factor")
        def term(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinaryOps(p[0], p[1].value, p[2])

        @self.pg.production("factor : power")
        @self.pg.production("factor : PLUS factor")
        @self.pg.production("factor : MINUS factor")
        def factor(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinaryOps(0, p[0].value, p[1])

        @self.pg.production("power : primary")
        @self.pg.production("power : primary CARAT factor")
        def power(p):
            if len(p) == 1:
                return p[0]
            else:
                return BinaryOps(p[0], p[1].value, p[2])

        @self.pg.production("primary : atom")
        @self.pg.production("primary : func_eval")
        def primary(p):
            return p[0]

        @self.pg.production("atom : ID")
        @self.pg.production("atom : NUMBER")
        @self.pg.production("atom : group")
        def atom(p):
            try:
                return p[0].value
            except AttributeError:
                return p[0]

        @self.pg.production("func_eval : ID group")
        def func_eval(p):
            return Evaluation(p[0].value, p[1])

        @self.pg.production("group : LPAREN expr RPAREN")
        def group(p):
            return p[1]

        @self.pg.error
        def error_handle(token):
            raise InvalidToken(token)

    def parse(self, tokens):
        """Parses the token stream into MathLang AST. Please do not call this function directly, use 'generate_ast()'
        instead for AST generation.
        """
        return self.parser.parse(tokens)


def generate_ast(source: str) -> AST:
    """Generates MathLang AST from MathLang source code.

    :param source: MathLang source code.
    :type source: str
    :return: MathLang AST.
    :rtype: str
    """
    lexer = Lexer()
    parser = Parser(lexer.tokens)
    ast = parser.parse(lexer.lex(source))
    populate_matching_table(parser.symbol_table)
    return ast
