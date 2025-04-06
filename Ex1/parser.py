from abc import ABC
from numpy import double
from abc import ABC,abstractmethod

class Expression(ABC):
    @abstractmethod
    def calc(self)->double:
        pass

# implement the classes here
class Num(Expression):
    def __init__(self, x:int):
        self.x = x

    def calc(self) ->double:
        return double(self.x)


class BinExp(Expression):
    def __init__(self, left:Expression, right:Expression):
        self.left = left
        self.right = right

    def calc(self) ->double:
        pass


#implement the parser function here
def parser(expression)->double:
    return 0.0



# from abc import ABC
# from typing import override
#
# from numpy import double
# from abc import ABC,abstractmethod
#
# class Expression(ABC):
#     @abstractmethod
#     def calc(self)->double:
#         pass
#
# # implement the classes here
# class Num(Expression):
#     def __init__(self, x:int):
#         self.x = x
#
#     @override
#     def calc(self) ->double:
#         return x
#
#
# class BinExp(Expression):
#     def __init__(self, right:Expression, left:Expression):
#         self.right = right
#         self.left = left
#
#     @override
#     def calc(self) ->double:
#         pass
#
#
# class Plus(BinExp):
#     def __init__(self):
#         pass
#
#
# #implement the parser function here
# def parser(expression)->double:
#     return 0.0
#
