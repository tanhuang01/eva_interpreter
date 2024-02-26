import unittest
from tests import eva, eva_to_lst


class TestLambda(unittest.TestCase):

    def setUp(self) -> None:
        self.eva = eva

    def test_basic_lambda(self):
        lst = eva_to_lst(''
                         '(begin'
                         '  (def onClick (callback) '
                         '      (begin'
                         '          (var x 10)'
                         '          (var y 20)'
                         '          (callback (+ x y))'
                         '      )'
                         '  )'
                         '  '
                         '  (onClick (lambda (data) (* data 10)) )'
                         ')'
                         '')
        # print(lst)
        self.assertEqual(self.eva.eval(lst), 300)

    def test_iile(self):
        """
        test immediately invode  lambda expression
        :return:
        """
        lst = eva_to_lst(''
                         '((lambda (x) (* x x)) 2)'
                         ''
                         '')
        # print(lst)
        self.assertEqual(self.eva.eval(lst), 4)

    def test_save_to_var(self):
        """
        save a lambda into a var and invoke it
        :return:
        """
        lst = eva_to_lst(''
                         '(begin'
                         '  (var square (lambda (x) (* x x))) '
                         '  (square 2)'
                         ')'
                         '')
        # print(lst)
        self.assertEqual(self.eva.eval(lst), 4)
