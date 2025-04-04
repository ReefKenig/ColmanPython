import re
from abc import ABC, abstractmethod

from numpy import double

PATTERN = r'\d+|\+|\-|\*|\/|\(|\)'
OPERATOR_PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2}


class Expression(ABC):
    @abstractmethod
    def calc(self) -> double:
        pass


# implement the classes here
class Num(Expression):
    def __init__(self, x: int):
        self.x = x

    def calc(self) -> double:
        return self.x


class BinExp(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right

    @abstractmethod
    def calc(self) -> double:
        pass


class Plus(BinExp):
    def calc(self) -> double:
        return self.left.calc() + self.right.calc()


class Minus(BinExp):
    def calc(self) -> double:
        return self.left.calc() - self.right.calc()


class Mul(BinExp):
    def calc(self) -> double:
        return self.left.calc() * self.right.calc()


class Div(BinExp):
    def calc(self) -> double:
        if self.right.calc() == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return self.left.calc() / self.right.calc()


def preprocess_tokens(tokens):
    result = []
    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == '-' and (i == 0 or tokens[i - 1] in OPERATOR_PRECEDENCE or tokens[i - 1] == '('):
            if i + 1 < len(tokens) and tokens[i + 1].isdigit():
                result.append('-' + tokens[i + 1])
                i += 2
                continue
        result.append(token)
        i += 1
    return result


def infix_to_rpn(tokens):
    queue = []
    stack = []
    for token in tokens:
        # Token is a number
        if re.fullmatch(r'-?\d+', token):
            queue.append(token)
        # Token is operator
        elif token in OPERATOR_PRECEDENCE.keys():
            while (stack and stack[-1] in OPERATOR_PRECEDENCE and
                   OPERATOR_PRECEDENCE[stack[-1]] >= OPERATOR_PRECEDENCE[token]):
                queue.append(stack.pop())
            else:
                stack.append(token)
        # Token is left bracket
        elif token == '(':
            stack.append(token)
        # Token is right bracket
        elif token == ')':
            while stack and stack[-1] != '(':
                queue.append(stack.pop())
            stack.pop()

    while stack:
        queue.append(stack.pop())

    return queue


def build_expression_tree(rpn):
    stack = []

    for token in rpn:
        if token not in OPERATOR_PRECEDENCE:
            # Operand
            stack.append(Num(float(token)))
        else:
            # Binary operator
            right = stack.pop()
            left = stack.pop()
            if token == '+':
                stack.append(Plus(left, right))
            elif token == '-':
                stack.append(Minus(left, right))
            elif token == '*':
                stack.append(Mul(left, right))
            elif token == '/':
                stack.append(Div(left, right))

    return stack[0]


# implement the parser function here
def parser(expression) -> double:
    tokens = re.findall(PATTERN, expression)
    tokens = preprocess_tokens(tokens)
    rpn = infix_to_rpn(tokens)
    expr_tree = build_expression_tree(rpn)
    return expr_tree.calc()
