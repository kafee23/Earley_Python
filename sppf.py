from dataclasses import dataclass

from common_funcs import get, DE_ZERO, split1, ShowProd


class SPPFNode:

    def __init__(self, _prod: [int], _range: range, _children: [[int]]):
        # // for non-terminal, prod[0] is always lhs, so prod is never empty
        #   // for terminal, prod is empty, range.start == range.end == position of this token, children is empty
        self.prod = _prod
        self.range = _range
        self.children = _children

    def __str__(self) -> str:
        return f"prod={len(self.prod)} range=({self.range.start}..{self.range.stop}) children={len(self.children)}"


class State:
    ...


@dataclass
class State0(State):
    node: int
    parent: int
    ch_idx: int


@dataclass
class State1(State):
    ...


@dataclass
class State2(State):
    node: int
    cur: int
    ch_idx: int


class SPPF:

    def __init__(self, _parser, _start: int, _tokens: [int], _nodes: [SPPFNode]):
        self.parser = _parser
        self.start = _start
        self.tokens = _tokens
        self.nodes = _nodes

    def __str__(self):
        out_str = "digraph g {\n"
        id2token = self.parser.id2token()
        circles = 0
        for idx, sppf_node in enumerate(self.nodes):
            prod = sppf_node.prod
            _range = sppf_node.range
            children = sppf_node.children
            if len(prod) > 0:
                out_str += f"  {idx}[shape=rect, label=\"{ShowProd(id2token, prod)}, {_range.start}..{_range.stop}\"]\n"
                for ch in children:
                    if len(ch) == 1:
                        out_str += f"  {idx} -> {ch[0]}\n"
                    else:
                        out_str += f"  {idx} -> circle{circles}\n"
                        out_str += f"  circle{circles}[shape=circle, label=\"\", width=0.2]\n"

                        for t in ch:
                            out_str += f"  circle{circles} -> {t}\n"

                        circles += 1
            else:
                out_str += f"  {idx}[shape=circle, label=\"{get(id2token, get(self.tokens, _range.start))}\"]\n"
        out_str += "}\n"
        return out_str

    def find(self, prod: [int], _range: range) -> int:
        for idx, node in enumerate(self.nodes):
            if node.prod == prod and node.range.start == _range.start and node.range.stop == _range.stop:
                return idx
        # if can't find any element
        self.nodes.append(SPPFNode(prod, _range, []))
        return len(self.nodes) - 1

    def iter(self):
        stk = []
        for idx, node in enumerate(self.nodes):
            if len(node.prod) > 0 and node.prod[0] == self.start and node.range.start == 0 and node.range.stop == len(
                    self.tokens):
                stk.append(State0(node=idx, parent=DE_ZERO, ch_idx=0))
        tree = SPPF(_parser=self.parser, _start=self.start, _tokens=self.tokens.copy(), _nodes=[])
        return Iter(_sppf=self, _stk=stk, _poses=[], _tree=tree)


class Iter:

    def __init__(self, _sppf: SPPF, _stk: [State], _poses: [(int, int, int)], _tree: SPPF):
        self.sppf = _sppf
        self.stk = _stk
        self.poses = _poses
        self.tree = _tree

    def next(self) -> SPPF | None:
        sppf = self.sppf
        stk = self.stk
        poses = self.poses
        tree = self.tree
        while True:
            last_stk_el = stk.pop(len(stk) - 1)  # pop last and get the value
            if isinstance(last_stk_el, State0):
                node = last_stk_el.node
                parent = last_stk_el.parent
                ch_idx = last_stk_el.ch_idx

                sppf_node = get(sppf.nodes, node)
                prod = sppf_node.prod
                _range = sppf_node.range
                children = sppf_node.children

                cur = len(tree.nodes)
                tree.nodes.append(SPPFNode(_prod=prod, _range=_range, _children=[]))

                if parent != DE_ZERO:
                    tree.nodes[parent].children[0][ch_idx] = cur

                if len(children) == 0:  # empty
                    stk.append(State1())

                    if len(poses) > 0:
                        last_p_node, last_p_parent, last_p_ch_idx = poses.pop(len(poses) - 1)
                        stk.append(State0(node=last_p_node, parent=last_p_parent, ch_idx=last_p_ch_idx))
                    else:
                        return tree
                else:
                    tree.nodes[cur].children.append([0] * (len(prod) - 1))
                    stk.append(State2(node=node, cur=cur, ch_idx=0))
            elif isinstance(last_stk_el, State1):
                tree.nodes.pop(len(tree.nodes) - 1)
            elif isinstance(last_stk_el, State2):
                node = last_stk_el.node
                cur = last_stk_el.cur
                ch_idx = last_stk_el.ch_idx

                n = sppf.nodes[node]
                if ch_idx < len(n.children):
                    fst, remain = split1(n.children[ch_idx])

                    for idx, r in reversed(list(enumerate(remain))):
                        print(f"WHOSE {idx}")
                        poses.append((r, cur, idx + 1))

                    stk.append(State2(node=node, cur=cur, ch_idx=ch_idx + 1))
                    stk.append(State0(node=fst, parent=cur, ch_idx=0))
                else:
                    tree.nodes.pop(len(tree.nodes) - 1)

            if len(stk) == 0:
                return None
