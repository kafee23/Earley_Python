class ParseRulesError(Exception):

    def __init__(self, data: int):
        self.data = data

    def __str__(self):
        if self.data == 0:
            return "empty rules"
        else:
            return f"rules line {self.data} is not in the form of \"lhs -> rhs1 rhs2 ...\""


class ParserException(Exception):

    def __init__(self, data: str):
        self.data = data

    def __str__(self):
        return f"no such terminal or non-terminal: {self.data}"
