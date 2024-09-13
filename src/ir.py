from tree_sitter import Node as TsNode
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
    children: Optional[List['Node']] = Field(default=[], description="children node.")

    @property
    def type(self) -> str:
        return self.ts_node.type

    @property
    def text(self) -> str:
        return self.ts_node.text

class Visitor(ABC):
    @abstractmethod
    def visit(self, node: Node) -> Any:
        pass

class Context:
    pass

class Graph(BaseModel):
    root: Node = Field(default=None, description="root node for the ir graph")

    def __str__(self):
        return str(self.root.ts_node).replace('(', '\n(')

    def accept(self, visitor: 'Visitor') -> Any:
        return visitor.visit(self.root)


def create_node(ts_node: TsNode) -> Node:
    return Node(
        ts_node=ts_node,
    )

