from src.ir import *


class Printer(Visitor):
    def __init__(self):
        self.indent = 0

    def visit(self, node: Node) -> Any:
        print("  " * self.indent + node.type)
        self.indent += 1
        for child in node.children:
            self.visit(child)
        self.indent -= 1
        return None


def print_graph(g: Graph):
    print('\n')
    printer = Printer()
    printer.visit(g.root)