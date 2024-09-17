import unittest

from llmcc.parser import parse_doc
from llmcc.compiler import compile_graph
from llmcc.printer import write_graph, print_graph
from llmcc.slicer import *

class TestSlicer(unittest.TestCase):

    @parse_doc()
    def test_query(self, g):
        """
        namespace Slicer {
            enum Color {RED, BLACK, DOUBLE_BLACK};
            class Foo {
                // define a
                int *a;
                Bar b;
                int c;
                void * f = int(a, b);

                // function declarator
                void bar();

                inline int sum() {
                    return c + 2;
                }

                class Bar {
                    int d;
                    int e;

                    int bzz() {
                        return d + 2;
                    }
                };

            };

            class ABC {
                int a, b, c;
            };

            void Foo::bar() {
                printf("hello"); 
            }
        }

        class DCE {
            int d, c, e;
        };
        """
        print_graph(g)
        slice_graph(g)



if __name__ == '__main__':
    unittest.main()
