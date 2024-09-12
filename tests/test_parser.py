import unittest
from src.parser import parse_doc

class TestParser(unittest.TestCase):

    @parse_doc()
    def test_basic_parse(self, g):
        """
        int main() {
            std::cout << "hello alpha" << endl;
        }
        """
        print(g.root.ts_node)



if __name__ == '__main__':
    unittest.main()
