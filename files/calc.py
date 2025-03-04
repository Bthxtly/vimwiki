INT, FLOAT, EOF, ADD, SUB, MUL, DIV, LPA, RPA = \
    'INT', 'FLOAT', 'EOF', 'ADD', 'SUB', 'MUL', 'DIV', 'LPA', 'RPA'

###############################################################################
#                                  Lexer                                      #
###############################################################################


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.current_char = self.text[self.index]

    def error(self, message):
        raise Exception(f"Lexer failed, {message}")

    def advance(self):
        self.index += 1
        if self.index < len(self.text):
            self.current_char = self.text[self.index]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_a_number(self):
        res = ''
        isFloat = False
        while self.current_char is not None and (
                self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                isFloat = True
            res += self.current_char
            self.advance()
        if isFloat:
            return Token(FLOAT, float(res))
        else:
            return Token(INT, int(res))

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isdigit() or self.current_char == '.':
                return self.get_a_number()

            elif self.current_char.isspace():
                self.skip_whitespace()
                continue

            elif self.current_char == '+':
                self.advance()
                return Token(ADD, '+')

            elif self.current_char == '-':
                self.advance()
                return Token(SUB, '-')

            elif self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            elif self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            elif self.current_char == '(':
                self.advance()
                return Token(LPA, '(')

            elif self.current_char == ')':
                self.advance()
                return Token(RPA, ')')

            else:
                self.error("invalid syntax")

        return Token(EOF, 'EOF')


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    __repr__ = __str__

###############################################################################
#                                  Parser                                     #
###############################################################################


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self, message):
        raise Exception(f"Parser failed, {message}")

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error("syntax error")

    def parse(self):
        res = self.expr()
        if self.current_token.type != EOF:
            self.error(f"unused Token: {self.current_token}")
        return res

    def expr(self):
        '''
        expr    : term ( ( ADD | SUB ) term )*
        '''
        lnode = self.term()
        while self.current_token.type in (ADD, SUB):
            if self.current_token.type == ADD:
                op = self.current_token
                self.eat(ADD)
                rnode = self.term()
                lnode = BinOpNode(op, lnode, rnode)
            elif self.current_token.type == SUB:
                op = self.current_token
                self.eat(SUB)
                rnode = self.term()
                lnode = BinOpNode(op, lnode, rnode)
        return lnode

    def term(self):
        '''
        term    : factor ( ( MUL | DIV ) factor )*
        '''
        lnode = self.factor()
        while self.current_token.type in (MUL, DIV):
            if self.current_token.type == MUL:
                op = self.current_token
                self.eat(MUL)
                rnode = self.factor()
                lnode = BinOpNode(op, lnode, rnode)
            elif self.current_token.type == DIV:
                op = self.current_token
                self.eat(DIV)
                rnode = self.factor()
                lnode = BinOpNode(op, lnode, rnode)
        return lnode

    def factor(self):
        '''
        factor  : INT
                | FLOAT
                | ADD factor
                | SUB factor
                | LPA expr RPA
        '''
        current_token = self.current_token
        if current_token.type == INT:
            self.eat(INT)
            return NumNode(current_token)

        elif current_token.type == FLOAT:
            self.eat(FLOAT)
            return NumNode(current_token)

        elif current_token.type == ADD:
            op = self.current_token
            self.eat(ADD)
            return UniOpNode(op, self.factor())

        elif current_token.type == SUB:
            op = self.current_token
            self.eat(SUB)
            return UniOpNode(op, self.factor())

        elif current_token.type == LPA:
            self.eat(LPA)
            expr = self.expr()
            self.eat(RPA)
            return expr

        else:
            self.error("invalid syntax")


class AST:
    pass


class BinOpNode(AST):
    def __init__(self, op, lnode, rnode):
        self.op = op
        self.lnode = lnode
        self.rnode = rnode

    def visit(self):
        if self.op.type == ADD:
            return self.lnode.visit() + self.rnode.visit()

        elif self.op.type == SUB:
            return self.lnode.visit() - self.rnode.visit()

        elif self.op.type == MUL:
            return self.lnode.visit() * self.rnode.visit()

        elif self.op.type == DIV:
            return self.lnode.visit() / self.rnode.visit()


class NumNode(AST):
    def __init__(self, num):
        self.num = num

    def visit(self):
        return self.num.value


class UniOpNode(AST):
    def __init__(self, op, node):
        self.op = op
        self.node = node

    def visit(self):
        if self.op.type == ADD:
            return self.node.visit()

        elif self.op.type == SUB:
            return - self.node.visit()


###############################################################################
#                                Interpreter                                  #
###############################################################################
class Interpreter(object):
    def __init__(self, parser):
        self.parser = parser

    def interpret(self):
        return self.parser.parse().visit()


###############################################################################
#                                  Main                                       #
###############################################################################
if __name__ == '__main__':
    while True:
        s = input("input the expression(q to exit): ")
        if s == '' or s.upper() == 'Q':
            break
        lexer = Lexer(s)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        print(interpreter.interpret())
