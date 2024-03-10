import lib_helper


def main():
    input_str = """
  Sum     -> Sum     + Product
Sum     -> Sum     - Product
Sum     -> Product
Product -> Product * Factor
Product -> Product / Factor
Product -> Factor
Factor  -> ( Sum )
Factor  -> Number
    """
    parser = lib_helper.from_rules(input_str)
    _, sppf = parser.parse(_input=["Number", "+", "(", "Number", "*", "Number", "-", "Number", ")"], start="Sum")

    it = sppf.iter()
    cnt = 0

    while True:
        tree = it.next()
        if tree is None:
            break
        with open(f"./out/{cnt}.dot", "w") as f:
            f.write(str(tree))
        cnt += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
