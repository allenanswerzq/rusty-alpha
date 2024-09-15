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

            int sum() {
                return c + 2;
            }
        };
        """
        print_graph(g)
        matches = query_class_data(g.root)
        self.assertEqual(len(matches), 4)
        self.assertEqual(get_class_name(g.root), 'Foo')
        data = collect_class_data(g.root)
        func = collect_class_data(g.root, is_func=True)
        print(data)
        print(func)



if __name__ == '__main__':
    unittest.main()
