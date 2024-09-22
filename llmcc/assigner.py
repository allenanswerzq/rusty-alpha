from llmcc.ir import *


# assign name to node
class Assigner(Visitor):

    def __init__(self, g: Graph):
        self.name = []
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
            return ty.text.decode("utf-8")

    def get_function_name(self, node) -> str:
        # assert node.type == "function_declarator"
        param = ""
        name = ""
        for child in node.children:
            if child.type == "qualified_identifier":
                name = child.text.decode("utf-8").replace("::", ".")
            elif child.type == "field_identifier":
                name = child.text.decode("utf-8")
            elif child.type == "parameter_list":
                for sub in child.children:
                    identifier = self.query_identifier(sub)
                    # TODO: bug here, need to fix it
                    if identifier:
                        if len(param) > 0:
                            param += ", "
                        param += (
                            sub.text.decode("utf-8")
                            .replace(identifier, "")
                            .replace(" ", "")
                            .strip()
                        )
                        # log.warn(f"{node.text} {param} {identifier}")
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

    def assign_name(self, node):
        parent = node
        while parent:
            if parent.type in ["class_specifier", "struct_specifier", "enum_specifier"]:
                break
            parent = parent.parent

        if parent.name:
            # log.warn(f"trying to assign same name {parent.name} twice")
            self.g.node_map.pop(parent.name)

        name = node.text.decode("utf-8")
        full_name = ".".join(self.name + [name])
        parent.name = full_name
        # log.warn(f"assign class {full_name} --> {parent.id}")
        self.g.node_map[full_name] = parent.id
        self.name.append(name)

    def assign_func_name(self, node):
        parent = node
        while parent:
            if parent.type in ["function_definition"]:
                break
            parent = parent.parent

        if parent.name:
            # log.warn(f"trying to assign same name {parent.name} twice")
            self.g.node_map.pop(parent.name)

        name = self.get_function_name(node)
        full_name = ".".join(self.name + [name])
        # log.warn(f"assign func {full_name} --> {parent.id}")
        parent.name = full_name
        self.g.node_map[full_name] = parent.id
        self.name.append(name)

    def visit_namespace_identifier(self, node: Node) -> Any:
        self.assign_name(node)

    def visit_function_declarator(self, node: Node) -> Any:
        self.assign_func_name(node)

    def visit_pointer_declarator(self, node: Node) -> Any:
        self.visit(node)

    def visit_type_identifier(self, node: Node) -> Any:
        if node.parent.type in [
            "class_specifier",
            "struct_specifier",
            "enum_specifier",
        ]:
            self.assign_name(node)
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
        self.visit(node)
        self.name.pop()

    def visit_preproc_ifdef(self, node: Node) -> Any:
        self.visit(node)

    def visit_struct_specifier(self, node: Node) -> Any:
        self.visit(node)
        self.name.pop()

    def visit_enum_specifier(self, node: Node) -> Any:
        self.visit(node)
        self.name.pop()

    def visit_function_definition(self, node: Node) -> Any:
        self.visit(node)
        self.name.pop()

    def visit_field_declaration(self, node: Node) -> Any:
        for child in node.children:
            if child.type == "class_specifier":
                self.visit(child)
                self.name.pop()

    def visit_class_specifier(self, node: Node) -> Any:
        self.visit(node)
        self.name.pop()

    def visit_declaration_list(self, node: Node) -> Any:
        self.visit(node)

    def visit_field_declaration_list(self, node: Node) -> Any:
        self.visit(node)


def assign_name_graph(g: Graph):
    assigner = Assigner(g)
    return g.accept(assigner)
