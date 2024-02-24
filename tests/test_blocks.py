import unittest
from tests import eva, eva_to_lst


class TestBlocks(unittest.TestCase):
    """

    """

    def setUp(self) -> None:
        self.eva = eva

    def test_block(self):
        self.assertEqual(self.eva.eval(['begin',
                                        ['var', 'x', 10],
                                        ['var', 'y', 20],
                                        ['+', ['*', 'x', 'y'], 30]
                                        ]), 230)

    def test_block_nested(self):
        self.assertEqual(self.eva.eval(['begin',  # nested blocks
                                        ['var', 'x', 10],
                                        ['begin',
                                         ['var', 'x', 20],
                                         'x'
                                         ],
                                        'x'
                                        ]), 10)

    def test_inner_block_looking_up_outer(self):
        self.assertEqual(self.eva.eval(['begin',  # inner block look up outer block variables
                                        ['var', 'value', 10],
                                        ['var', 'result',
                                         ['begin',
                                          ['var', 'x', ['+', 'value', 10]],
                                          'x'
                                          ]
                                         ],
                                        'result',
                                        ]), 20)

    def test_access_outer_block(self):
        self.assertEqual(self.eva.eval(['begin',  # access outer block
                                        ['var', 'data', 10],
                                        ['begin',
                                         ['set', 'data', 100],
                                         ],
                                        'data'
                                        ]), 100)

    def test_access_outer_block_eva(self):
        self.assertEqual(self.eva.eval(eva_to_lst('''
            (begin
                (var data 10)
                (begin 
                    (set data 100)
                )
                data
            )
        ''')), 100)


if __name__ == '__main__':
    unittest.main()
