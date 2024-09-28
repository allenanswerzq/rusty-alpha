from llmcc.ir import *


# assign name to node
class Assigner(Visitor):

    def __init__(self, g: Graph):
        self.scope = Scope()
        self.g = g

    def visit(self, node: Node, continue_down=False) -> Any:
        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                getattr(self, f"visit_{child.type}")(child)

            if continue_down:
                self.visit(child, continue_down=continue_down)

    def query_identifier(self, node: Node):
        query = Language(tree_sitter_cpp.language()).query(
            """
        (identifier) @identifier
        """
        )
        capture = query.captures(node.ts_node)
        if "identifier" in capture:
            ty = capture["identifier"][0]
            return Node(ts_node=ty).text

    def get_function_name(self, node) -> str:
        param = ""
        name = ""
        for child in node.children:
            if child.type == "qualified_identifier":
                name = child.text.replace("::", ".")
            elif child.type == "field_identifier":
                name = child.text
            elif child.type == "parameter_list":
                for sub in child.children:
                    identifier = self.query_identifier(sub)
                    if identifier:
                        if len(param) > 0:
                            param += ", "
                        param += re.sub(identifier + "$", "", sub.text, count=1).strip()
            elif child.type == "identifier":
                # assert False, node.text
                # construct function like
                # TODO: we should only have the signature, not the full definition
                return node.text
            else:
                # assert False, child.type
                return node.text

        assert len(name), node.parent.text
        if len(param) > 0:
            name += ".(" + param + ")"
        else:
            name += ".()"
        return name

    def assign_name(self, name):
        # The node which a name should exist
        root = self.scope.root
        assert root

        if root.name:
            self.g.node_map.pop(root.name)

        qualified_name = name
        if self.scope.parent:
            outer = self.scope.parent.root
            if outer:
                assert outer.name, outer.text
                qualified_name = outer.name + "." + name

        root.name = qualified_name
        self.g.node_map[qualified_name] = root.id

    def visit_namespace_identifier(self, node: Node) -> Any:
        self.assign_name(node.text)

    def visit_function_declarator(self, node: Node) -> Any:
        self.assign_name(self.get_function_name(node))

    def visit_pointer_declarator(self, node: Node) -> Any:
        self.visit(node)

    def visit_type_identifier(self, node: Node) -> Any:
        assert isinstance(node.parent, Node)
        assert node.parent
        if node.parent.is_complex_type():
            self.assign_name(node.text)
        else:
            pass
            # funciton like: Node* func() {}
            # log.warn(node.parent.ts_node)

    def visit_identifier(self, node: Node) -> Any:
        self.assign_name(node.text)

    # -----------------------------------------------------------------------------------------
    def assign_scope(self, node, continue_down=False):
        self.scope = Scope(root=node, parent=self.scope)
        self.visit(node, continue_down=continue_down)
        self.scope = self.scope.parent

    def visit_preproc_def(self, node: Node) -> Any:
        self.assign_scope(node)

    def visit_declaration(self, node: Node) -> Any:
        self.assign_scope(node, continue_down=True)

    def visit_field_identifier(self, node: Node) -> Any:
        pass

    def visit_namespace_definition(self, node: Node) -> Any:
        self.assign_scope(node)

    def visit_preproc_ifdef(self, node: Node) -> Any:
        self.visit(node)

    def visit_struct_specifier(self, node: Node) -> Any:
        self.assign_scope(node)

    def visit_enum_specifier(self, node: Node) -> Any:
        self.assign_scope(node)

    def visit_function_definition(self, node: Node) -> Any:
        self.assign_scope(node)

    def visit_field_declaration(self, node: Node) -> Any:
        self.visit(node)

    def visit_class_specifier(self, node: Node) -> Any:
        self.assign_scope(node)

    def visit_declaration_list(self, node: Node) -> Any:
        self.visit(node)

    def visit_field_declaration_list(self, node: Node) -> Any:
        self.visit(node)


def assign_name_graph(g: Graph):
    assigner = Assigner(g)
    return g.accept(assigner)
