from llmcc.ir import *
from llmcc.printer import *

import tree_sitter_cpp
from tree_sitter import Language, Parser


def is_field_func_declarator(node: Node):
    query = Language(tree_sitter_cpp.language()).query(
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

    capture = query.captures(node.ts_node)
    return len(capture) > 0


def is_field_class_declarator(node: Node):
    query = Language(tree_sitter_cpp.language()).query(
        """
    (
    (field_declaration 
        (class_specifier)
    ) @field_declaration
    )
    (
    (field_declaration 
        (struct_specifier)
    ) @field_declaration
    )
    """
    )

    capture = query.captures(node.ts_node)
    return len(capture) > 0


class ScopeVisitor(Visitor):

    def __init__(self, g: Graph):
        self.scope = Scope()
        self.g = g

    def visit(self, node: Node, continue_down=False) -> Any:
        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                getattr(self, f"visit_{child.type}")(child)

            elif continue_down:
                self.visit(child, continue_down=continue_down)

    def scope_impl(self, node, continue_down=False):
        self.scope = Scope(root=node, parent=self.scope)
        if hasattr(self, f"impl_{node.type}"):
            # If the subclass define customized function, run it
            getattr(self, f"impl_{node.type}")(node)
        else:
            self.visit(node, continue_down=continue_down)
        self.scope = self.scope.parent

    def visit_preproc_def(self, node: Node) -> Any:
        self.scope_impl(node)

    def visit_declaration(self, node: Node) -> Any:
        self.scope_impl(node, continue_down=True)

    def visit_namespace_definition(self, node: Node) -> Any:
        self.scope_impl(node)

    def visit_struct_specifier(self, node: Node) -> Any:
        self.scope_impl(node)

    def visit_enum_specifier(self, node: Node) -> Any:
        self.scope_impl(node)

    def visit_function_definition(self, node: Node) -> Any:
        self.scope_impl(node)

    def visit_class_specifier(self, node: Node) -> Any:
        self.scope_impl(node)

    def visit_preproc_ifdef(self, node: Node) -> Any:
        # TODO: each should be in a new scope
        self.visit(node)

    def impl_field_func_declarator(self, node) -> Any:
        pass

    def impl_field_class_declarator(self, node) -> Any:
        pass

    def impl_field_data_declarator(self, node) -> Any:
        pass

    def visit_field_declaration(self, node: Node) -> Any:
        if is_field_func_declarator(node):
            self.impl_field_func_declarator(node)
        elif is_field_class_declarator(node):
            self.impl_field_class_declarator(node)
        else:
            self.impl_field_data_declarator(node)

    def visit_declaration_list(self, node: Node) -> Any:
        self.visit(node)

    def visit_field_declaration_list(self, node: Node) -> Any:
        self.visit(node)
