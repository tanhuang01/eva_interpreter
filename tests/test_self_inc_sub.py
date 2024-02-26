import unittest
from tests import eva
from parser.EvaParser import eva_to_lst


class TestInc(unittest.TestCase):

    def setUp(self) -> None:
        self.eva = eva

    def test_inc(self):
        lst = eva_to_lst(''
                         '(begin '
                         '  (var result 0)'
                         '  (++ result)'
                         '  result'
                         ')'
                         '')
        self.assertEqual(self.eva.eval(lst), 1)

    def test_sub(self):
        lst = eva_to_lst(''
                         '(begin '
                         '  (var result 0)'
                         '  (-- result)'
                         '  result'
                         ')'
                         '')
        self.assertEqual(self.eva.eval(lst), -1)
