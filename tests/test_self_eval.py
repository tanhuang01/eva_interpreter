import unittest
from tests import eva


class TestSelfEval(unittest.TestCase):

    def setUp(self) -> None:
        self.eva = eva

    def test_num(self):
        self.assertEqual(self.eva.eval(1), 1)
        self.assertEqual(self.eva.eval(42), 42)

    def test_str(self):
        self.assertEqual(self.eva.eval('"hello"'), "hello")
        self.assertEqual(self.eva.eval('"world"'), "world")


if __name__ == '__main__':
    unittest.main()
