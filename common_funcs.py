DE_ZERO = 4294967295  # 4294967295 = !0 in Rust


def get(x: [], i: int) -> int:
    return x[i]


def split1(p: []) -> (int, []):
    return p[0], p[1:]


class ShowProd:

    def __init__(self, _first: [str], _second: [int]):
        self.first = _first
        self.second = _second

    def __str__(self):
        lhs, rhs = split1(self.second)
        out_str = f"{get(self.first, lhs)} ->"
        for r in rhs:
            out_str += f" {get(self.first, r)}"
        return out_str
