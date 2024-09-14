import tree_sitter_cpp as tscpp

from tree_sitter import Language, Parser
from tree_sitter import Node as TsNode
from src.ir import *


def parse_from_file(file) -> Graph:
    with open(file, 'r') as f:
        return parse(f.read())


def parse(code: str | bytearray, old_tree = None) -> Graph:
    if isinstance(code, str):
        code = code.encode('utf-8')
    parser = Parser(Language(tscpp.language()))
    if old_tree:
        tree = parser.parse(bytes(code), old_tree)
    else:
        tree = parser.parse(bytes(code))
    return _tree_to_graph(tree)


def _tree_to_graph(tree) -> Graph:
    g = Graph()
    ts_root = tree.root_node
    ra_root = create_node(ts_root)
    g.root = ra_root

    # Use a stack for depth-first traversal
    stack = [(ts_root, ra_root)]

    while stack:
        ts_node, ra_node = stack.pop()

        for child in ts_node.children:
            child_ra_node = create_node(child)
            ra_node.children.append(child_ra_node)
            stack.append((child, child_ra_node))

    return g


def parse_doc():
    def decorator(func):
        def wrapper(*args, **kwargs):
            docstring = func.__doc__

            if docstring is None:
                raise ValueError("Function has no docstring to parse.")

            cpp_code = bytearray(docstring, "utf8")
            g = parse(cpp_code)

            return func(*args, **kwargs, g=g)
        return wrapper
    return decorator
