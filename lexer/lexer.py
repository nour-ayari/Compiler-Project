import re

TOKEN_SPEC = [
    ("KW_IF", r"\bif\b"),
    ("KW_THEN", r"\bthen\b"),
    ("KW_ELSE", r"\belse\b"),

    ("INT_TYPE", r"\bint\b"),
    ("STRING_TYPE", r"\bstring\b"),

    ("STRING_LITERAL", r'"[^"\n]*"'),
    ("NUM", r"\d+"),
    ("ID", r"[A-Za-z_][A-Za-z0-9_]*"),

    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MUL", r"\*"),
    ("DIV", r"/"),
    ("ASSIGN", r"="),
    ("GT", r">"),

    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("SEMI", r";"),

    ("NEWLINE", r"\n"),
    ("SKIP", r"[ \t]+"),
    ("MISMATCH", r"."),
]

master_pattern = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
)

def tokenize(code: str):
    tokens = []
    line_num = 1
    line_start = 0

    for match in master_pattern.finditer(code):
        token_type = match.lastgroup
        value = match.group()
        start = match.start()
        column = start - line_start + 1

        if token_type == "NEWLINE":
            line_num += 1
            line_start = match.end()

        elif token_type == "SKIP":
            continue

        elif token_type == "NUM":
            tokens.append(("NUM", int(value), line_num, column))

        elif token_type == "STRING_LITERAL":
            tokens.append(("STRING_LITERAL", value[1:-1], line_num, column))

        elif token_type == "MISMATCH":
            raise SyntaxError(
                f"Unexpected character '{value}' at line {line_num}, column {column}"
            )

        else:
            tokens.append((token_type, value, line_num, column))

    return tokens


if __name__ == "__main__":
    source_code = """
    int x;
    string name;
    x = 5 + 2;
    name = "Alice";
    """

    result = tokenize(source_code)
    for token in result:
        print(token)