from llmcc.ir import *
from llmcc.config import *
from llmcc.parser import parse
from llmcc.scoper import *

from pydantic import BaseModel, Field
from tree_sitter import Language, Parser

import tree_sitter_cpp


class Analyzer(ScopeVisitor):
    """Analysis the dependency for a class or function."""

    def __init__(self, g: Graph):
        super().__init__(g)

    def resolve_depend(self, name):
        cur = self.scope.root
        assert cur.name, cur.text
        if cur.depend_store is None:
            cur.depend_store = Store()

        log.debug(f"reslove symbol: {name} for {cur.name}")
        depend_nodes = self.scope.resolve(name)
        for node in depend_nodes:
            # NOTE: given a function name, there could be multiple override version of it
            assert isinstance(node, Node), node
            if node.id == cur.id:
                continue
            log.debug(f"{cur.name}:{cur.id} depends `{node.name}:{node.id}'")
            cur.depend_store.append_version({name: node})

    def impl_field_data_declarator(self, node) -> Any:
        def query_custom_type(node: Node):
            CPP_LANGUAGE = Language(tree_sitter_cpp.language())
            query = CPP_LANGUAGE.query(
                """
            (type_identifier) @type_identifier
            """
            )
            capture = query.captures(node.ts_node)
            if "type_identifier" in capture:
                ty = capture["type_identifier"][0]
                return Node(ts_node=ty).text

        ty = query_custom_type(node)
        if ty:
            log.debug(f"reslove data field type: {ty}")
            self.resolve_depend(ty)

    def impl_call_expression(self, node: Node) -> Any:
        call = node.text.split("(")[0]
        log.debug(f"reslove function call: {call}")
        self.resolve_depend(call)

    def impl_struct_specifier(self, node: Node) -> Any:
        self.visit(node)

    def impl_class_specifier(self, node: Node) -> Any:
        self.visit(node)

    def impl_function_definition(self, node: Node) -> Any:
        self.visit(node, continue_down=True)

        # if this function inside a class, it should also depends on this class
        parent = self.scope.parent.root
        if parent is not None and parent.is_complex_type():
            self.resolve_depend(parent.scope_name)


def analyze_graph(g: Graph) -> Any:
    analyzer = Analyzer(g)
    analyzer.visit(g.root)
