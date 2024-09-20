import tree_sitter_cpp as tscpp
from tree_sitter import Language, Parser

# Load the C++ language
CPP_LANGUAGE = Language(tscpp.language())

# Create a parser
parser = Parser(CPP_LANGUAGE)

# Sample C++ code to parse
cpp_code = """
#include <iostream>

int add(int a, int b) {
    return a + b;
}

int main() {
    std::cout << "Result: " << add(5, 3) << std::endl;
    return 0;
}
"""

# Parse the code
tree = parser.parse(bytes(cpp_code, "utf8"))


# Function to traverse the syntax tree
def traverse_tree(node, level=0):
    text = node.text.decode("utf8").replace("\n", "\\n")
    print("  " * level + f"{node.type}: {text}")
    for child in node.children:
        traverse_tree(child, level + 1)


# Traverse and print the syntax tree
print("Syntax Tree:")
traverse_tree(tree.root_node)

# Pretty print the syntax tree
print(tree.root_node)

# Find all function definitions
function_nodes = tree.root_node.children

for node in function_nodes:
    if node.type == "function_definition":
        function_name = (
            node.child_by_field_name("declarator")
            .child_by_field_name("declarator")
            .text.decode("utf8")
        )
        print(f"\nFound function: {function_name}")

        # Get function parameters
        parameters = node.child_by_field_name("declarator").child_by_field_name(
            "parameters"
        )
        if parameters:
            param_names = [
                param.child_by_field_name("declarator").text.decode("utf8")
                for param in parameters.children
                if param.type == "parameter_declaration"
            ]
            print(f"Parameters: {', '.join(param_names)}")
