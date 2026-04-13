class SemanticError(Exception):
    def __init__(self, message, line=None, column=None):
        self.message = message
        self.line = line
        self.column = column

        if line is not None and column is not None:
            super().__init__(f"{message} at line {line}, column {column}")
        elif line is not None:
            super().__init__(f"{message} at line {line}")
        else:
            super().__init__(message)


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise SemanticError(f"No visit method for {type(node).__name__}")

    def visit_Program(self, node):
        for stmt in node.statements:
            self.analyze(stmt)

    def visit_Assign(self, node):
        if node.name not in self.symbol_table:
            raise SemanticError(
                f"Variable '{node.name}' not declared",
                node.line,
                node.column
            )

        var_type = self.symbol_table[node.name]
        expr_type = self.analyze(node.expr)

        if var_type != expr_type:
            raise SemanticError(
                f"Type mismatch: cannot assign {expr_type} to {var_type} variable '{node.name}'",
                node.line,
                node.column
            )

    def visit_Identifier(self, node):
        if node.name not in self.symbol_table:
            raise SemanticError(
                f"Variable '{node.name}' not declared",
                node.line,
                node.column
            )
        return self.symbol_table[node.name]

    def visit_Number(self, node):
        return "int"

    def visit_VarDecl(self, node):
        if node.name in self.symbol_table:
            raise SemanticError(
                f"Variable '{node.name}' already declared",
                node.line,
                node.column
            )
        self.symbol_table[node.name] = node.var_type

    def visit_StringLiteral(self, node):
        return "string"

    def visit_BinaryOp(self, node):
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)

        if node.op == "+":
            if left_type == right_type:
                return left_type
            else:
                raise SemanticError(
                    f"Type mismatch in expression: {left_type} + {right_type}",
                    node.line,
                    node.column
                )

        raise SemanticError(
            f"Unsupported operator '{node.op}'",
            node.line,
            node.column
        )