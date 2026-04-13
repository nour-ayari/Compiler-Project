from lexer.lexer import tokenize
from parser.AST import BinaryOp, StringLiteral, Program, VarDecl, Assign, Identifier, Number


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def expect(self, token_type):
        token = self.current()
        if token is None or token[0] != token_type:
            raise SyntaxError(f"Expected {token_type}, found {token}")
        self.advance()
        return token

    def parse_program(self):
        statements = []
        while self.current() is not None:
            statements.append(self.parse_stmt())
        return Program(statements)

    def parse_stmt(self):
        token = self.current()

        if token is None:
            raise SyntaxError("Unexpected end of input")

        if token[0] in ("INT_TYPE", "STRING_TYPE"):
            return self.parse_decl_stmt()
        elif token[0] == "ID":
            return self.parse_assign_stmt()
        else:
            raise SyntaxError(f"Unexpected token {token}")

    def parse_decl_stmt(self):
        type_token = self.current()

        if type_token[0] == "INT_TYPE":
            var_type = "int"
        else:
            var_type = "string"

        self.advance()
        name_token = self.expect("ID")
        self.expect("SEMI")

        return VarDecl(var_type, name_token[1], name_token[2], name_token[3])

    def parse_assign_stmt(self):
        name_token = self.expect("ID")
        self.expect("ASSIGN")
        expr = self.parse_expr()
        self.expect("SEMI")
        return Assign(name_token[1], expr, name_token[2], name_token[3])

    def parse_expr(self):
        left = self.parse_term()

        while self.current() is not None and self.current()[0] == "PLUS":
            op_token = self.current()
            self.advance()
            right = self.parse_term()
            left = BinaryOp(left, op_token[1], right, op_token[2], op_token[3])

        return left

    def parse_term(self):
        token = self.current()

        if token is None:
            raise SyntaxError("Unexpected end of input in expression")

        if token[0] == "ID":
            self.advance()
            return Identifier(token[1], token[2], token[3])
        elif token[0] == "NUM":
            self.advance()
            return Number(token[1], token[2], token[3])

        elif token[0] == "STRING_LITERAL":
            self.advance()
            return StringLiteral(token[1], token[2], token[3])

        elif token[0] == "LPAREN":
            self.advance()
            expr = self.parse_expr()
            self.expect("RPAREN")
            return expr

        else:
            raise SyntaxError(f"Unexpected token in expression: {token}")