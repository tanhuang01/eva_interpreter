import unittest
from tests import eva, eva_to_lst


class TestInc(unittest.TestCase):

    def setUp(self) -> None:
        self.eva = eva

    def test_inc_val(self):
        lst = eva_to_lst(''
                         '(begin '
                         '  (var result 0)'
                         '  (+= result 5)'
                         '  result'
                         ')'
                         '')
        self.assertEqual(self.eva.eval(lst), 5)

    def test_sub_val(self):
        lst = eva_to_lst(''
                         '(begin '
                         '  (var result 0)'
                         '  (-= result 5)'
                         '  result'
                         ')'
                         '')
        self.assertEqual(self.eva.eval(lst), -5)
