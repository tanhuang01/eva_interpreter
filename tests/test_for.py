import unittest
from tests import eva, eva_to_lst

class TestFor(unittest.TestCase):

    def setUp(self) -> None:
        self.eva = eva

    def test_basic_for(self):
        lst = eva_to_lst(''
                         '(begin '
                         '  (var result 0)'
                         ''
                         '  (for (var i 0) (< i 5) (set i (+ i 1)) '
                         '      (set result (+ result i)))'
                         ''
                         '  result'
                         ')'
                         '')
        self.assertEqual(self.eva.eval(lst), 10)