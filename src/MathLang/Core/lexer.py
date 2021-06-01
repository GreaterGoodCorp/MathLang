import re
from typing import Generator

from rply import LexerGenerator, Token

# This tuple is the master token-pattern pairs list
token_pair = (
    # For reserved keywords
    # 1. Print
    ("PRINT", r"print"),
    # 2. Plot
    ("PLOT", r"plot"),
    # 3. Solve
    ("SOLVE", r"solve"),
    # 4. In
    ("IN", r"IN"),
    # 5. Real
    ("REAL", r"REAL"),
    # 6. Rational
    ("RATIONAL", r"RATIONAL"),
    # 7. Integer
    ("INTEGER", r"INTEGER"),

    # For identifiers
    # At most 64 characters
    ("ID", r"[_a-zA-Z][_a-zA-Z0-9]{0,63}"),

    # For numbers
    ("NUMBER", r"\d+(?:\.\d+)?"),

    # For special symbols
    # 1. Parentheses
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    # 2. Semicolon
    ("SEMICOLON", r"\;"),
    # 3. Comma
    ("COMMA", r","),

    # For comparison operators
    ("EQ", r"=="),
    ("NEQ", r"=="),
    ("LTE", "<="),
    ("LT", r"<"),
    ("GTE", ">="),
    ("GT", r">"),

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

    def lex(self, s) -> Generator[Token, None, None]:
        """Yields a stream of tokens from source.

        :param s: MathLang source code.
        :type s: str
        :return: A stream of tokens.
        :rtype: Generator[Token]
        """
        for token in self.lexer.lex(s):
            # Ignore whitespace
            if token.name == "WHITESPACE":
                continue
            yield token


def get_source_signature(source) -> str:
    """Gets signature of MathLang source.

    Note that the signature only takes into account the source code, not any comments. As a result, two sources might
    have the same signature despite the fact that their hashes are different.

    :param source: MathLang source code.
    :type source: str
    :return: A signature string.
    :rtype: str
    """
    return " ".join([f"{_.name}:{_.value}" for _ in Lexer().lex(source)])
