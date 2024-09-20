from llmcc.ir import *
from llmcc.config import *
from llmcc.parser import parse
from llmcc.slicer import slice_graph

from pydantic import BaseModel, Field
from tree_sitter import Language, Parser

import tree_sitter_cpp

CPP_LANGUAGE = Language(tree_sitter_cpp.language())


class Analyzer(Visitor):
    """Analysis the dependency for a class or function."""

    def __init__(self):
        self.depends = None
        self.name = None
        pass

    def visit(self, node: Node) -> Any:
        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                getattr(self, f"visit_{child.type}")(child)

    def visit_declaration_list(self, node: Node) -> Any:
        self.visit(node)

    def visit_namespace_definition(self, node: Node) -> Any:
        self.visit(node)

    def query_custom_type(self, node: Node):
        query = CPP_LANGUAGE.query(
            """
        (type_identifier) @type_identifier
        """
        )
        capture = query.captures(node.ts_node)
        if "type_identifier" in capture:
            ty = capture["type_identifier"][0]
            return ty.text.decode("utf-8")

    def visit_field_declaration(self, node: Node) -> Any:
        ty = self.query_custom_type(node)
        if ty:
            log.debug(f"{self.name} depends {ty}")
            self.depends.append(ty)

    def visit_preproc_ifdef(self, node: Node) -> Any:
        self.visit(node)

    def visit_enum_specifier(self, node: Node) -> Any:
        # self.compile(node)
        pass

    def visit_struct_specifier(self, node: Node) -> Any:
        self.visit_class_specifier(node)

    def visit_declaration(self, node: Node) -> Any:
        pass

    def visit_field_declaration_list(self, node: Node) -> Any:
        self.visit(node)

    def visit_class_specifier(self, node: Node) -> Any:
        self.depends = []
        self.name = node.name
        self.visit(node)

    def visit_function_definition(self, node: Node) -> Any:
        pass


def analysis_graph(g: Graph) -> Any:
    analyzer = Analyzer()
    return g.accept(analyzer)
