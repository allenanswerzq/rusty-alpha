from llmcc.ir import *


# assign name to node
class Assigner(Visitor):

    def __init__(self, g: Graph):
        self.scope = []
        self.g = g

    def visit(self, node: Node) -> Any:
        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                getattr(self, f"visit_{child.type}")(child)

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
                assert False, node.parent.type
            else:
                assert False, child.text

        assert len(name), node.parent.text
        if len(param) > 0:
            name += ".(" + param + ")"
        else:
            name += ".()"
        return name

    def assign_name(self, name):
        assert len(self.scope) > 0
        # The node which a name should exist
        parent = self.scope[-1]

        if parent.name:
            self.g.node_map.pop(parent.name)

        qualified_name = name
        if len(self.scope) > 1:
            outer = self.scope[-2]
            assert outer.name
            qualified_name = outer.name + "." + name

        parent.name = qualified_name
        self.g.node_map[qualified_name] = parent.id

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

    def visit_declaration(self, node: Node) -> Any:
        pass

    def visit_identifier(self, node: Node) -> Any:
        pass

    def visit_field_identifier(self, node: Node) -> Any:
        pass

    def visit_namespace_definition(self, node: Node) -> Any:
        self.scope.append(node)
        self.visit(node)
        self.scope.pop()

    def visit_preproc_ifdef(self, node: Node) -> Any:
        self.visit(node)

    def visit_struct_specifier(self, node: Node) -> Any:
        self.scope.append(node)
        self.visit(node)
        self.scope.pop()

    def visit_enum_specifier(self, node: Node) -> Any:
        self.scope.append(node)
        self.visit(node)
        self.scope.pop()

    def visit_function_definition(self, node: Node) -> Any:
        self.scope.append(node)
        self.visit(node)
        self.scope.pop()

    def visit_field_declaration(self, node: Node) -> Any:
        self.visit(node)

    def visit_class_specifier(self, node: Node) -> Any:
        self.scope.append(node)
        self.visit(node)
        self.scope.pop()

    def visit_declaration_list(self, node: Node) -> Any:
        self.visit(node)

    def visit_field_declaration_list(self, node: Node) -> Any:
        self.visit(node)


def assign_name_graph(g: Graph):
    assigner = Assigner(g)
    return g.accept(assigner)
