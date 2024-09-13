import unittest

from src.compile import compile_doc

class TestCompiler(unittest.TestCase):
    @compile_doc()
    def test_basic_compile(self, c):
        """
        int main() {
            std::cout << "hello alpha" << endl;
        }
        """
        print(c)


if __name__ == '__main__':
    unittest.main()