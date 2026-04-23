import pytest
from lexer.lexer import tokenize
from parser.parser_prog import Parser
from parser.AST import Program, VarDecl, Assign, BinaryOp, Identifier, Number, StringLiteral


def parse(source):
    return Parser(tokenize(source)).parse_program()


# --- Valid programs ---

def test_int_declaration():
    ast = parse("int x;")
    assert len(ast.statements) == 1
    decl = ast.statements[0]
    assert isinstance(decl, VarDecl)
    assert decl.var_type == "int"
    assert decl.name == "x"

def test_string_declaration():
    ast = parse("string name;")
    decl = ast.statements[0]
    assert isinstance(decl, VarDecl)
    assert decl.var_type == "string"
    assert decl.name == "name"

def test_assignment_number():
    ast = parse("int x;\nx = 5;")
    assign = ast.statements[1]
    assert isinstance(assign, Assign)
    assert assign.name == "x"
    assert isinstance(assign.expr, Number)
    assert assign.expr.value == 5

def test_assignment_string_literal():
    ast = parse('string s;\ns = "hello";')
    assign = ast.statements[1]
    assert isinstance(assign.expr, StringLiteral)
    assert assign.expr.value == "hello"

def test_assignment_identifier():
    ast = parse("int x;\nint y;\ny = x;")
    assign = ast.statements[2]
    assert isinstance(assign.expr, Identifier)
    assert assign.expr.name == "x"

def test_binary_op_addition():
    ast = parse("int x;\nx = 5 + 2;")
    assign = ast.statements[1]
    assert isinstance(assign.expr, BinaryOp)
    assert assign.expr.op == "+"
    assert isinstance(assign.expr.left, Number)
    assert isinstance(assign.expr.right, Number)

def test_chained_addition():
    ast = parse("int x;\nx = 1 + 2 + 3;")
    assign = ast.statements[1]
    # left-associative: (1+2)+3
    assert isinstance(assign.expr, BinaryOp)
    assert isinstance(assign.expr.left, BinaryOp)
    assert assign.expr.right.value == 3

def test_string_concat():
    ast = parse('string s;\ns = "hello" + " world";')
    assign = ast.statements[1]
    assert isinstance(assign.expr, BinaryOp)
    assert isinstance(assign.expr.left, StringLiteral)
    assert isinstance(assign.expr.right, StringLiteral)

def test_multiple_statements():
    ast = parse("int x;\nstring s;\nx = 1;\ns = \"a\";")
    assert len(ast.statements) == 4

def test_program_node_type():
    ast = parse("int x;")
    assert isinstance(ast, Program)

def test_line_and_column_on_decl():
    ast = parse("int x;")
    decl = ast.statements[0]
    assert decl.line == 1
    assert decl.column == 5  # 'x' is at column 5

def test_empty_program():
    ast = parse("")
    assert isinstance(ast, Program)
    assert ast.statements == []


# --- Invalid programs ---

def test_missing_semicolon_raises():
    with pytest.raises(SyntaxError):
        parse("int x")

def test_missing_assign_raises():
    with pytest.raises(SyntaxError):
        parse("x 5;")

def test_unknown_token_raises():
    with pytest.raises(SyntaxError):
        parse("42 = x;")

def test_incomplete_expression_raises():
    with pytest.raises(SyntaxError):
        parse("int x;\nx = ;")
