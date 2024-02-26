import unittest
from tests import eva, eva_to_lst


class TestIf(unittest.TestCase):

    def setUp(self) -> None:
        self.eva = eva

    def test_if(self):
        self.assertEqual(self.eva.eval(
            ['begin',
             ['var', 'x', 10],
             ['var', 'y', 0],

             ['if', ['>', 'x', 10],
              ['set', 'y', 20],
              ['set', 'y', 30],
              ],
             'y'
             ]
        ), 30)

    def test_if_eva(self):
        lst = eva_to_lst('''
            (begin 
                (var x 10)
                (var y 10)
                
                (if (> x 10)
                    (set y 20)
                    (set y 30)
                )
                y
            )
        ''')
        # print(lst)
        self.assertEqual(self.eva.eval(lst), 30)
