import tree_sitter_cpp as tscpp

from tree_sitter import Language, Parser
from tree_sitter import Node as TsNode

from acc.ir import *
from acc.parser import parse
from acc.config import *

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

            if child.type == "class_specifier": 
                n = len(self.nested_class_declarator)
                self.nested_class_global.extend(self.nested_class_declarator)
                for nest in self.nested_class_global[-n:]:
                    self.visit_class_specifier(nest)

    def visit_preproc_ifdef(self, node: Node) -> Any:
        self.visit(node)

    def visit_struct_specifier(self, node: Node) -> Any:
        pass

    def visit_field_declaration_list(self, node: Node) -> Any:
        for child in node.children:
            self.visit(child)
    
    def visit_function_definition(self, node: Node) -> Any:
        self.funtion_definition.append(node)

    def visit_field_declaration(self, node: Node) -> Any:
        if is_field_func_declarator(node):
            # NOTE: we dont need function decl because it will have a impl function in the cpp file
            pass
        elif is_field_class_declarator(node):
            assert node.children[0].type == "class_specifier"
            self.nested_class_declarator.append(node.children[0])
            self.nested_class_global.append(node.children[0])
        else:
            self.field_declarator.append(node.ts_node)

    def visit_class_specifier(self, node: Node) -> Any:
        self.field_declarator = []
        self.funtion_definition = []
        self.nested_class_declarator = []

        for child in node.children:
            self.visit(child)

        class_name = get_class_name(node)
        data = collect_class_data(class_name, self.field_declarator)
        func = collect_class_func(class_name, self.funtion_definition)
        log.debug(data.text)
        for k, v in func.items():
            log.debug(v.text)
        if node.depends_store is None:
            node.depends_store = Store()
        node.depends_store.add_version({"data": data, "func": func})


def slice_graph(g: Graph) -> Any:
    compiler = Slicer()
    return g.accept(compiler)

def get_class_name(node: TsNode | Node):
    query = CPP_LANGUAGE.query("""
        (class_specifier
        (type_identifier) @class_name)
        """)

    if isinstance(node, Node):
        node = node.ts_node

    captures = query.captures(node)
    assert 'class_name' in captures
    return captures['class_name'][0].text.decode('utf-8')


def is_field_func_declarator(node: TsNode | Node):
    query = CPP_LANGUAGE.query("""
    (
    (field_declaration 
        (_) 
        (function_declarator)
    ) @field_declaration
    )
    """)

    if isinstance(node, Node):
        node = node.ts_node

    capture = query.captures(node)
    return len(capture) > 0


def is_field_class_declarator(node: TsNode | Node):
    query = CPP_LANGUAGE.query("""
    (
    (field_declaration 
        (class_specifier)
    ) @field_declaration
    )
    """)

    if isinstance(node, Node):
        node = node.ts_node

    capture = query.captures(node)
    return len(capture) > 0


def collect_class_data(class_name, fields) -> Node:
    fields_text = '\n'.join('    ' + field.text.decode('utf-8')
                            for field in fields)
    code = f"""
class {class_name} {{
{fields_text}
}};
    """
    return parse(code).root

def collect_class_func(class_name, funcs) -> Dict[str, Node]:
    func_text = {}
    for f in funcs:
        type = f.child_by_field_name('type').text.decode('utf-8')
        d = f.child_by_field_name('declarator')
        stmt = f.child_by_field_name('body').text.decode('utf-8')
        name = d.child_by_field_name('declarator').text.decode('utf-8')
        para = d.text.decode('utf-8')
        text = f"""
        {type} {class_name}::{para} {stmt}
        """
        node = parse(text).root
        for j in range(0, 100):
            # TOOD: use paramter type to unique the override function
            override = f"{class_name}.{name}.{j}"
            if override not in func_text:
                func_text[override] = node
                break
    return func_text
