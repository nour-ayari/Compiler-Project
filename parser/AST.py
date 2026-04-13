class Program:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Program({self.statements})"


class VarDecl:
    def __init__(self, var_type, name, line=None, column=None):
        self.var_type = var_type
        self.name = name
        self.line = line
        self.column = column

    def __repr__(self):
        return f"VarDecl(type={self.var_type}, name={self.name}, line={self.line}, column={self.column})"


class Assign:
    def __init__(self, name, expr, line=None, column=None):
        self.name = name
        self.expr = expr
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Assign(name={self.name}, expr={self.expr}, line={self.line}, column={self.column})"


class Identifier:
    def __init__(self, name, line=None, column=None):
        self.name = name
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Identifier({self.name}, line={self.line}, column={self.column})"


class Number:
    def __init__(self, value, line=None, column=None):
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Number({self.value}, line={self.line}, column={self.column})"


class StringLiteral:
    def __init__(self, value, line=None, column=None):
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"StringLiteral({self.value}, line={self.line}, column={self.column})"


class BinaryOp:
    def __init__(self, left, op, right, line=None, column=None):
        self.left = left
        self.op = op
        self.right = right
        self.line = line
        self.column = column

    def __repr__(self):
        return f"BinaryOp(left={self.left}, op='{self.op}', right={self.right}, line={self.line}, column={self.column})"




