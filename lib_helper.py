from earley_exceptions import ParserException, ParseRulesError
from sppf import SPPF
from common_funcs import get, DE_ZERO, split1, ShowProd


class Item:

    def __init__(self, _prod: [], _dot: int, _orig: int):
        self.prod = _prod
        self.dot = _dot
        self.orig = _orig

    def __str__(self):
        return f"prod=len.{len(self.prod)} dot={self.dot} orig={self.orig}"

    def __eq__(self, other):
        """
        compare production array using pointer, because each prod is considered unique
        :param other:
        :return:
        """
        return self.prod is other.prod and self.dot == other.dot and self.orig == other.orig


# the dp chart type
Chart = [[Item]]


class Parser:
    def __init__(self, _prods: [], _tokens: {}, _nullable: []):
        self.prods = _prods
        self.tokens = _tokens  # hash map
        self.nullable = _nullable

    def __str__(self) -> str:
        id2token = self.id2token()
        out_str = ""
        for prod in self.prods:
            out_str += f"{ShowProd(id2token, prod)}\n"
        return out_str

    def token_id(self, t):
        return self.tokens.get(t, None)

    def terminal_id(self, t: str) -> int:
        t_id = self.token_id(t)
        if t_id >= len(self.nullable):
            return t_id

        raise ParserException

    def non_terminal_id(self, t: str) -> int:
        t_id = self.token_id(t)
        if t_id < len(self.nullable):
            return t_id

        raise ParserException

    def id2token(self) -> [str]:
        ret = [-1] * len(self.tokens)
        for k, v in self.tokens.items():
            ret[v] = k
        return ret

    def parse(self, _input: [str], start: str) -> (Chart, SPPF):
        """
        return Err only when input/start contains undefined terminal/non-terminal
        so returning Ok doesn't mean the parse succeeds
        `SPPF::next` will return a sequence of possible trees, so the parse succeeds when it returns anything
        :param _input:
        :param start:
        :return:
        """
        tokens = []
        for t in _input:
            try:
                tokens.append(
                    self.terminal_id(t)
                )
            except ParserException:
                raise ParserException(t)

        try:
            new_start = self.non_terminal_id(start)
        except ParserException:
            raise ParserException(start)
        print(f"[lib_helper.py][parse] {tokens}")
        return self.do_parse(tokens, new_start)

    def do_parse(self, tokens: [int], start: int) -> (Chart, SPPF):
        nt_num = len(self.nullable)
        sets = [[] for i in range(len(tokens) + 1)]
        for prod in self.prods:
            if get(prod, 0) == start:
                # // dot = 1 is start position, because [0] is lhs
                sets[0].append(Item(prod, _dot=1, _orig=0))

        def set_add(v: [Item], x: Item):
            if not x in v:
                v.append(x)

        for i in range(0, len(tokens) + 1):
            si = sets[i]
            token = tokens[i] if i < len(tokens) else None
            j = 0
            while j < len(si):
                it = si[j]
                nxt = it.prod[it.dot] if it.dot < len(it.prod) else None
                if nxt is not None:
                    # // is a non-terminal
                    if nxt < nt_num:
                        # // PREDICATE step
                        for prod in self.prods:
                            if get(prod, 0) == nxt:
                                set_add(si, Item(prod, 1, i))

                        if get(self.nullable, nxt):
                            # // this is a modification (or say correction) to the original earley parser
                            # // a nullable non-terminal A can be advanced without seeing A -> string. during PREDICATE
                            # step
                            # // for more detail, see
                            # https://courses.engr.illinois.edu/cs421/sp2012/project/PracticalEarleyParsing.pdf
                            set_add(si, Item(it.prod, it.dot + 1, it.orig))
                    elif token == nxt:
                        # // is a terminal, SCAN step
                        # // this never causes duplication, so no need to check `contains`
                        # // when i == tokens.len(), i + 1 seems to be out of range of `sets`, but it will never really
                        # // causes an error
                        # // because when i == tokens.len(), token is None, so this branch is never entered
                        sets[i + 1].append(Item(it.prod, it.dot + 1, it.orig))
                else:
                    # // COMPLETE step
                    lhs = get(it.prod, 0)
                    # // caution: it is possible that i == orig, so can't use iterator
                    # // the semantics of this step is just iterating over those already in the sets
                    orig = sets[it.orig]
                    for idx in range(0, len(orig)):
                        it2 = orig[idx]
                        if it2.dot < len(it2.prod) and it2.prod[it2.dot] == lhs:
                            set_add(si, Item(it2.prod, it2.dot + 1, it2.orig))
                j += 1
        complete = [[] for i in range(len(tokens) + 1)]
        for idx, _set in enumerate(sets):
            for item in _set:
                if len(item.prod) == item.dot:
                    complete[item.orig].append(Item(item.prod, item.dot, idx))

        class DfsCtx:
            def __init__(self, _range: range, _nt_num: int, _complete: [[Item]], _prod: [int], _sppf: SPPF,
                         _path: [(int, int)]):
                self.range = _range
                self.nt_num = _nt_num
                self.complete = _complete
                self.prod = _prod
                self.sppf = _sppf
                self.path = _path

            def dfs(self, cur: int, start_dfs: int):
                if cur < len(self.prod) and self.prod[cur] is not None:
                    x = self.prod[cur]

                    if x < self.nt_num:
                        for idx, it in enumerate(self.complete[start_dfs]):
                            print(f"Index: {idx}")
                            if get(it.prod, 0) == x:
                                self.path.append((start_dfs, idx))
                                self.dfs(cur=cur + 1, start_dfs=it.orig)
                                self.path.pop(len(self.path) - 1)
                    elif start_dfs < len(self.sppf.tokens) and self.sppf.tokens[start_dfs] == x:
                        self.path.append((DE_ZERO, start_dfs))
                        self.dfs(cur=cur + 1, start_dfs=start_dfs + 1)
                        self.path.pop(len(self.path) - 1)
                elif len(self.path) != 0:
                    node = self.sppf.find(self.prod, self.range)
                    ch = []
                    cur = self.range.start
                    for state, idx in self.path:
                        if state != DE_ZERO:
                            it = get(get(self.complete, state, ), idx)
                            ch.append(self.sppf.find(it.prod, range(cur, it.orig)))
                            cur = it.orig
                        else:
                            ch.append(self.sppf.find([], range(cur, cur)))
                            cur += 1
                    if cur == self.range.stop:
                        self.sppf.nodes[node].children.append(ch)

        ctx = DfsCtx(range(0, len(tokens)), nt_num, complete, [], SPPF(self, start, tokens, []), [])
        for item in ctx.complete[0]:
            print(item.prod)
            print(item.orig)
            if item.prod[0] == start and item.orig == len(ctx.sppf.tokens):
                ctx.prod = item.prod
                ctx.dfs(cur=1, start_dfs=0)
        i = 0
        while i < len(ctx.sppf.nodes):
            print(f"i: {i}")
            sppf_node = ctx.sppf.nodes[i]
            # // not visited && non-terminal
            if len(sppf_node.children) == 0 and len(sppf_node.prod) != 0:
                _range = sppf_node.range
                ctx.range = _range
                ctx.prod = sppf_node.prod
                ctx.dfs(cur=1, start_dfs=_range.start)
            i += 1

        nodes = ctx.sppf.nodes[0]
        # // reorder, so that the children containing no production are in the front
        # // in this way the dfs on sppf can generate trees from short to tall, instead of insisting on a infinite tall
        # tree
        for n in ctx.sppf.nodes:
            if len(n.children) >= 1:
                first_part = []
                second_part = []
                # // this if is not necessary, just save some work
                for child in n.children:
                    cond1 = True
                    for c in child:
                        if len(ctx.sppf.nodes[c].children) != 0:
                            cond1 = False
                    if cond1:
                        first_part.append(child)
                    else:
                        second_part.append(child)
                n.children = [*first_part, *second_part]
        return sets, ctx.sppf


