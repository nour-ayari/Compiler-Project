import pytest
from lexer.lexer import tokenize
from parser.parser_prog import Parser
from semantic.semantic import SemanticAnalyzer, SemanticError


def analyze(source):
    ast = Parser(tokenize(source)).parse_program()
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    return analyzer


# --- Valid programs ---

def test_int_declaration_populates_symbol_table():
    a = analyze("int x;")
    assert a.symbol_table == {"x": "int"}

def test_string_declaration_populates_symbol_table():
    a = analyze("string name;")
    assert a.symbol_table == {"name": "string"}

def test_int_assignment_passes():
    a = analyze("int x;\nx = 5;")
    assert a.symbol_table["x"] == "int"

def test_string_assignment_passes():
    a = analyze('string s;\ns = "hello";')
    assert a.symbol_table["s"] == "string"

def test_int_addition_passes():
    analyze("int x;\nx = 1 + 2;")

def test_string_concat_passes():
    analyze('string s;\ns = "hello" + " world";')

def test_assign_from_identifier_passes():
    analyze("int x;\nint y;\nx = 5;\ny = x;")

def test_multiple_variables():
    a = analyze("int x;\nstring name;\nx = 1;\nname = \"Alice\";")
    assert a.symbol_table == {"x": "int", "name": "string"}

def test_chained_int_addition():
    analyze("int x;\nx = 1 + 2 + 3;")


# --- Scope errors ---

def test_undeclared_variable_assign_raises():
    with pytest.raises(SemanticError) as exc:
        analyze("x = 5;")
    assert "not declared" in str(exc.value)

def test_undeclared_variable_in_expr_raises():
    with pytest.raises(SemanticError):
        analyze("int x;\nx = y;")

def test_duplicate_declaration_raises():
    with pytest.raises(SemanticError) as exc:
        analyze("int x;\nint x;")
    assert "already declared" in str(exc.value)


# --- Type errors ---

def test_assign_string_to_int_raises():
    with pytest.raises(SemanticError) as exc:
        analyze('int x;\nx = "hello";')
    assert "Type mismatch" in str(exc.value)

def test_assign_int_to_string_raises():
    with pytest.raises(SemanticError) as exc:
        analyze("string s;\ns = 42;")
    assert "Type mismatch" in str(exc.value)

def test_mixed_type_addition_raises():
    with pytest.raises(SemanticError) as exc:
        analyze('int x;\nx = 1 + "hello";')
    assert "Type mismatch" in str(exc.value)

def test_assign_string_var_to_int_raises():
    with pytest.raises(SemanticError):
        analyze('int x;\nstring s;\ns = "a";\nx = s;')


# --- Error location info ---

def test_semantic_error_has_line():
    with pytest.raises(SemanticError) as exc:
        analyze("x = 5;")
    assert exc.value.line == 1

def test_semantic_error_message_contains_variable_name():
    with pytest.raises(SemanticError) as exc:
        analyze("myvar = 5;")
    assert "myvar" in str(exc.value)
