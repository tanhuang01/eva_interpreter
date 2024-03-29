import unittest
from tests import eva
from parser.EvaParser import eva_to_lst, to_block


class TestClass(unittest.TestCase):

    def setUp(self) -> None:
        self.eva = eva

    def test_class(self):
        lst = eva_to_lst(to_block(''
                                  '(class Point null'
                                  '    (begin'
                                  '        (def constructor (this x y)'
                                  '            (begin'
                                  '                (set (prop this x) x)'
                                  '                (set (prop this y) y)'
                                  '            )'
                                  '         )'
                                  ''
                                  '        (def calc(this)' 
                                  '         (+ (prop this x) (prop this y))'
                                  '        )'
                                  '    )'
                                  ')'
                                  ''
                                  '(var p (new Point 10 20))'
                                  ''
                                  '((prop p calc) p)'
                                  ''))
        self.assertEqual(self.eva.eval_global(lst), 30)

    def test_class_inheritance(self):
        lst = eva_to_lst(to_block(''
                                  '(class Point null'
                                  '    (begin'
                                  '        (def constructor (this x y)'
                                  '            (begin'
                                  '                (set (prop this x) x)'
                                  '                (set (prop this y) y)'
                                  '            )'
                                  '         )'
                                  ''
                                  '        (def calc(this) '
                                  '         (+ (prop this x) (prop this y))'
                                  '        )'
                                  '    )'
                                  ')'
                                  ''
                                  '(class Point3D Point'
                                  '    (begin'
                                  '        (def constructor (this x y z)'
                                  '            (begin'
                                  '                ((prop (super Point3D) constructor) this x y)'
                                  '                (set (prop this z) z)'
                                  '            )'
                                  '         )'
                                  ''
                                  '        (def calc(this) '
                                  '         (+ ((prop (super Point3D) calc) this) '
                                  '             (prop this z))'
                                  '        )'
                                  '    )'
                                  ')'
                                  ''
                                  '(var p (new Point3D 10 20 30))'
                                  ''
                                  '((prop p calc) p)'
                                  ''))
        self.assertEqual(self.eva.eval_global(lst), 60)

