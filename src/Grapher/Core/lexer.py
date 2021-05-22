import re

from rply import LexerGenerator

# Number sets
sets = ("complexes", "reals", "integers", "naturals")

# This tuple is the master token-pattern pairs list
token_pair = (
    # For strings
    ("STRING", r'(?<=").*(?=")'),

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
    # 4. Newline
    # Works for both Windows, Linux and MacOS
    ("NEWLINE", r"(\r\n|\r|\n)+"),

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

    # For comparison operators
    ("LESS", r"<"),
    ("MORE", r">"),
)

# This tuple is the master token list
tokens = (_[0] for _ in token_pair)

# This tuple is the master ignored token list
ignored_tokens = (
    # Whitespaces
    r" ",
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

    def add_tokens(self):
        for pair in self.token_pair:
            self.lexer.add(pair[0], pair[1], re.IGNORECASE)

    def get_lexer(self):
        # Add accepted tokens
        for pair in self.token_pair:
            self.lexer.add(pair[0], pair[1], re.IGNORECASE)

        # Ignore ignored tokens
        for it in self.ignored_tokens:
            self.lexer.ignore(it)
        return self.lexer.build()


if __name__ == '__main__':
    from pathlib import Path
    lexer = Lexer().get_parser()
    path_to_test_data = (Path(__file__).parent.parent / "Tests" / "test_data").absolute()
    path_to_source1 = path_to_test_data / "source1.gp"
    with open(path_to_source1) as fp:
        source_code = fp.read()
    tokens = lexer.lex(source_code)
    s = " ".join([token.value for token in tokens])
    path_to_lexed_source1 = path_to_test_data / "source1.lexed"
    with open(path_to_lexed_source1) as fp:
        assert fp.read().strip("\n") == s
