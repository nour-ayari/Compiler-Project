from lexer.lexer import tokenize
from parser.parser_prog import Parser
from semantic.semantic import SemanticAnalyzer,SemanticError

source_code = """

string name;
x = 5 + 2;
name = "Alice";
"""

tokens = tokenize(source_code)
parser = Parser(tokens)
ast = parser.parse_program()

analyzer = SemanticAnalyzer()

try:
    analyzer.analyze(ast)
    print("Semantic analysis passed")
    print("Symbol table:", analyzer.symbol_table)
except SemanticError as e:
    print("Semantic error:", e)