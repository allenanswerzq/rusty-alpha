import ell
import json

from pydantic import BaseModel, Field

from src.ir import *
from src.parser import parse
from src.printer import print_graph
from src.config import *

class Data(BaseModel):
    explain: str = Field(description="simple explanation of the code.")
    target_code: str = Field(description="target code generated.")

class Compiler(Visitor):

    def __init__(self):
        pass

    @ell.simple(model="gpt-4-turbo")
    def compile_impl(self, node: Node):
        schema = json.dumps(Data.model_json_schema(), indent=4)
        code = node.text.decode('utf-8')
        return [
            ell.system(f"""You are a distinguished software developer, give you some c++ code, you will convert it to rust code.

            **ONLY OUTPUT JSON OBJECT THAT FOLLOWS THIS JSON SCHEMA**
            ```json
            {schema}
            ```
            """),

            ell.user(f"<cpp_code>\n {code} \n</cpp_code>"),
        ]

    def compile(self, node: Node):
        unparsed = self.compile_impl(node)
        if unparsed.startswith("```json"):
            unparsed = unparsed[7:]
        if unparsed.endswith("```"):
            unparsed = unparsed[:-3]
        log.debug(unparsed)
        unparsed = json.loads(unparsed)
        parsed = Data.model_validate(unparsed)
        log.debug(parsed)
        if node.code_store is None:
            node.code_store = Store()
        node.code_store.add_version({
            "parsed": parsed,
            "source_code": node.text.decode('utf-8')
            })

    def visit(self, node: Node) -> Any:
        for child in node.children:
            if hasattr(self, f"visit_{child.type}"):
                getattr(self, f"visit_{child.type}")(child)

    def visit_preproc_ifdef(self, node: Node) -> Any:
        self.visit(node)
    
    def visit_struct_specifier(self, node: Node) -> Any:
        self.compile(node)

    def visit_declaration(self, node: Node) -> Any:
        self.compile(node)

    def visit_class_specifier(self, node: Node) -> Any:
        self.compile(node)

    def visit_function_definition(self, node: Node) -> Any:
        self.compile(node)


def compile_graph(g: Graph) -> Any:
    compiler = Compiler()
    return g.accept(compiler)
