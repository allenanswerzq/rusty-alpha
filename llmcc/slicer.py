import tree_sitter_cpp as tscpp

from tree_sitter import Language, Parser
from tree_sitter import Node as TsNode

from llmcc.ir import *
from llmcc.parser import parse
from llmcc.config import *

CPP_LANGUAGE = Language(tscpp.language())


class Slicer(Visitor):

    def __init__(self):
        self.field_declarator = []
        self.funtion_definition = []
        self.nested_class_declarator = []
        self.nested_class_global = []

    def visit(self, node: Node) -> Any:
        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                getattr(self, f"visit_{child.type}")(child)

            if child.type in ["class_specifier", "struct_specifier"]:
                n = len(self.nested_class_declarator)
                self.nested_class_global.extend(self.nested_class_declarator)
                for nest in self.nested_class_global[-n:]:
                    self.visit_class_specifier(nest)

    def visit_declaration_list(self, node: Node) -> Any:
        for child in node.children:
            self.visit(child)

    def visit_namespace_definition(self, node: Node) -> Any:
        for child in node.children:
            self.visit(child)

    def visit_preproc_ifdef(self, node: Node) -> Any:
        self.visit(node)

    def visit_struct_specifier(self, node: Node) -> Any:
        self.visit_class_specifier(node)

    def visit_field_declaration_list(self, node: Node) -> Any:
        for child in node.children:
            self.visit(child)

    def visit_function_definition(self, node: Node) -> Any:
        # log.debug(node.text)
        log.debug(node.rows)
        self.funtion_definition.append(node)

    def visit_field_declaration(self, node: Node) -> Any:
        if is_field_func_declarator(node):
            # NOTE: we dont need function decl because it will have a impl function in the cpp file
            pass
        elif is_field_class_declarator(node):
            assert node.children[0].type == "class_specifier"
            nest = node.children[0]
            parts = nest.name.split(".")
            parts.pop(-2)
            nest.name = ".".join(parts)
            self.nested_class_declarator.append(nest)
        else:
            self.field_declarator.append(node.ts_node)

    def visit_class_specifier(self, node: Node) -> Any:
        self.field_declarator = []
        self.funtion_definition = []
        self.nested_class_declarator = []

        for child in node.children:
            self.visit(child)

        class_name = node.name
        data = collect_class_data(class_name, self.field_declarator)
        func = collect_class_func(class_name, self.funtion_definition)
        if data:
            log.debug(data.text)
        if func:
            for k, v in func.items():
                log.debug(v.text)
        if node.depends_store is None:
            node.depends_store = Store()
        if data or func:
            node.depends_store.add_version({"data": data, "func": func})


def slice_graph(g: Graph) -> Any:
    compiler = Slicer()
    return g.accept(compiler)


def is_field_func_declarator(node: TsNode | Node):
    query = CPP_LANGUAGE.query(
        """
    (
    (field_declaration 
        (_)
        (function_declarator)
    ) @field_declaration
    )
    (
    (field_declaration 
        (_)
        (pointer_declarator
            (function_declarator)
        )
    ) @field_declaration
    )
    """
    )

    if isinstance(node, Node):
        node = node.ts_node

    capture = query.captures(node)
    return len(capture) > 0


def is_field_class_declarator(node: TsNode | Node):
    query = CPP_LANGUAGE.query(
        """
    (
    (field_declaration 
        (class_specifier)
    ) @field_declaration
    )
    """
    )

    if isinstance(node, Node):
        node = node.ts_node

    capture = query.captures(node)
    return len(capture) > 0


def collect_class_data(class_name, fields) -> Node:
    if len(fields) == 0:
        return None
    fields_text = "\n".join("    " + field.text.decode("utf-8") for field in fields)
    parts = class_name.split(".")
    assert len(parts) in [1, 2]
    if len(parts) == 1:
        code = f"""
class {class_name} {{
{fields_text}
}};
    """
    else:
        code = f"""
namespce {parts[0]} {{
    class {parts[1]} {{
{fields_text}
    }}
}};
    """
    return parse(code).root


def collect_class_func(class_name, funcs) -> Dict[str, Node]:
    if len(funcs) == 0:
        return None
    func_text = {}
    for f in funcs:
        type = f.child_by_field_name("type").text.decode("utf-8")
        d = f.child_by_field_name("declarator")
        stmt = f.child_by_field_name("body").text.decode("utf-8")
        name = d.child_by_field_name("declarator").text.decode("utf-8")
        para = d.text.decode("utf-8")
        text = f"""
        {type} {class_name.replace('.', '::')}::{para} {stmt}
        """
        node = parse(text).root
        for j in range(0, 100):
            # TOOD: use paramter type to unique the override function
            override = f"{class_name}.{name}.{j}"
            if override not in func_text:
                func_text[override] = node
                break
    return func_text
