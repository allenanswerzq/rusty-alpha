from llmcc.ir import *
from llmcc.config import *


class Printer(Visitor):

    def __init__(self):
        self.indent = 0

    def visit(self, node: Node) -> Any:
        if node.is_named:
            text = node.text.replace("\n", "\\n").replace("  ", "")
            print(f"{'  ' * self.indent} ({node.type} {node.name} {node.id}: {text}")
        self.indent += 1
        for child in node.children:
            self.visit(child)
        self.indent -= 1
        return None


def print_node(n: Node):
    print("\n")
    printer = Printer()
    printer.visit(n)


def print_graph(g: Graph):
    print_node(g.root)


class Writer(Visitor):

    def __init__(self, file):
        self.file_name = file
        self.file = open(file, "a+")

    def __del__(self):
        self.file.close()

    def write(self, node):
        if node.code_store is None:
            return

        log.info(f"writing {node.type} {node.name}")
        store = node.code_store.get_current_version()
        parsed = store["parsed"]
        src_node = store["src_node"]
        if src_node.depend_store:
            if src_node.depend_store.current_version > 0:
                depends = src_node.depend_store.get_current_version()
                for k, v in depends.items():
                    self.file.write(f"//+[Depends] {node.name} -> {v.name}")
                    self.file.write("\n")
                    self.file.write("//+" + v.text.replace("\n", "\n//+"))
                    self.file.write("\n")
                    self.file.write("//+-------------------------------------------\n")
        self.file.write("//|" + src_node.text.replace("\n", "\n//|"))
        self.file.write("\n")
        self.file.write(parsed.root.text)
        self.file.write("\n")

    def visit(self, node: Node) -> Any:
        if node.is_class() and node.slice_store:
            assert node.slice_store
            slice = node.slice_store.get_current_version()
            data_node = slice["data"]
            func_nodes = slice["func"]
            assert data_node or func_nodes
            if data_node is not None:
                self.write(data_node)
            if func_nodes is not None:
                for f, v in func_nodes.items():
                    self.write(v)

        if node.code_store:
            self.write(node)

        for child in node.children:
            self.visit(child)


def write_graph(g: Graph, file: str):
    writer = Writer(file)
    writer.visit(g.root)
    return None
