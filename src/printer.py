from src.ir import *


class Printer(Visitor):
    def __init__(self):
        self.indent = 0

    def visit(self, node: Node) -> Any:
        if node.is_named:
            text = node.text.decode('utf-8').replace('\n', '\\n')
            print(f"{'  ' * self.indent} ({node.type}: {text}")
        self.indent += 1
        for child in node.children:
            self.visit(child)
        self.indent -= 1
        return None


def print_graph(g: Graph):
    print('\n')
    printer = Printer()
    printer.visit(g.root)


class Writer(Visitor):
    def __init__(self, file):
        self.file = open(file, 'w')

    def __del__(self):
        self.file.close()

    def visit(self, node: Node) -> Any:
        if node.code_store:
            store = node.code_store.get_current_version()
            parsed = store["parsed"]
            source_code = store["source_code"]
            self.file.write('//' + source_code.replace('\n', '\n//'))
            self.file.write('\n')
            self.file.write(parsed.target_code)
            self.file.write('\n')
        for child in node.children:
            self.visit(child)
        return None

def write_graph(g: Graph, file: str):
    writer = Writer(file)
    writer.visit(g.root)
    return None