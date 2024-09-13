import unittest

from src.parser import parse_doc
from src.compiler import compile_graph
from src.printer import write_graph

class TestCompiler(unittest.TestCase):

    @parse_doc()
    def test_basic_compile(self, g):
        """
        const int c = 10;
        class Foo {
            int a;
            int b;

            void bar() {
                std::cout << "hello alpha" << endl;
            }

            int baz() {
                return a + b + 10;
            }
        };

        int sum(int a, int b) {
            return a + b;
        }
        """
        compile_graph(g)
        write_graph(g, "a.rs")


if __name__ == '__main__':
    unittest.main()