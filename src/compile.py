import ell

from src.ir import *
from src.parser import parse


class Compiler(Visitor):

    def __init__(self):
        pass

    @ell.simple(model="gpt-4-turbo")
    def compile(self, code: str):
        """
        You are a distinguished software developer, give you some c++ code,
        you will convert it to rust code.
        """
        return f"<cpp_code>\n {code} \n</cpp_code>"

    def visit(self, node: Node) -> Any:
        return self.compile(node.text)


def compile_graph(g: Graph) -> str:
    compiler = Compiler()
    return compiler.visit(g.root)


def compile_doc():
    def decorator(func):
        def wrapper(*args, **kwargs):
            docstring = func.__doc__

            if docstring is None:
                raise ValueError("Function has no docstring to compile.")

            cpp_code = bytearray(docstring, "utf8")
            g = parse(cpp_code)
            c = compile_graph(g)

            return func(*args, **kwargs, c=c)
        return wrapper
    return decorator