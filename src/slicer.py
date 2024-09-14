from typing import Any
from src.ir import *
from src.ir import Node

class Slicer(Visitor):
    """Slicer does the job of deciding whether a node should be compiled"""
    def __init__(self) -> None:
        pass
    
    def visit(self, node: Node) -> Any:
        for child in node.children:

