import tree_sitter_cpp

from tree_sitter import Language, Parser
from tree_sitter import Node as TsNode

from llmcc.ir import *
from llmcc.parser import parse
from llmcc.config import *
from llmcc.assigner import *
from llmcc.scoper import ScopeVisitor


class Slicer(ScopeVisitor):

    def __init__(self, g: Graph):
        super().__init__(g)
        self.data_fields = []
        self.func_definitions = []
        self.nested_classes = []

    def visit_function_definition(self, node: Node) -> Any:
        self.func_definitions.append(node)

    def visit_field_class_declarator(self, node) -> Any:
        assert node.children[0].is_complex_type()
        nest = node.children[0]
        self.nested_classes.append(nest)

    def visit_field_data_declarator(self, node) -> Any:
        self.data_fields.append(node)

    def visit_struct_specifier(self, node: Node) -> Any:
        self.visit_class_specifier(node)

    def visit_class_specifier(self, node: Node) -> Any:
        def func(node: Node, continue_down=False):
            self.data_fields = []
            self.func_definitions = []
            self.nested_classes = []

            # for child in node.children:
            #     self.visit(child)

            nested_class = self.nested_classes.copy()
            data_fields = self.data_fields.copy()
            func_definitions = self.func_definitions.copy()
            for nest in nested_class:
                pass
                # TODO: move the scope up one level
                # self.visit(nest)

            # data = collect_class_data(self.scope, data_fields)
            # func = collect_class_func(self.scope, func_definitions)

            # if data:
            #     log.debug("\n" + data.text)
            # if func:
            #     for k, v in func.items():
            #         log.debug("\n" + v.text)

            # if node.slice_store is None:
            #     node.slice_store = Store()
            # if data or func:
            #     node.slice_store.add_version(
            #         {"data": data, "func": func, "nest_classes": nested_class}
            #     )
        log.debug(f"scope visit struct {node.text}")
        self.scope_visit(node)


def slice_graph(g: Graph) -> Any:
    log.info("slicing the graph")
    slicer = Slicer(g)
    slicer.visit(g.root)


def collect_class_data(scope: Scope, fields) -> Node:
    chain = scope.get_scope_chain()
    text = ""
    indent = 0
    for sc in chain:
        name = sc.root.name.split(".")[-1]
        text += " " * indent + f"{sc.root.scope_str} {name} {{\n"
        indent += 4
    for field in fields:
        text += " " * indent + field.text
        text += "\n"
    for sc in chain:
        indent -= 4
        text += " " * indent + "}\n"
    assert indent == 0
    return parse(text).root


def collect_class_func(scope, funcs) -> Dict[str, Node]:
    func_text = {}
    class_name = scope.root.name
    for f in funcs:
        type = Node(ts_node=f.child_by_field_name("type")).text
        d = f.child_by_field_name("declarator")
        stmt = Node(ts_node=f.child_by_field_name("body")).text
        name = Node(ts_node=d.child_by_field_name("declarator")).text
        para = Node(ts_node=d).text
        text = f"""
        {type} {class_name.replace('.', '::')}::{para} {stmt.rstrip()}
        """
        node = parse(text).root
        node.name = f"{class_name}.{para}"
        for j in range(0, 100):
            # TOOD: use paramter type to unique the override function
            override = f"{class_name}.{name}.{j}"
            if override not in func_text:
                func_text[override] = node
                break
    return func_text
