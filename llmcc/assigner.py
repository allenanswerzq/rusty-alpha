from llmcc.ir import *
from llmcc.scoper import ScopeVisitor

# from llmcc.util import get_function_signature


# assign name to node
class Assigner(ScopeVisitor):

    def __init__(self, g: Graph):
        super().__init__(g)

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

    def get_function_signature(self, node: Node) -> str:
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
        self.assign_name(self.get_function_signature(node))

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

    def visit_field_identifier(self, node: Node) -> Any:
        pass


def assign_name_graph(g: Graph):
    assigner = Assigner(g)
    assigner.visit(g.root)
