import pytest
from lexer.lexer import tokenize


def types(code):
    return [t[0] for t in tokenize(code)]

def values(code):
    return [t[1] for t in tokenize(code)]


# --- Valid programs ---

def test_int_declaration():
    tokens = tokenize("int x;")
    assert tokens[0] == ("INT_TYPE", "int", 1, 1)
    assert tokens[1] == ("ID", "x", 1, 5)
    assert tokens[2] == ("SEMI", ";", 1, 6)

def test_string_declaration():
    tokens = tokenize("string name;")
    assert tokens[0] == ("STRING_TYPE", "string", 1, 1)
    assert tokens[1] == ("ID", "name", 1, 8)

def test_assignment_with_arithmetic():
    toks = tokenize("x = 5 + 2;")
    assert [t[0] for t in toks] == ["ID", "ASSIGN", "NUM", "PLUS", "NUM", "SEMI"]
    assert toks[2][1] == 5
    assert toks[4][1] == 2

def test_string_literal_strips_quotes():
    tokens = tokenize('name = "Alice";')
    str_tok = next(t for t in tokens if t[0] == "STRING_LITERAL")
    assert str_tok[1] == "Alice"

def test_keywords():
    tokens = tokenize("if x then")
    assert tokens[0][0] == "KW_IF"
    assert tokens[2][0] == "KW_THEN"

def test_else_keyword():
    tokens = tokenize("else")
    assert tokens[0][0] == "KW_ELSE"

def test_operators():
    tokens = tokenize("+ - * / = >")
    assert [t[0] for t in tokens] == ["PLUS", "MINUS", "MUL", "DIV", "ASSIGN", "GT"]

def test_parentheses_and_braces():
    tokens = tokenize("( ) { }")
    assert [t[0] for t in tokens] == ["LPAREN", "RPAREN", "LBRACE", "RBRACE"]

def test_multiline_line_numbers():
    tokens = tokenize("int x;\nint y;")
    assert tokens[0][2] == 1  # int x on line 1
    assert tokens[3][2] == 2  # int y on line 2

def test_column_tracking():
    tokens = tokenize("int x;")
    assert tokens[0][3] == 1   # 'int' starts at col 1
    assert tokens[1][3] == 5   # 'x' starts at col 5

def test_empty_input():
    assert tokenize("") == []

def test_whitespace_only():
    assert tokenize("   \t  ") == []

def test_numeric_literal_parsed_as_int():
    tokens = tokenize("42")
    assert tokens[0] == ("NUM", 42, 1, 1)

def test_identifier_with_underscore():
    tokens = tokenize("my_var")
    assert tokens[0][0] == "ID"
    assert tokens[0][1] == "my_var"

def test_identifier_not_confused_with_keyword():
    # 'iff' should be ID, not KW_IF
    tokens = tokenize("iff")
    assert tokens[0][0] == "ID"

def test_string_concat_tokens():
    tokens = tokenize('"hello" + " world"')
    assert tokens[0][0] == "STRING_LITERAL"
    assert tokens[0][1] == "hello"
    assert tokens[1][0] == "PLUS"
    assert tokens[2][0] == "STRING_LITERAL"
    assert tokens[2][1] == " world"


# --- Invalid programs ---

def test_invalid_character_raises():
    with pytest.raises(SyntaxError):
        tokenize("x = @5;")

def test_unterminated_string_raises():
    with pytest.raises(SyntaxError):
        tokenize('"unterminated')
