import pygraphviz as pgv
from IPython.display import Image


def render(dotfile: str, outputfile: str):
    # Read the content of the uploaded .dot file
    with open(dotfile, "r") as file:
        dot_content = file.read()

    # Generate graph from dot content
    graph = pgv.AGraph(string=dot_content)

    # Render the graph to a PNG image
    file_path = outputfile
    graph.layout(prog="dot")
    graph.draw(file_path)

    # Display the image
    Image(file_path)


def main():
    render("./0.dot", "0.png")


if __name__ == "__main__":
    main()
