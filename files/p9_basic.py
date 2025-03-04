# A very simple pascal interpreter
# https://ruslanspivak.com/lsbasi-part9/

from typing import NoReturn

###############################################################################
#   LERER                                                                     #
###############################################################################


class Token(object):
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return f'Token({self.type}, "{self.value}")'

    def __repr__(self) -> str:
        return self.__str__()


BEGIN, END, SEMI, ID, DOT, EOF = "BEGIN", "END", "SEMI", "ID", "DOT", "EOF"
ASSIGN, PLUS, MINUS, MUL, DIV = "ASSIGN", "PLUS", "MINUS", "MUL", "DIV"
INTEGER = "INTEGER"
LPAREN, RAPAREN = "LPAREN", "RAPAREN"

RESERVED_KEYWORDS = {
    BEGIN: Token(BEGIN, BEGIN),
    END: Token(END, END)
}


class Lexer(object):
    def __init__(self, text) -> None:
        self.text = text
        self.index = 0
        self.current_char = self.text[self.index]
        self.len = len(self.text)

    def error(self, msg) -> NoReturn:
        raise Exception(f"Lexer fails! {msg}")

    def advance(self) -> None:
        if self.index < self.len - 1:
            self.index += 1
            self.current_char = self.text[self.index]
        elif self.index == self.len - 1:
            self.current_char = EOF
        elif self.current_char == EOF:
            self.error("Reach the end of file")
        else:
            self.error("What else?")

    def peek(self) -> str:
        if self.index < self.len - 1:
            return self.text[self.index + 1]
        elif self.index == self.len - 1:
            return EOF
        else:
            self.error("Reach the end of file")

    def skip_whitespace(self) -> None:
        while self.current_char.isspace():
            self.advance()

    def get_number(self) -> Token:
        result = ""
        while self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return Token(INTEGER, int(result))

    def _id(self):
        """ Handle identifiers and reserved keywords"""
        result = ""
        while self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    def get_next_token(self) -> Token:
        while self.current_char != EOF:
            if self.current_char.isspace():
                self.skip_whitespace()

            elif self.current_char.isdigit():
                return self.get_number()

            elif self.current_char.isalnum():
                return self._id()

            elif self.current_char == ".":
                self.advance()
                return Token(DOT, ".")

            elif self.current_char == ";":
                self.advance()
                return Token(SEMI, ";")

            elif self.current_char == ":" and self.peek() == "=":
                self.advance()
                self.advance()
                return Token(ASSIGN, ":=")

            elif self.current_char == "=":
                self.advance()
                return Token(PLUS, "=")

            elif self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")

            elif self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")

            elif self.current_char == "*":
                self.advance()
                return Token(MUL, "*")

            elif self.current_char == "/":
                self.advance()
                return Token(DIV, "/")

            # elif self.current_char == "(":
            #     self.advance()
            #     return Token(LPAREN, "(")

            # elif self.current_char == ")":
            #     self.advance()
            #     return Token(RAPAREN, ")")

            else:
                self.error(f"Unknown character {self.current_char}")
        return Token(EOF, "EOF")

###############################################################################
#   PARSER                                                                    #
###############################################################################


class AST:
    ...


class NumNode(AST):
    def __init__(self, value) -> None:
        self.value = value


class UniNode(AST):
    def __init__(self, node, op) -> None:
        self.node = node
        self.op = op


class DuoNode(AST):
    def __init__(self, left, right, op) -> None:
        self.left = left
        self.right = right
        self.op = op


class Compound(AST):  # Represents a 'BEGIN ... END' block
    def __init__(self) -> None:
        self.children = []


class Assign(AST):
    def __init__(self, left, right, op=":=") -> None:
        self.left = left
        self.right = right
        self.op = op


