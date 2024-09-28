from llmcc.ir import *
from llmcc.config import *
from llmcc.parser import parse
from llmcc.slicer import is_field_func_declarator, is_field_class_declarator

from pydantic import BaseModel, Field
from tree_sitter import Language, Parser

import tree_sitter_cpp

CPP_LANGUAGE = Language(tree_sitter_cpp.language())


class Analyzer(Visitor):
    """Analysis the dependency for a class or function."""

    def __init__(self, g: Graph):
        self.curr_node = []
        self.g = g

    def visit(self, node: Node, continue_down=False) -> Any:
        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                getattr(self, f"visit_{child.type}")(child)

            elif continue_down:
                self.visit(child, continue_down=continue_down)

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
            return ty.text

    def resolve_depend(self, cur, name, allow_same_level=True):
        # get the parent node which has a name associated with it
        parent = cur
        while parent:
            if parent.type in [
                "function_definition",
                "class_specifier",
                "struct_specifier",
                "enum_specifier",
            ]:
                break
            parent = parent.parent
        cur = parent
        assert cur, self.curr_node[-1].text
        assert cur.name, cur.text

        if cur.depend_store is None:
            cur.depend_store = Store()
        depend_nodes = self.g.resolve_name(name, cur, allow_same_level=allow_same_level)
        # assert len(depend_nodes) > 0
        for depend_node in depend_nodes:
            if depend_node.id == cur.id:
                continue
            # log.debug(f"{cur.name}:{cur.id} depends `{depend_node.name}:{depend_node.id}'")
            if depend_node.slice_store:
                depend = depend_node.slice_store.get_current_version()
                data_node = depend["data"]
                # func_nodes = depend["func"]
                cur.depend_store.append_version({name: data_node})
            else:
                cur.depend_store.append_version({name: depend_node})

    def visit_field_declaration(self, node: Node) -> Any:
        if is_field_func_declarator(node) or is_field_class_declarator(node):
            return

        ty = self.query_custom_type(node)
        if ty:
            # log.debug(f"analyze field decl {node.text.decode('utf-8')}")
            cur = self.curr_node[-1]
            self.resolve_depend(cur, ty)

    def visit_declaration(self, node: Node) -> Any:
        self.visit_field_declaration(node)

    def visit_call_expression(self, node: Node) -> Any:
        call = node.text.split("(")[0]
        assert len(self.curr_node) > 0
        # log.debug(f"resolving {call} {self.curr_node[-1].text}")
        cur = self.curr_node[-1]
        self.resolve_depend(cur, call)

    def visit_preproc_ifdef(self, node: Node) -> Any:
        self.visit(node)

    def visit_enum_specifier(self, node: Node) -> Any:
        # self.compile(node)
        pass

    def visit_struct_specifier(self, node: Node) -> Any:
        self.depends = []
        self.curr_node.append(node)
        self.visit(node)
        self.curr_node.pop()

    def visit_field_declaration_list(self, node: Node) -> Any:
        self.visit(node)

    def visit_class_specifier(self, node: Node) -> Any:
        self.depends = []
        self.curr_node.append(node)
        self.visit(node)
        self.curr_node.pop()

    def visit_function_definition(self, node: Node) -> Any:
        self.curr_node.append(node)
        self.visit(node, continue_down=True)
        self.curr_node.pop()

        # if this function inside a class, it should also depends on this class
        if len(node.name.split(".")) >= 3:
            name = node.name.split(".")[-3]
            self.resolve_depend(node, name, allow_same_level=False)


def analyze_graph(g: Graph) -> Any:
    analyzer = Analyzer(g)
    return g.accept(analyzer)
