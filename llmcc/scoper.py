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

    def __init__(self, g: Graph, enforce_scope_name=True):
        self.scope = Scope()
        self.g = g
        self.enforce_scope_name = enforce_scope_name

    def visit(self, node: Node, continue_down=False) -> Any:
        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                getattr(self, f"visit_{child.type}")(child)

            elif continue_down:
                self.visit(child, continue_down=continue_down)

    def scope_visit(self, node, continue_down=False, func=None):
        if self.enforce_scope_name and node.name is None:
            raise ValueError(f"scope node should have name assigned {node.text}")

        if self.enforce_scope_name:
            log.debug(f"enter new scope {node.name}")

        self.scope = Scope(root=node, parent=self.scope)
        if func is not None:
            func(node, continue_down=continue_down)
        else:
            self.visit(node, continue_down=continue_down)
        self.scope = self.scope.parent

        if self.enforce_scope_name:
            log.debug(f"leave new scope {node.name}")

    def visit_declaration(self, node: Node) -> Any:
        root = self.scope.root
        if root.is_complex_type() or root.is_function():
            # local declaration
            # self.visit(node, continue_down=True)
            pass
        else:
            # global declaration
            log.debug("scope visit declaration")
            self.scope_visit(node, continue_down=True)

    def visit_namespace_definition(self, node: Node) -> Any:
        log.debug(f"scope visit namespace {node.name}")
        self.scope_visit(node)

    def visit_struct_specifier(self, node: Node) -> Any:
        log.debug("scope visit struct")
        self.scope_visit(node)

    def visit_enum_specifier(self, node: Node) -> Any:
        log.debug("scope visit enum")
        self.scope_visit(node)

    def visit_function_definition(self, node: Node) -> Any:
        log.debug("scope visit function definition")
        self.scope_visit(node)

    def visit_class_specifier(self, node: Node) -> Any:
        log.debug("scope visit class")
        self.scope_visit(node)

    def visit_preproc_def(self, node: Node) -> Any:
        pass
        # self.scope_visit(node)

    def visit_preproc_ifdef(self, node: Node) -> Any:
        pass
        # TODO: each should be in a new scope
        # self.visit(node)

    def visit_pointer_declarator(self, node: Node) -> Any:
        self.visit(node)

    def visit_declaration_list(self, node: Node) -> Any:
        self.visit(node)

    def visit_field_declaration_list(self, node: Node) -> Any:
        self.visit(node)

    def visit_field_declaration(self, node: Node) -> Any:
        if is_field_func_declarator(node):
            self.visit_field_func_declarator(node)
        elif is_field_class_declarator(node):
            self.visit_field_class_declarator(node)
        else:
            self.visit_field_data_declarator(node)

    def visit_field_func_declarator(self, node) -> Any:
        pass

    def visit_field_class_declarator(self, node) -> Any:
        pass

    def visit_field_data_declarator(self, node) -> Any:
        pass