class Var(AST):  # The Var node is consturcted out of ID token
    def __init__(self, token) -> None:
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class Parser(object):
    def __init__(self, lexer) -> None:
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, msg) -> NoReturn:
        raise Exception(f"Parser fails! {msg}")

    def eat(self, type) -> None:
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Find {self.current_token}, but expect {type}")

    def program(self) -> AST:
        """
        program              : compound_statement DOT
        """
        node = self.compound_statement()
        self.eat(DOT)
        return node

    def compound_statement(self) -> AST:
        """
        compound_statement   : BEGIN statement_list END
        """
        self.eat(BEGIN)
        nodes = self.statement_list()
        self.eat(END)

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self) -> list[AST]:
        """
        statement_list       : statements
                             | statements SEMI statement_list
        """
        node = self.statement()

        result = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            result.append(self.statement())

        if self.current_token.type == ID:
            self.error("Can't parse statement_list")

        return result

    def statement(self) -> AST:
        """
        statement            : compound_statement
                             | assignment_statement
                             | empty
        """
        if self.current_token.type == BEGIN:
            node = self.compound_statement()
        elif self.current_token.type == ID:
            node = self.assignment_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self) -> AST:
        """
        assignment_statement : variable ASSIGN expr
        """
        left = self.variable()
        self.eat(ASSIGN)
        right = self.expr()
        node = Assign(left, right)
        return node

    def variable(self) -> AST:
        """
        variable             : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self) -> AST:
        """
        empty                : [None]
        """
        return NoOp()

    def factor(self) -> AST:
        """
        factor               : PLUS factor
                             | MINUS factor
                             | INTEGER
                             | LPAREN expr RPAREN
                             | variable
        """
        if self.current_token.type == PLUS:
            self.eat(PLUS)
            node = self.factor()
            return UniNode(node, "+")

        elif self.current_token.type == MINUS:
            self.eat(MINUS)
            node = self.factor()
            return UniNode(node, "-")

        elif self.current_token.type == INTEGER:
            node = NumNode(self.current_token.value)
            self.eat(INTEGER)
            return node

        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RAPAREN)
            return node

        else:
            return self.variable()

    def term(self) -> AST:
        """
        term : factor ((MUL | DIV) factor)*
        """
        lnode = self.factor()
        while (self.current_token.type == MUL or
               self.current_token.type == DIV):
            if self.current_token.type == MUL:
                self.eat(MUL)
                rnode = self.factor()
                lnode = DuoNode(lnode, rnode, "*")
            else:
                self.eat(DIV)
                rnode = self.factor()
                lnode = DuoNode(lnode, rnode, "/")
        return lnode

    def expr(self) -> AST:
        """
        expr : term ((PLUS | MINUS) term)*
        """
        lnode = self.term()
        while (self.current_token.type == PLUS or
               self.current_token.type == MINUS):
            if self.current_token.type == PLUS:
                self.eat(PLUS)
                rnode = self.term()
                lnode = DuoNode(lnode, rnode, "+")
            else:
                self.eat(MINUS)
                rnode = self.term()
                lnode = DuoNode(lnode, rnode, "-")
        return lnode

    def parse(self) -> AST:
        node = self.program()
        if self.current_token.type != EOF:
            self.error("Don't reach EOF after parsing the file")
        return node

###############################################################################
#   INTERPRETER                                                               #
###############################################################################


class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)    # self.method_name(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node)} method")


class Interpreter(NodeVisitor):
    def __init__(self, parser) -> None:
        self.parser = parser
        self.GLOBAL_SCOPE = {}

    def visit_NumNode(self, node):
        return node.value

    def visit_UniNode(self, node):
        op = node.op
        value = self.visit(node.node)

        if op == "+":
            return value
        elif op == "-":
            return -value

    def visit_DuoNode(self, node):
        op = node.op
        left = self.visit(node.left)
        right = self.visit(node.right)

        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            return int(left / right)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Assign(self, node):
        self.GLOBAL_SCOPE[node.left.value] = self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def visit_NoOp(self, _):    # a node is sent as the argument
        ...

    def interpret(self):
        return self.visit(self.parser.parse())


def test():
    pascal = """\
BEGIN
    BEGIN
        number := 2;
        a := number;
        b := 10 * a + 10 * number / 4;
        c := a - - b
    END;
    x := 11;
END.
        """
    print(pascal)
    lexer = Lexer(pascal)
    parser = Parser(lexer)
    # print("AST")
    # print_AST(parser.parse())
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)


def print_AST(ast, prefix="", next=False):
    astype = type(ast).__name__

    if astype == "Compound":
        for node in ast.children[:-1]:
            print(prefix + "├── " + "○")
            print_AST(node, prefix + "│   ")

        print(prefix + "└── " + "○")
        print_AST(ast.children[-1], prefix + "    ")

    elif astype == "UniNode":
        print(prefix + "└── " + ast.op)
        print_AST(ast.node, prefix + "    ")

    elif astype == "DuoNode" or astype == "Assign":
        if next:
            branch = "├── "
            append = "│   "
        else:
            branch = "└── "
            append = "    "
        print(prefix + branch + ast.op)
        print_AST(ast.left, prefix + append, next=True)
        print_AST(ast.right, prefix + append)

    elif astype == "Var" or astype == "NumNode":
        branch = "├── " if next else "└── "
        print(prefix + branch + str(ast.value))


if __name__ == "__main__":
    test()
