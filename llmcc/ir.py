import re
import tree_sitter_cpp

from tree_sitter import Node as TsNode
from tree_sitter import Tree as TsTree
from tree_sitter import Language, Parser
from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Any, Optional, Tuple, Union, Type, List
from abc import ABC, abstractmethod

from llmcc.store import Store
from llmcc.config import *


class Node(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int = Field(default=None, description="unique id for every node")
    name: str = Field(default=None, description="full qualified name of the node.")
    parent: Optional["Node"] = Field(default=None, description="part of the node.")
    ts_node: TsNode = Field(default=None, description="tree sitter node.")
    knowledge_store: Optional[Store] = Field(
        default=None, description="kb related to this node."
    )
    summary_store: Optional[Store] = Field(
        default=None, description="multiple version storage for summary of this node."
    )
    code_store: Optional[Store] = Field(
        default=None, description="multiple version storage for rust code"
    )
    depend_store: Optional[Store] = Field(
        default=None, description="the stuff this node depends."
    )
    slice_store: Optional[Store] = Field(
        default=None, description="the storage save sliced stuff."
    )
    sym_table_store: Optional[Store] = Field(
        default=None, description="symbol table storage"
    )
    children: Optional[List["Node"]] = Field(default=[], description="children node.")

    @property
    def type(self) -> str:
        return self.ts_node.type

    @property
    def text(self) -> str:
        return self.ts_node.text

    @property
    def is_named(self) -> bool:
        return self.ts_node.is_named

    @property
    def start_point(self) -> int:
        return self.ts_node.start_point

    @property
    def end_point(self) -> int:
        return self.ts_node.end_point

    @property
    def rows(self) -> int:
        s = self.start_point
        e = self.end_point
        return e.row - s.row

    def child_by_field_name(self, name: str) -> Any:
        return self.ts_node.child_by_field_name(name)


class Visitor(ABC):

    @abstractmethod
    def visit(self, node: Node) -> Any:
        pass


class Context:
    pass


class Graph(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    root: Node = Field(default=None, description="root node for the ir graph")
    node_map: Dict[str, int] = Field(
        default=None, description="map node name to node id"
    )
    id_map: Dict[int, Node] = Field(default=None, description="map node it to node")

    # def __str__(self):
    #     return str(self.root.ts_node).replace("(", "\n(")

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit(self.root)

    def resolve_name(self, name: str, cur: Node) -> List[Node]:
        """Given a name resolve the node in the lowest scope."""
        level = len(cur.name.split("."))
        if cur.name.endswith(")"):
            # NOTE: function
            level -= 1
        # log.debug(f"resolving {name} for {cur.name} in level {level}")
        # get a node in the <= level
        # TODO: improve this algorithm
        resolved = []
        for node_name, node_id in self.node_map.items():
            parts = node_name.split(".")
            assert len(parts) > 0
            if parts[-1].startswith("(") and parts[-1].endswith(")"):
                # Function sybmol, We didn't make difference with the overload functions
                parts.pop()
            if len(parts) <= level and parts[-1] == name:
                resolved.append(self.id_map[node_id])
        return resolved


_id = 0


def create_node(g: Graph, ts_node: TsNode, parent: Node) -> Node:
    global _id
    _id += 1
    g.id_map[_id] = Node(ts_node=ts_node, parent=parent, id=_id)
    return g.id_map[_id]


# assign name to node
class Assigner(Visitor):

    def __init__(self, g: Graph):
        self.name = []
        self.g = g

    def visit(self, node: Node, continue_down=False) -> Any:
        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                getattr(self, f"visit_{child.type}")(child)

            elif continue_down:
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
            return ty.text.decode("utf-8")

    def function_name(self, node) -> str:
        assert node.type == "function_declarator"
        param = ""
        for child in node.children:
            if child.type == "qualified_identifier":
                name = child.text.decode("utf-8").replace("::", ".")
            elif child.type == "field_identifier":
                name = child.text.decode("utf-8")
            elif child.type == "parameter_list":
                for sub in child.children:
                    identifier = self.query_identifier(sub)
                    if identifier:
                        if len(param) > 0:
                            param += ", "
                        param += (
                            sub.text.decode("utf-8")
                            .replace(identifier, "")
                            .replace(" ", "")
                            .strip()
                        )
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
        if node.parent.name:
            self.g.node_map.pop(node.parent.name)

        name = node.text.decode("utf-8")
        if node.type == "function_declarator":
            name = self.function_name(node)

        node.parent.name = ".".join(self.name + [name])

        self.g.node_map[node.parent.name] = node.parent.id
        self.name.append(name)

    def visit_namespace_identifier(self, node: Node) -> Any:
        self.assign_name(node)

    def visit_function_declarator(self, node: Node) -> Any:
        self.assign_name(node)

    def visit_type_identifier(self, node: Node) -> Any:
        self.assign_name(node)

    def visit_declaration(self, node: Node) -> Any:
        pass

    def visit_identifier(self, node: Node) -> Any:
        pass

    def visit_field_identifier(self, node: Node) -> Any:
        pass

    def visit_namespace_definition(self, node: Node) -> Any:
        self.visit(node, continue_down=True)
        self.name.pop()

    def visit_preproc_ifdef(self, node: Node) -> Any:
        self.visit(node, continue_down=True)

    def visit_struct_specifier(self, node: Node) -> Any:
        self.visit(node, continue_down=True)
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
        self.visit(node, continue_down=True)
        self.name.pop()


def assign_name_graph(g: Graph):
    assigner = Assigner(g)
    return g.accept(assigner)
