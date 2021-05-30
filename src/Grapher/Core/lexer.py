import re

from rply import LexerGenerator

# This tuple is the master token-pattern pairs list
token_pair = (
    # For reserved keywords
    # 1. Print
    ("PRINT", r"print"),
    # 2. Plot
    ("PLOT", r"plot"),
    # 3. Solve
    ("SOLVE", r"solve"),
    # 5. As
    ("AS", r"as"),
    # 6. Real
    ("REAL", r"REAL"),
    # 7. Integer
    ("INTEGER", r"INTEGER"),
    # 8. String
    ("STRING", r"STRING"),

    # For flow controls
    # 1. If
    ("IF", r"if"),
    ("ELSE", r"else"),
    # 2. While
    ("WHILE", r"while"),

    # For identifiers
    # At most 64 characters
    ("ID", r"[_a-zA-Z][_a-zA-Z0-9]{0,63}"),

    # For numbers
    ("NUMBER", r"\d+(?:\.\d+)?"),

    # For special symbols
    # 1. Parentheses
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    # 2. Curly braces
    ("LCURLY", r"{"),
    ("RCURLY", r"}"),
    # 3. Semicolon
    ("SEMICOLON", r"\;"),
    # 4. Comma
    ("COMMA", r","),

    # For comparison operators
    ("EQUALITY", r"=="),
    ("LEQ", "<="),
    ("GEQ", ">="),
    ("LESS", r"<"),
    ("MORE", r">"),

    # For operators
    # 1. Plus
    ("PLUS", r"\+"),
    # 2. Minus
    ("MINUS", r"-"),
    # 3. Times
    ("TIMES", r"\*"),
    # 4. Divide
    ("DIVIDE", r"\/"),
    # 5. Carat
    ("CARAT", r"\^"),
    # 6. Equal
    ("EQUAL", r"="),

    # Whitespace (to be ignored later)
    ("WHITESPACE", " "),
)

# This tuple is the master token list
tokens = [_[0] for _ in token_pair]

# This tuple is the master ignored token list
ignored_tokens = (
    # Newlines
    r"\r\n|\r|\n",
    # Tabs
    r"\t",
    # Comments (# ....)
    r"#.*"
)


class Lexer:
    def __init__(self):
        self.token_pair = token_pair
        self.tokens = tokens
        self.ignored_tokens = ignored_tokens
        self.lg = LexerGenerator()
        self.lexer = self.get_lexer()
        if "WHITESPACE" in self.tokens:
            self.tokens.remove("WHITESPACE")

    def get_lexer(self):
        # Add accepted tokens
        for pair in self.token_pair:
            self.lg.add(pair[0], pair[1], re.IGNORECASE)

        # Ignore ignored tokens
        for it in self.ignored_tokens:
            self.lg.ignore(it)
        return self.lg.build()

    def lex(self, s):
        for token in self.lexer.lex(s):
            # Ignore whitespace
            if token.name == "WHITESPACE":
                continue
            yield token


def get_source_signature(source):
    return " ".join([f"{_.name}:{_.value}" for _ in Lexer().lex(source)])
