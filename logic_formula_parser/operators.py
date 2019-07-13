class Proposition:
    def __init__(self, literal) -> None:
        self.literal = literal


class UnaryOperator:
    def __init__(self, right) -> None:
        self.right = right


class BinaryOperator:
    def __init__(self, left, right) -> None:
        self.left = left
        self.right = right


class Not(UnaryOperator):
    pass


class Box(UnaryOperator):
    pass


class BoxNot(UnaryOperator):
    pass


class Diamond(UnaryOperator):
    pass


class DiamondNot(UnaryOperator):
    pass


class Imply(BinaryOperator):
    pass


class And(BinaryOperator):
    pass


class Or(BinaryOperator):
    pass

