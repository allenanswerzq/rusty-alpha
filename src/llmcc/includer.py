import os

from llmcc.ir import *
from llmcc.parser import parse
from llmcc.config import *


def search_file(directory, filename) -> str:
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.join(root, filename)


class Includer(Visitor):

    def __init__(self, dir, tree):
        self.dir = dir
        self.tree = tree

    def visit(self, node: Node) -> Any:
        g = None
        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                ng = getattr(self, f"visit_{child.type}")(node, child)
                if ng: g = ng
        return g

    def visit_preproc_include(self, tree, node: Node) -> Graph:
        # TODO: this acutally is a recursive process..
        include_file = node.children[1].text.decode('utf-8')
        include_file = search_file(self.dir, include_file.replace('"', ''))
        log.debug(f"searching include {include_file}")
        if not include_file:
            return None
        old_src = tree.text
        with open(include_file, 'r') as f:
            inc_src = f.read()
            inc_len = len(inc_src)
        new_src = inc_src.encode('utf-8') + old_src
        tree.ts_node.edit(start_byte=0,
                          old_end_byte=0,
                          new_end_byte=inc_len,
                          start_point=(0, 0),
                          old_end_point=(0, 0),
                          new_end_point=(0, inc_len))
        ng = parse(new_src, self.tree)
        self.tree = ng
        return ng


def include_graph(g: Graph, dir: str) -> Graph:
    i = Includer(dir, g.tree)
    ng = g.accept(i)
    if ng: return ng
