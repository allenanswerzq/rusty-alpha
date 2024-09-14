from tree_sitter import Node as TsNode
from tree_sitter import Tree as TsTree
from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Any, Optional, Tuple, Union, Type, List
from abc import ABC, abstractmethod

from src.store import Store


class Node(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    ts_node: TsNode = Field(default=None, description="tree sitter node.")
    knowledge_store: Optional[Store] = Field(default=None, description="kb related to this node.")
    summary_store: Optional[Store] = Field(default=None, description="multiple version storage for summary of this node.")
    code_store: Optional[Store] = Field(default=None, description="multiple version storage for rust code")
    depends_store: Optional[Store] = Field(default=None, description="the stuff this node depends.")
    sym_table_store: Optional[Store] = Field(default=None, description="symbol table storage")
    children: Optional[List['Node']] = Field(default=[], description="children node.")

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
        return str(self.root.ts_node).replace('(', '\n(')

    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit(self.root)


def create_node(ts_node: TsNode) -> Node:
    return Node(
        ts_node=ts_node,
    )

