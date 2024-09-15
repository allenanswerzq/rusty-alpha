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
            void bar();
            void * f = int(a, b);
        };
        """
        print_graph(g)
        matches = query_class_data(g.root)
        self.assertEqual(len(matches), 3)
        self.assertEqual(get_class_name(g.root), 'Foo')
        print(collect_class_data_text(g.root))


if __name__ == '__main__':
    unittest.main()
    