def from_rules(rules: str) -> Parser:
    prods = []
    tokens = {}  # hash map
    nullable = []

    lines = [line.strip() for line in rules.splitlines() if line.strip() != "" and not line.strip().startswith("#")]

    for idx, line in enumerate(lines):
        sp = line.split()

        if len(sp) == 0:
            raise ParseRulesError(idx + 1)
        lhs = sp[0]

        _id = len(tokens)
        if lhs not in tokens.keys():
            tokens[lhs] = _id
        prods.append([tokens[lhs]])

    if len(prods) == 0:
        raise ParseRulesError(0)
    nullable = [False] * len(tokens)

    for idx, (rule, prod) in enumerate(zip(lines, prods)):
        sp = rule.split()

        # ensure the second element is ->
        if len(sp) < 3:
            ParseRulesError(idx + 1)

        for rhs in sp[2:]:
            # print(f"rhs: {rhs}")
            _id = len(tokens)
            if rhs not in tokens.keys():
                tokens[rhs] = _id
            prods[idx].append(tokens[rhs])

    changed = False
    # // compute nullable set
    while True:
        for p in prods:
            (lhs, rhs) = split1(p)
            if get(nullable, lhs):
                continue
            cond2 = True
            for r in rhs:
                if r >= len(nullable) or not nullable[r]:
                    cond2 = False
                    break
            if cond2:
                nullable[lhs] = True
                changed = True
        if not changed:
            break

    return Parser(prods, tokens, nullable)
