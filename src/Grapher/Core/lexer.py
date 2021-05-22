import re

from rply import LexerGenerator

# Number sets
sets = ("complexes", "reals", "integers", "naturals")

# This tuple is the master token-pattern pairs list
token_pair = (
    # For strings
    ("STRING", r'".*"'),

    # For reserved keywords
    # 1. Print
    ("PRINT", r"print"),
    # 2. Plot
    ("PLOT", r"plot"),
    # 3. Solve
    ("SOLVE", r"solve"),
    # 4. In
    ("IN", r"in"),

    # For flow controls
    # 1. If
    ("IF", r"if"),
    ("ELSE", r"else"),
    ("ENDIF", r"endif"),
    # 2. While
    ("WHILE", r"while"),
    ("ENDWHILE", r"endwhile"),

    # For number sets
    ("SET", r"|".join(sets)),

    # For identifiers
    # At most 64 characters
    ("ID", r"[_a-zA-Z][_a-zA-Z0-9]{0,63}"),

    # For numbers
    ("NUMBER", r"\d+(?:\.\d+)?"),

    # For special symbols
    # 1. Parentheses
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    # 2. Square brackets
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    # 3. Semicolon
    ("SEMICOLON", r"\;"),

    # For comparison operators
    ("LESS", r"<"),
    ("MORE", r">"),
    ("EQUALITY", r"=="),

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
tokens = (_[0] for _ in token_pair)

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
        self.lexer = LexerGenerator()

    def get_lexer(self):
        # Add accepted tokens
        for pair in self.token_pair:
            self.lexer.add(pair[0], pair[1], re.IGNORECASE)

        # Ignore ignored tokens
        for it in self.ignored_tokens:
            self.lexer.ignore(it)
        return self.lexer.build()


def get_source_signature(source):
    return "".join([_.value for _ in Lexer().get_lexer().lex(source)])
