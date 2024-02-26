import unittest
from tests import eva, eva_to_lst


class TestFunctions(unittest.TestCase):
    def setUp(self) -> None:
        self.eva = eva

    # basic function
    def test_basic_function(self):
        self.assertEqual(self.eva.eval(['begin',
                                        ['def', 'square', ['x'],
                                         ['*', 'x', 'x']],
                                        ['square', 2],
                                        ]), 4)

    def test_complex_function(self):
        self.assertEqual(self.eva.eval(['begin',
                                        ['def', 'calc', ['x', 'y'],
                                         ['begin',
                                          ['var', 'z', 30],
                                          ['+', ['*', 'x', 'y'], 'z']
                                          ]
                                         ],
                                        ['calc', 10, 20]
                                        ]), 230)

    # closure:
    def test_closure_function(self):
        self.assertEqual(self.eva.eval(['begin',
                                        ['var', 'value', 100],

                                        ['def', 'calc', ['x', 'y'],
                                         ['begin',
                                          ['var', 'z', ['+', 'x', 'y']],

                                          ['def', 'inner', ['foo'],
                                           ['+', ['+', 'foo', 'z'], 'value']],

                                          'inner',
                                          ]
                                         ],

                                        ['var', 'fn', ['calc', 10, 20]],
                                        ['fn', 30],
                                        ]), 160)

    def test_recursive_function(self):
        """

        :return:
        """
        lst = eva_to_lst(''
                         '(begin'
                         '  (def factorial (x) '
                         '      (if (== x 1) '
                         '          1'
                         '          (* x (factorial (- x 1))))'
                         '  )'
                         ''
                         '  (factorial 5)'
                         ')'
                         '')
        # print(lst)
        self.assertEquals(self.eva.eval(lst), 120)
