import unittest
from tests import eva
from parser.EvaParser import eva_to_lst, to_block


class TestModule(unittest.TestCase):
    def setUp(self) -> None:
        self.eva = eva

    def test_module(self):
        lst = eva_to_lst(to_block(''
                                  '(module Math'
                                  '  (begin'
                                  '      (def abs (value)'
                                  '         (if (< value 0)'
                                  '           (- value) '
                                  '           value ) '
                                  '      )'
                                  ''
                                  '      (def square(x) '
                                  '          (* x x))'
                                  ''
                                  '      (var MAX_VALUE 1000)'
                                  '  )'
                                  ')'
                                  ''
                                  '((prop Math abs) (- 10))'
                                  ''))
        self.assertEqual(self.eva.eval(lst), 10)
