import unittest
from tests import eva


class TestVariables(unittest.TestCase):

    def setUp(self) -> None:
        self.eva = eva

    # ------------------------------------------------------------
    # Variables:
    def test_variables(self):
        self.assertEqual(self.eva.eval(['var', 'x', 10]), 10)
        self.assertEqual(self.eva.eval('x'), 10)
        self.assertEqual(self.eva.eval(['var', 'y', 100]), 100)
        self.assertEqual(self.eva.eval('y'), 100)
        self.assertEqual(self.eva.eval(['var', 'isUser', True]), True)

        self.assertEqual(self.eva.eval(['var', 'z', ['*', 2, 5]]), 10)
        self.assertEqual(self.eva.eval('z'), 10)
