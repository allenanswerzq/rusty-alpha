import unittest

from acc.parser import parse_doc
from acc.compiler import compile_graph
from acc.printer import write_graph, print_graph
from acc.slicer import *

class TestSlicer(unittest.TestCase):

    @parse_doc()
    def test_query(self, g):
        """
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
        """
        print_graph(g)
        slice_graph(g)



if __name__ == '__main__':
    unittest.main()
