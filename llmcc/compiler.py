import ell
import json

from llmcc.ir import *
from llmcc.config import *
from llmcc.parser import parse
from pydantic import BaseModel, Field

import tree_sitter_rust as tsrust
from tree_sitter import Language, Parser


class Data(BaseModel):
    explain: str = Field(description="simple explanation of the code.")
    target_code: str = Field(description="target code generated.")


class Compiler(Visitor):

    def __init__(self):
        pass

    @ell.simple(model="gpt-4-turbo")
    def compile_impl(self, node: Node):
        schema = json.dumps(Data.model_json_schema(), indent=4)
        code = node.text.decode("utf-8")
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
        log.info(f"compiling {node.type} {node.name}")
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
        parsed = parse(parsed.target_code, lan=Language(tsrust.language()))
        node.code_store.add_version({"parsed": parsed, "source_code": node})

    def visit(self, node: Node) -> Any:
        if node.type == "translation_unit" and node.depends_store:
            depends = node.depends_store.get_current_version()
            if "include_files" in depends:
                for include in depends["include_files"]:
                    self.compile(include.root)

        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                getattr(self, f"visit_{child.type}")(child)

    def visit_preproc_ifdef(self, node: Node) -> Any:
        self.visit(node)

    def visit_enum_specifier(self, node: Node) -> Any:
        self.compile(node)

    def visit_struct_specifier(self, node: Node) -> Any:
        self.visit_class_specifier(node)

    def visit_declaration(self, node: Node) -> Any:
        self.compile(node)

    def visit_class_specifier(self, node: Node) -> Any:
        assert node.depends_store
        depend = node.depends_store.get_current_version()
        data_node = depend["data"]
        func_nodes = depend["func"]
        assert data_node or func_nodes
        if data_node:
            self.compile(data_node)
        if func_nodes:
            for f, v in func_nodes:
                self.compile(v)

    def visit_function_definition(self, node: Node) -> Any:
        self.compile(node)


def compile_graph(g: Graph) -> Any:
    compiler = Compiler()
    return g.accept(compiler)
