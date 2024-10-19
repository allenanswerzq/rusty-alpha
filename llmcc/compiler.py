import ell
import json
import tree_sitter_rust

from llmcc.ir import *
from llmcc.config import *
from llmcc.parser import parse
from llmcc.slicer import slice_graph
from llmcc.scoper import ScopeVisitor

from pydantic import BaseModel, Field
from tree_sitter import Language, Parser


class Data(BaseModel):
    explain: str = Field(description="simple explanation of the code.")
    target_code: str = Field(description="target code generated.")


def mock_func():
    return f"""{{
        "explain": "Mock",
        "target_code": "fn mock() {{}}"
    }}"""


class Compiler(ScopeVisitor):

    def __init__(self, g: Graph):
        super().__init__(g)

    @ell.mock(model="gpt-4-turbo", mock_func=mock_func)
    def compile_impl(self, node: Node):
        schema = json.dumps(Data.model_json_schema(), indent=4)
        code = node.text
        return [
            ell.system(
                f"""
            You are a distinguished software developer, give you some c++ code, you will convert it to rust code.
            - Do not add any additional code, only convert the given code to rust.

            **ONLY OUTPUT JSON OBJECT THAT FOLLOWS THIS JSON SCHEMA**
            ```json
            {schema}
            ```
            """
            ),
            ell.user(f"<cpp_code>\n {code} \n</cpp_code>"),
        ]

    def compile(self, node: Node):
        log.info(f"compiling {node.type} \n{node.text}")
        for i in range(3):
            try:
                unparsed = self.compile_impl(node)
                if unparsed.startswith("```json"):
                    unparsed = unparsed[7:]
                if unparsed.endswith("```"):
                    unparsed = unparsed[:-3]
                log.debug(unparsed)
                unparsed = json.loads(unparsed)
                parsed = Data.model_validate(unparsed)
                log.debug(parsed)
            except Exception as e:
                log.error(e)
                log.info(f"retrying compiling {node.type}")
                continue
            else:
                break

        if node.code_store is None:
            node.code_store = Store()

        assert parsed
        parsed = parse(parsed.target_code, lan=Language(tree_sitter_rust.language()))
        node.code_store.add_version({"parsed": parsed, "src_node": node})

    def visit_struct_specifier(self, node: Node) -> Any:
        self.visit_class_specifier(node)

    def visit_declaration(self, node: Node) -> Any:
        self.compile(node)

    def visit_class_specifier(self, node: Node) -> Any:
        if node.slice_store:
            slice = node.slice_store.get_current_version()
            data_node = slice["data"]
            func_nodes = slice["func"]
            nest_classes = slice["nest_classes"]
            assert data_node or func_nodes
            if data_node:
                self.compile(data_node)
            if func_nodes:
                for f, v in func_nodes.items():
                    self.compile(v)
            if nest_classes:
                for nest in nest_classes:
                    self.visit_class_specifier(nest)

    def visit_function_definition(self, node: Node) -> Any:
        self.compile(node)


def compile_graph(g: Graph) -> Any:
    compiler = Compiler(g)
    return g.accept(compiler)
