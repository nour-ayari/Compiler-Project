import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS

from lexer.lexer import tokenize
from parser.parser_prog import Parser
from semantic.semantic import SemanticAnalyzer, SemanticError

app = Flask(__name__)
CORS(app)


def ast_to_dict(node):
    if node is None:
        return None
    t = type(node).__name__
    if t == "Program":
        return {"type": "Program", "statements": [ast_to_dict(s) for s in node.statements]}
    if t == "VarDecl":
        return {"type": "VarDecl", "var_type": node.var_type, "name": node.name, "line": node.line, "column": node.column}
    if t == "Assign":
        return {"type": "Assign", "name": node.name, "expr": ast_to_dict(node.expr), "line": node.line, "column": node.column}
    if t == "BinaryOp":
        return {"type": "BinaryOp", "op": node.op, "left": ast_to_dict(node.left), "right": ast_to_dict(node.right), "line": node.line, "column": node.column}
    if t == "Identifier":
        return {"type": "Identifier", "name": node.name, "line": node.line, "column": node.column}
    if t == "Number":
        return {"type": "Number", "value": node.value, "line": node.line, "column": node.column}
    if t == "StringLiteral":
        return {"type": "StringLiteral", "value": node.value, "line": node.line, "column": node.column}
    return {"type": t}


@app.post("/compile")
def compile_code():
    body = request.get_json(force=True)
    source = body.get("source", "")

    result = {"tokens": None, "ast": None, "semantic": None, "error": None, "stage": None}

    try:
        tokens = tokenize(source)
        result["tokens"] = [{"type": t[0], "value": t[1], "line": t[2], "col": t[3]} for t in tokens]
    except SyntaxError as e:
        result["error"] = str(e)
        result["stage"] = "lexer"
        return jsonify(result)

    try:
        parser = Parser(tokens)
        ast = parser.parse_program()
        result["ast"] = ast_to_dict(ast)
    except SyntaxError as e:
        result["error"] = str(e)
        result["stage"] = "parser"
        return jsonify(result)

    try:
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        result["semantic"] = {"ok": True, "symbol_table": analyzer.symbol_table}
    except SemanticError as e:
        result["error"] = str(e)
        result["stage"] = "semantic"
        return jsonify(result)

    result["stage"] = "ok"
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
