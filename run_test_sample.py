import lib_helper


def run_test_sample1():
    input_str = """
A -> B1 B2
A -> C1 C2
B1 -> B11
B1 -> B12
B2 -> B21
B2 -> B22
C1 -> C11
C1 -> C12
C2 -> C21
C2 -> C22
B11 -> t
B12 -> t
B21 -> t
B22 -> t
C11 -> t
C12 -> t
C21 -> t
C22 -> t
"""
    parser = lib_helper.from_rules(input_str)
    _, sppf = parser.parse(_input=["t", "t"], start="A")

    it = sppf.iter()
    cnt = 0

    while True:
        tree = it.next()
        if tree is None:
            break
        with open(f"./out/sp2/{cnt}.dot", "w") as f:
            f.write(str(tree))
        cnt += 1


def run_test_sample2():
    input_str = """
    E1 -> Earleys A by B using C
          A -> Parser Example
          B -> Abdul
          C -> GitRust
          E2 -> B1 B2
          E2 -> C1 C2
          B1 -> B11
          B1 -> B12
          B2 -> B21
          B2 -> B22
          C1 -> C11
          C1 -> C12
          C2 -> C21
          C2 -> C22
          B11 -> t
          B12 -> t
          B21 -> t
          B22 -> t
          C11 -> t
          C12 -> t
          C21 -> t
          C22 -> t
          E3 -> NP VP 
          NP -> NP PP 
          PP -> P NP 
          NP -> N 
          VP -> V NP 
          N -> astronomers 
          VP -> VP PP 
          N -> ears 
          P -> with 
          N -> stars 
          V -> saw 
          N -> telescopes
          E4 -> NP VP  
          E4 -> Aux NP VP 
          E4 -> VP 
          NP -> Pronoun 
          NP -> Proper-Noun 
          NP -> Det Nom 
          Nom -> Noun 
          Nom -> Nom Noun 
          Nom -> Nom PP 
          VP -> Verb 
          VP -> Verb NP 
          VP -> Verb NP PP 
          VP -> Verb PP 
          VP -> VP PP 
          PP -> Prep NP 
          Verb -> book
          Noun -> flight
          Det -> that
        """
    parser = lib_helper.from_rules(input_str)
    _, sppf = parser.parse(_input=["t", "t"], start="E2")

    it = sppf.iter()
    cnt = 0

    while True:
        tree = it.next()
        if tree is None:
            break
        with open(f"./out/sp2/{cnt}.dot", "w") as f:
            f.write(str(tree))
        cnt += 1


def run_test_sample3():
    input_str = """
    E1 -> Earleys A by B using C
          A -> Parser Example
          B -> Abdul
          C -> GitRust
          E2 -> B1 B2
          E2 -> C1 C2
          B1 -> B11
          B1 -> B12
          B2 -> B21
          B2 -> B22
          C1 -> C11
          C1 -> C12
          C2 -> C21
          C2 -> C22
          B11 -> t
          B12 -> t
          B21 -> t
          B22 -> t
          C11 -> t
          C12 -> t
          C21 -> t
          C22 -> t
          E3 -> NP VP 
          NP -> NP PP 
          PP -> P NP 
          NP -> N 
          VP -> V NP 
          N -> astronomers 
          VP -> VP PP 
          N -> ears 
          P -> with 
          N -> stars 
          V -> saw 
          N -> telescopes
          E4 -> NP VP  
          E4 -> Aux NP VP 
          E4 -> VP 
          NP -> Pronoun 
          NP -> Proper-Noun 
          NP -> Det Nom 
          Nom -> Noun 
          Nom -> Nom Noun 
          Nom -> Nom PP 
          VP -> Verb 
          VP -> Verb NP 
          VP -> Verb NP PP 
          VP -> Verb PP 
          VP -> VP PP 
          PP -> Prep NP 
          Verb -> book
          Noun -> flight
          Det -> that
        """
    parser = lib_helper.from_rules(input_str)
    _, sppf = parser.parse(_input=["astronomers", "saw", "stars", "with", "ears"], start="E3")

    it = sppf.iter()
    cnt = 0

    while True:
        tree = it.next()
        if tree is None:
            break
        with open(f"./out/sp3/{cnt}.dot", "w") as f:
            f.write(str(tree))
        cnt += 1


def run_test_sample4():
    input_str = """
    E1 -> Earleys A by B using C
          A -> Parser Example
          B -> Abdul
          C -> GitRust
          E2 -> B1 B2
          E2 -> C1 C2
          B1 -> B11
          B1 -> B12
          B2 -> B21
          B2 -> B22
          C1 -> C11
          C1 -> C12
          C2 -> C21
          C2 -> C22
          B11 -> t
          B12 -> t
          B21 -> t
          B22 -> t
          C11 -> t
          C12 -> t
          C21 -> t
          C22 -> t
          E3 -> NP VP 
          NP -> NP PP 
          PP -> P NP 
          NP -> N 
          VP -> V NP 
          N -> astronomers 
          VP -> VP PP 
          N -> ears 
          P -> with 
          N -> stars 
          V -> saw 
          N -> telescopes
          E4 -> NP VP  
          E4 -> Aux NP VP 
          E4 -> VP 
          NP -> Pronoun 
          NP -> Proper-Noun 
          NP -> Det Nom 
          Nom -> Noun 
          Nom -> Nom Noun 
          Nom -> Nom PP 
          VP -> Verb 
          VP -> Verb NP 
          VP -> Verb NP PP 
          VP -> Verb PP 
          VP -> VP PP 
          PP -> Prep NP 
          Verb -> book
          Noun -> flight
          Det -> that
        """
    parser = lib_helper.from_rules(input_str)
    _, sppf = parser.parse(_input=["book", "that", "flight"], start="E4")

    it = sppf.iter()
    cnt = 0

    while True:
        tree = it.next()
        if tree is None:
            break
        with open(f"./out/sp4/{cnt}.dot", "w") as f:
            f.write(str(tree))
        cnt += 1


run_test_sample1()
