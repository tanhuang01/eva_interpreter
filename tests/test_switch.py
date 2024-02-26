import unittest
from tests import eva
from parser.EvaParser import eva_to_lst

class TestSwitch(unittest.TestCase):

    def setUp(self) -> None:
        self.eva = eva

    def test_basic_switch(self):
        lst = eva_to_lst(''
                         '(begin'
                         '  (var x 10)'
                         '  '
                         '  (switch ((> x 10) 100)'
                         '          ((< x 10) 200)'
                         '          (else 300)'
                         '  )'
                         ')'
                         '')
        self.assertEqual(self.eva.eval(lst), 300)
