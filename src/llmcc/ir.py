from tree_sitter import Node as TsNode
from tree_sitter import Tree as TsTree
from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Any, Optional, Tuple, Union, Type, List
from abc import ABC, abstractmethod

from llmcc.store import Store


class Node(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
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
    depends_store: Optional[Store] = Field(
        default=None, description="the stuff this node depends."
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
    tree: TsTree = Field(default=None, description="ts tree")

    def __str__(self):
        return str(self.root.ts_node).replace("(", "\n(")

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit(self.root)


def create_node(ts_node: TsNode, parent: Node) -> Node:
    return Node(ts_node=ts_node, parent=parent)


# assign name to node
class Assigner(Visitor):

    def __init__(self):
        self.name = []

    def visit(self, node: Node) -> Any:
        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                # print(f"visiting {child.type}")
                getattr(self, f"visit_{child.type}")(child)

    def assign_name(self, node):
        name = node.text.decode("utf-8").replace("::", ".")
        if node.type == "function_declarator":
            name = name.split("(")[0]
        node.parent.name = ".".join(self.name) + "." + name
        self.name.append(name)
        print(self.name)

    def visit_namespace_identifier(self, node: Node) -> Any:
        self.assign_name(node)

    def visit_function_declarator(self, node: Node) -> Any:
        self.assign_name(node)

    def visit_type_identifier(self, node: Node) -> Any:
        self.assign_name(node)

    def visit_identifier(self, node: Node) -> Any:
        pass

    def visit_field_identifier(self, node: Node) -> Any:
        # self.assign_name(node)
        pass

    def visit_declaration_list(self, node: Node) -> Any:
        self.visit(node)

    def visit_namespace_definition(self, node: Node) -> Any:
        self.visit(node)
        self.name.pop()

    def visit_preproc_ifdef(self, node: Node) -> Any:
        self.visit(node)

    def visit_struct_specifier(self, node: Node) -> Any:
        self.visit_class_specifier(node)

    def visit_field_declaration_list(self, node: Node) -> Any:
        self.visit(node)

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


def assign_name_graph(g: Graph):
    assigner = Assigner()
    return g.accept(assigner)
