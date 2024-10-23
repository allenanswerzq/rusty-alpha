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

        log.debug(f"reslove symbol: {name} -> {cur.name}")
        depend_nodes = self.scope.resolve(name)
        for node in depend_nodes:
            # NOTE: given a function name, there could be multiple override version of it
            assert isinstance(node, Node), node
            if node.id == cur.id:
                continue
            log.debug(f"{cur.name}:{cur.id} depends `{node.name}:{node.id}'")
            cur.depend_store.append_version({name: node})

    def visit_field_data_declarator(self, node) -> Any:
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

    def visit_field_class_declarator(self, node) -> Any:
        self.visit(node)

    def visit_type_identifier(self, node: Node) -> Any:
        if not self.scope.root.is_complex_type():
            log.warn(f"reslove type identifier: {node.text} {self.scope.root.text}")
            self.resolve_depend(node.text)

    def visit_call_expression(self, node: Node) -> Any:
        call = node.text.split("(")[0]
        log.debug(f"reslove function call: {call}")
        self.resolve_depend(call)

    def visit_declaration(self, node: Node) -> Any:
        root = self.scope.root
        if root.is_function():
            self.visit(node, continue_down=True)
        else:
            pass

    def visit_function_definition(self, node: Node) -> Any:
        def func(node: Node, continue_down=False):
            self.visit(node, continue_down=continue_down)

            # if this function inside a class, it should also depends on this class
            parent = self.scope.parent.root
            if parent is not None and parent.is_complex_type():
                log.debug(
                    f"reslove nest function class {node.name}-> {parent.scope_name}"
                )
                self.resolve_depend(parent.scope_name)

        self.scope_visit(node, func=func, continue_down=True)


def analyze_graph(g: Graph) -> Any:
    log.info("analyzing the graph")
    analyzer = Analyzer(g)
    analyzer.visit(g.root)
