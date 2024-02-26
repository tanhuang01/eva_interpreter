import unittest
from tests import eva
from parser.EvaParser import eva_to_lst, to_block


class TestModule(unittest.TestCase):
    def setUp(self) -> None:
        self.eva = eva

    def test_import(self):
        lst = eva_to_lst(to_block(''
                                  '(import Math)'
                                  ''
                                  '((prop Math abs) (- 10))'
                                  ''))
        self.assertEqual(self.eva.eval(lst), 10)
