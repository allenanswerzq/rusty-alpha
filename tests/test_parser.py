import unittest

from llmcc.parser import parse_doc
from llmcc.printer import print_graph

class TestParser(unittest.TestCase):

    @parse_doc()
    def test_basic_parse(self, g):
        """
        int main() {
            std::cout << "hello alpha" << endl;
        }
        """
        print_graph(g)



if __name__ == '__main__':
    unittest.main()
