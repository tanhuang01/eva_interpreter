import unittest
from tests import eva


class TestMath(unittest.TestCase):

    def setUp(self) -> None:
        self.eva = eva

    def test_add(self):
        self.assertEqual(self.eva.eval(['+', 1, 5]), 6)
        self.assertEqual(self.eva.eval(['+', ['+', 2, 7], 5]), 14)
        self.assertEqual(self.eva.eval(['+', 5, ['+', 2, 7]]), 14)
        self.assertEqual(self.eva.eval(['+', ['+', ['+', 1, 3], 8], ['+', 2, 7]]), 21)

    def test_sub(self):
        self.assertEqual(self.eva.eval(['-', 5, 3]), 2)
        self.assertEqual(self.eva.eval(['-', 5, ['-', 1, 2]]), 6)

    def test_mul(self):
        self.assertEqual(self.eva.eval(['*', 5, 5]), 25)
        self.assertEqual(self.eva.eval(['*', 5, ['*', 2, 4]]), 40)

    def test_op(self):
        self.assertEqual(self.eva.eval(['+', 10, ['*', 2, 4]]), 18)


if __name__ == '__main__':
    unittest.main()
