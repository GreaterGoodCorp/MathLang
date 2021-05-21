import re

from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def add_token(self, name: str, pattern: str, flag: int = 0):
        # In-sensitive language
        flag |= re.IGNORECASE
        self.lexer.add(name, pattern, flag)

    def initialise_tokens(self):
        # For strings
        self.add_token("STRING", r'(?<=").*(?=")')

        # For reserved keywords
        # 1. Print
        self.add_token("PRINT", r"print")
        # 2. Plot
        self.add_token("PLOT", r"plot")
        # 3. Solve
        self.add_token("SOLVE", r"solve")
        # 4. In
        self.add_token("IN", r"in")

        # For flow controls
        # 1. If
        self.add_token("IF", r"if")
        self.add_token("ENDIF", r"endif")
        # 2. While
        self.add_token("WHILE", r"while")
        self.add_token("ENDWHILE", r"endwhile")

        # For number sets
        sets = ("complexes", "reals", "integers", "naturals")
        self.add_token("SET", r"|".join(sets))

        # For identifiers
        # At most 64 characters
        self.add_token("ID", r"[_a-zA-Z][_a-zA-Z0-9]{0,63}")

        # For numbers
        self.add_token("NUMBER", r"\d+(?:\.\d+)?")

        # For special symbols
        # 1. Parentheses
        self.add_token("LPAREN", r"\(")
        self.add_token("RPAREN", r"\)")
        # 2. Square brackets
        self.add_token("LBRACKET", r"\[")
        self.add_token("RBRACKET", r"\]")
        # 3. Semicolon
        self.add_token("SEMICOLON", r"\;")
        # 4. Newline
        # Works for both Windows, Linux and MacOS
        self.add_token("NEWLINE", r"\r\n|\r|\n")

        # For operators
        # 1. Plus
        self.add_token("PLUS", r"\+")
        # 2. Minus
        self.add_token("MINUS", r"-")
        # 3. Times
        self.add_token("TIMES", r"\*")
        # 4. Divide
        self.add_token("DIVIDE", r"\/")
        # 5. Carat
        self.add_token("CARAT", r"\^")
        # 6. Equal
        self.add_token("EQUAL", r"=")

        # For comparison operators
        self.add_token("LESS", r"<")
        self.add_token("MORE", r">")

        # Ignore spaces and tabs
        self.lexer.ignore(r"\s+")
        self.lexer.ignore(r"\t")

        # Ignore comments
        self.lexer.ignore(r"#.*")

    def get_parser(self):
        self.initialise_tokens()
        return self.lexer.build()
