from llmcc.ir import *


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
