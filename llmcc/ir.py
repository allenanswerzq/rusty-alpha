import copy
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
        return self.ts_node.type if self.ts_node else None

    @property
    def scope_name(self) -> str:
        return self.name.split(".")[-1]

    @property
    def text(self) -> str:
        return self.ts_node.text.decode("utf-8") if self.ts_node else None

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

    @property
    def scope_str(self) -> str:
        scope_dict = {
            "class_specifier": "class",
            "struct_specifier": "struct",
            "enum_specifier": "enum",
            "namespace_definition": "namespace",
        }
        return scope_dict[self.type]

    def child_by_field_name(self, name: str) -> Any:
        return self.ts_node.child_by_field_name(name)

    def is_complex_type(self) -> bool:
        return self.type in [
            "class_specifier",
            "struct_specifier",
            "enum_specifier",
        ]

    def is_function(self) -> bool:
        return self.type in ["function_definition"]

    def is_class(self) -> bool:
        return self.type in [
            "class_specifier",
            "struct_specifier",
        ]


class Visitor(ABC):

    @abstractmethod
    def visit(self, node: Node) -> Any:
        pass


class Context:
    pass


class Scope:
    def __init__(
        self, root: Node = None, parent: "Scope" = None, child: "Scope" = None
    ):
        self.root = root
        self.nodes: Dict[str, Node] = {}
        self.parent = parent
        self.child = child

        if root is not None and root.name is not None:
            self.define(root.scope_name, root)

    def define(self, name: str, value: Node):
        self.nodes[name] = value

    def resolve(self, name) -> List[Node]:
        ans = []
        for k, v in self.nodes.items():
            if name == k:
                ans.append(v)
            elif k.startswith(name + "("):
                # Handle override functions, we want to get all override functions at the same scope level
                ans.append(v)

        if len(ans) > 0:
            return ans
        elif self.parent is not None:
            return self.parent.resolve(name)
        else:
            raise NameError(f"Symbol '{name}' is not defined.")

    def get_scope_chain(self) -> List["Scope"]:
        chain = [self]
        start = self
        while start.parent is not None:
            start = start.parent
            chain.append(start)
        chain.pop()
        return chain[::-1]

    # def __deepcopy__(self, memo):
    #     # Create a new Scope instance
    #     new_copy = Scope()

    #     # Copy the root node if it exists
    #     new_copy.root = copy.deepcopy(self.root, memo)

    #     # Deepcopy the nodes dictionary
    #     new_copy.nodes = copy.deepcopy(self.nodes, memo)

    #     # Handle parent and child attributes
    #     new_copy.parent = copy.deepcopy(self.parent, memo) if self.parent else None
    #     new_copy.child = copy.deepcopy(self.child, memo) if self.child else None

    #     # Return the new deepcopy instance
    #     return new_copy


class Graph(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    root: Node = Field(default=None, description="root node for the ir graph")
    node_map: Dict[str, int] = Field(
        default=None, description="map node name to node id"
    )
    id_map: Dict[int, Node] = Field(default=None, description="map node it to node")
    tree: TsTree = Field(default=None, description="ts tree")
    global_vars: Dict[str, Node] = Field(
        default=None, description="global variable map"
    )

    # def __str__(self):
    #     return str(self.root.ts_node).replace("(", "\n(")

    def accept(self, visitor: "Visitor") -> Any:
        return visitor.visit(self.root)


_id = 0


def create_node(g: Graph, ts_node: TsNode, parent: Node, restart=False) -> Node:
    global _id
    if restart:
        _id = 0
    _id += 1
    # log.warn(f"{_id} {ts_node.type} {ts_node.text}")
    g.id_map[_id] = Node(ts_node=ts_node, parent=parent, id=_id)
    return g.id_map[_id]
