from llmcc.ir import *
from llmcc.config import *


class Printer(Visitor):

    def __init__(self):
        self.indent = 0

    def visit(self, node: Node) -> Any:
        if node.is_named:
            text = node.text.decode("utf-8").replace("\n", "\\n").replace("  ", "")
            print(f"{'  ' * self.indent} ({node.type} {node.name} {node.id}: {text}")
        self.indent += 1
        for child in node.children:
            self.visit(child)
        self.indent -= 1
        return None


def print_graph(g: Graph):
    print("\n")
    printer = Printer()
    printer.visit(g.root)


class Writer(Visitor):

    def __init__(self, file):
        self.file_name = file
        self.file = open(file, "a+")

    def __del__(self):
        self.file.close()

    def write(self, node):
        log.info(f"writing {node.type} {node.name}")
        store = node.code_store.get_current_version()
        parsed = store["parsed"]
        source_code = store["source_code"]
        self.file.write("//|" + source_code.text.decode("utf-8").replace("\n", "\n//|"))
        self.file.write("\n")
        self.file.write(parsed.root.text.decode("utf-8"))
        self.file.write("\n")

    def visit(self, node: Node) -> Any:
        if node.type == "translation_unit" and node.depend_store:
            depends = node.depend_store.get_current_version()
            if "include_files" in depends:
                for include in depends["include_files"]:
                    write_graph(include, self.file_name)

        if node.type in ["class_specifier", "struct_specifier"]:
            assert node.slice_store
            depend = node.slice_store.get_current_version()
            data_node = depend["data"]
            func_nodes = depend["func"]
            assert data_node or func_nodes
            if data_node:
                self.write(data_node)
            if func_nodes:
                for f, v in func_nodes:
                    self.write(v)

        if node.code_store:
            self.write(node)

        for child in node.children:
            self.visit(child)


def write_graph(g: Graph, file: str):
    writer = Writer(file)
    writer.visit(g.root)
    return None
