# A very simple pascal interpreter

from typing import NoReturn, Sequence

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


PROGRAM = "PROGRAM"
VAR = "VAR"
BEGIN = "BEGIN"
END = "END"
ID = "ID"
EOF = "EOF"
DIV = "DIV"

DOT = "DOT"                     # .
COMMA = "COMMA"                 # ,
COLON = "COLON"                 # :
SEMI = "SEMI"                   # ;
ASSIGN = "ASSIGN"               # :=
PLUS = "PLUS"                   # +
MINUS = "MINUS"                 # -
MUL = "MUL"                     # *
FLOAT_DIV = "FLOAT_DIV"         # /
INTEGER_DIV = "INTEGER_DIV"     # DIV
LPAREN = "LPAREN"               # (
RAPAREN = "RAPAREN"             # )

INTEGER = "INTEGER"
REAL = "REAL"
INTEGER_CONST = "INTEGER_CONST"
REAL_CONST = "REAL_CONST"

RESERVED_KEYWORDS = {
    PROGRAM: Token(PROGRAM, PROGRAM),
    VAR: Token(VAR, VAR),
    DIV: Token(INTEGER_DIV, DIV),
    INTEGER: Token(INTEGER, INTEGER),
    REAL: Token(REAL, REAL),
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

    def skip_comment(self) -> None:
        while self.current_char != "}":
            self.advance()
        self.advance()

    def number(self) -> Token:
        result = ""
        while self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token(REAL_CONST, float(result))

        else:
            return Token(INTEGER_CONST, int(result))

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

            elif self.current_char == "{":
                self.skip_comment()

            elif self.current_char.isdigit():
                return self.number()

            elif self.current_char.isalnum():
                return self._id()

            elif self.current_char == ".":
                self.advance()
                return Token(DOT, ".")

            elif self.current_char == ",":
                self.advance()
                return Token(COMMA, ",")

            elif self.current_char == ";":
                self.advance()
                return Token(SEMI, ";")

            elif self.current_char == ":":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(ASSIGN, ":=")
                else:
                    self.advance()
                    return Token(COLON, ":")

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
                return Token(FLOAT_DIV, "/")

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


class Program(AST):
    def __init__(self, name, block) -> None:
        self.name = name
        self.block = block


class Block(AST):
    def __init__(self, declarations, compound_statement) -> None:
        self.declarations = declarations
        self.compound_statement = compound_statement


class VarDecl(AST):  # var : type
    def __init__(self, var_node, type_node) -> None:
        self.var_node = var_node
        self.type_node = type_node


class Type(AST):  # type
    def __init__(self, token) -> None:
        self.token = token
        self.value = token.value


class Num(AST):  # number
    def __init__(self, value) -> None:
        self.value = value


class UniNode(AST):  # op node
    def __init__(self, node, op) -> None:
        self.node = node
        self.op = op


class DuoNode(AST):  # left op right
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
            # print(f"eat {self.current_token} done!")
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Expect {type}, find {self.current_token}")

    def program(self) -> AST:
        """
        program              : PROGRAM variable SEMI block DOT
        """
        self.eat(PROGRAM)
        prog_name = self.variable().value
        self.eat(SEMI)
        block_node = self.block()
        program_node = Program(prog_name, block_node)
        self.eat(DOT)
        return program_node

    def block(self) -> AST:
        """
        block                : declarations compound_statement
        """
        declaration_node = self.declarations()
        compound_statement_node = self.compound_statement()
        node = Block(declaration_node, compound_statement_node)
        return node

    def declarations(self) -> list[AST]:
        """
        declarations         : VAR (variable_declaration SEMI)+
                             | empty
        """
        declarations = []
        if self.current_token.type == VAR:
            self.eat(VAR)
            while self.current_token.type == ID:
                var_decl = self.variable_declaration()
                declarations.extend(var_decl)
                self.eat(SEMI)

        return declarations

    def variable_declaration(self) -> Sequence[AST]:
        """
        variable_declaration : ID (COMMA ID)* COLON type_spec
        """
        var_nodes = [Var(self.current_token)]
        self.eat(ID)
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_nodes.append(Var(self.current_token))
            self.eat(ID)
        self.eat(COLON)

        type_node = self.type_spec()
        variable_declarations = [
            VarDecl(var_node, type_node)
            for var_node in var_nodes
        ]
        return variable_declarations

    def type_spec(self) -> AST:
        """
        type_spec            : INTEGER | REAL
        """
        token = self.current_token
        if self.current_token.type == INTEGER:
            self.eat(INTEGER)
        elif self.current_token.type == REAL:
            self.eat(REAL)
        else:
            self.error(f"Unknown type {self.current_token.type}")
        node = Type(token)
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

    def variable(self) -> Var:
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
                             | INTEGER_CONST
                             | REAL_CONST
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

        elif self.current_token.type == INTEGER_CONST:
            node = Num(self.current_token.value)
            self.eat(INTEGER_CONST)
            return node

        elif self.current_token.type == REAL_CONST:
            node = Num(self.current_token.value)
            self.eat(REAL_CONST)
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
        term : factor ((MUL | INTEGER_DIV | FLOAT_DIV) factor)*
        """
        node = self.factor()
        while self.current_token.type in (MUL, INTEGER_DIV, FLOAT_DIV):
            op = self.current_token.value
            if self.current_token.type == MUL:
                self.eat(MUL)
            elif self.current_token.type == INTEGER_DIV:
                self.eat(INTEGER_DIV)
            elif self.current_token.type == FLOAT_DIV:
                self.eat(FLOAT_DIV)
            else:
                self.error("term")

            node = DuoNode(node, self.factor(), op)

        return node

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
#   SYMBOL TABLE                                                              #
###############################################################################


class Symbol(object):
    def __init__(self, name, type=None) -> None:
        self.name = name
        self.type = type


class BuiltinTypeSymbol(Symbol):
    def __init__(self, name, type=None) -> None:
        super().__init__(name, type)

    def __str__(self) -> str:
        return self.name

    __repr__ = __str__


class VarSymbol(Symbol):
    def __init__(self, name, type=None) -> None:
        super().__init__(name, type)

    def __str__(self) -> str:
        return f"<{self.name}: {self.type}>"

    __repr__ = __str__


class SymbolTable(object):
    def __init__(self) -> None:
        self._symbols = {}
        self._init_builtins()

    def _init_builtins(self):
        self.define(BuiltinTypeSymbol('INTEGER'))
        self.define(BuiltinTypeSymbol('REAL'))

    def __str__(self) -> str:
        return "Symbols: {symbols}".format(
            symbols=[value for value in self._symbols.values()]
        )

    __repr__ = __str__

    def define(self, symbol):
        print(f"Define: {symbol}")
        self._symbols[symbol.name] = symbol

    def lookup(self, name) -> Symbol | None:
        print(f"Lookup: {name}")
        symbol = self._symbols.get(name)
        return symbol


###############################################################################
#   INTERPRETER                                                               #
###############################################################################


class NodeVisitor(object):
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)    # self.method_name(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")


class SymbolTableBuilder(NodeVisitor):
    def __init__(self) -> None:
        self.symtab = SymbolTable()

    def visit_UniNode(self, node):
        self.visit(node.expr)

    def visit_DuoNode(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Num(self, _):
        pass

    def visit_NoOp(self, _):    # a node is sent as the argument
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))
        self.visit(node.right)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symtab.lookup(var_name)
        if var_symbol is None:
            raise NameError(repr(var_name))

    def visit_Program(self, node):
        self.visit(node.block)

    def visit_Block(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_VarDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.symtab.lookup(type_name)
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)
        self.symtab.define(var_symbol)


def test():
    pascal = """
        PROGRAM Part11;
        VAR
        number : INTEGER;
        a, b   : INTEGER;
        y      : REAL;

        BEGIN {Part11}
        number := 2;
        a := number ;
        b := 10 * a + 10 * y DIV 4;
        y := 20 / 7 + 3.14
        END.  {Part11}
    """
    lexer = Lexer(pascal)
    parser = Parser(lexer)
    ast = parser.parse()
    stb = SymbolTableBuilder()
    stb.visit(ast)
    print(stb.symtab)


if __name__ == "__main__":
    test()
