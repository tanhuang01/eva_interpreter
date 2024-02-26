import unittest
from tests import eva, eva_to_lst


class TestMath(unittest.TestCase):

    def setUp(self) -> None:
        self.eva = eva

    def test_add(self):
        self.assertEqual(self.eva.eval(eva_to_lst('(+ 1 5)')), 6)
        self.assertEqual(self.eva.eval(eva_to_lst('(+ (+ 2 7) 5)')), 14)
        self.assertEqual(self.eva.eval(eva_to_lst('(+ 5 (+ 2 7))')), 14)
        self.assertEqual(self.eva.eval(eva_to_lst('(+ (+ (+ 1 3) 8) (+ 2 7))')), 21)

    def test_sub(self):
        self.assertEqual(self.eva.eval(eva_to_lst('(- 4 2)')), 2)
        self.assertEqual(self.eva.eval(eva_to_lst('(- 5 (- 1 2))')), 6)

    def test_mul(self):
        self.assertEqual(self.eva.eval(eva_to_lst('(* 5 5)')), 25)
        self.assertEqual(self.eva.eval(eva_to_lst('(* 5 (* 2 4))')), 40)

    def test_op(self):
        self.assertEqual(self.eva.eval(eva_to_lst('(+ 10 (* 2 4))')), 18)

    def test_comparison(self):
        self.assertFalse(self.eva.eval(eva_to_lst('(> 1 5)')))
        self.assertTrue(self.eva.eval(eva_to_lst('(< 1 5)')))
        self.assertTrue(self.eva.eval(eva_to_lst('(<= 5 5)')))
        self.assertTrue(self.eva.eval(eva_to_lst('(>= 5 5)')))
        self.assertTrue(self.eva.eval(eva_to_lst('(== 5 5)')))


if __name__ == '__main__':
    unittest.main()
