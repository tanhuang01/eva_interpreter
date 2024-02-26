import unittest
from tests import eva, eva_to_lst


class TestClass(unittest.TestCase):

    def setUp(self) -> None:
        self.eva = eva

    def test_class(self):
        lst = eva_to_lst(''
                         '(begin'
                         '  (class Point null'
                         '      (begin'
                         '          (def constructor (this x y)'
                         '              (begin'
                         '                  (set (prop this x) x)'
                         '                  (set (prop this y) y)'
                         '              )'
                         '           )'
                         ''
                         '          (def calc(this) '
                         '           (+ (prop this x) (prop this y))'
                         '          )'
                         '      )'
                         '  )'
                         ''
                         '  (var p (new Point 10 20))'
                         ''
                         '  ((prop p calc) p)'
                         ')'
                         '')
        self.assertEqual(self.eva.eval(lst), 30)
