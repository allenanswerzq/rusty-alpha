import tree_sitter_cpp as tscpp

from tree_sitter import Language, Parser
from tree_sitter import Node as TsNode

from acc.ir import *
from acc.config import *

CPP_LANGUAGE = Language(tscpp.language())

class Slicer(Visitor):

    def __init__(self):
        pass

    def visit(self, node: Node) -> Any:
        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                getattr(self, f"visit_{child.type}")(child)

    def visit_preproc_ifdef(self, node: Node) -> Any:
        self.visit(node)

    def visit_struct_specifier(self, node: Node) -> Any:
        pass

    def visit_declaration(self, node: Node) -> Any:
        pass
    
    def visit_class_specifier(self, node: Node) -> Any:
        self.visit(node)


    def visit_function_definition(self, node: Node) -> Any:
        pass



def get_class_name(node: TsNode | Node):
    query = CPP_LANGUAGE.query(
        """
        (class_specifier
        (type_identifier) @class_name)
        """
    )

    if isinstance(node, Node):
        node = node.ts_node

    captures = query.captures(node)
    assert 'class_name' in captures
    return captures['class_name'][0].text.decode('utf-8')


def is_field_func_declarator(node: TsNode | Node):
    query = CPP_LANGUAGE.query(
    """
    (
    (field_declaration 
        (_) 
        (function_declarator)
    ) @field_declaration
    )
    """
    )

    if isinstance(node, Node):
        node = node.ts_node

    capture = query.captures(node)
    return len(capture) > 0


def collect_class_data_text(node: Node) -> str:
    class_name = get_class_name(node)
    fields = query_class_data(node)
    fields_text = '\n'.join('    ' + field.text.decode('utf-8') for field in fields)
    return f"""
class {class_name} {{
{fields_text}
}};
    """

def query_class_data(node: Node) -> Any:
    query = CPP_LANGUAGE.query(
    """
    (
    (comment)+ @comments
    (field_declaration 
        (primitive_type) 
    ) @field_declaration
    )
    (
    (comment)+ @comments
    (field_declaration 
        (type_identifier) 
    ) @field_declaration
    )
    """
    )

    decls = query.captures(node.ts_node)
    if len(decls) > 0:
        decls = decls['field_declaration']

    fields = [
        decl for decl in decls
        if not is_field_func_declarator(decl)
    ]
    # TODO: sort, add comment into Node related to it
    # TODO: add private and public for every field
    return fields

