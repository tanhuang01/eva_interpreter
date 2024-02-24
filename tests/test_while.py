import unittest
from tests import eva


class TestWhile(unittest.TestCase):
    def setUp(self) -> None:
        self.eva = eva

    def test_while_basic(self):
        self.assertEqual(self.eva.eval(['begin',
                                        ['var', 'counter', 0],
                                        ['var', 'result', 0],

                                        ['while', ['<', 'counter', 10],
                                         # result++
                                         # TODO: implement ['++', <expr>]
                                         ['begin',
                                          ['set', 'result', ['+', 'result', 1]],
                                          ['set', 'counter', ['+', 'counter', 1]],
                                          ]
                                         ],
                                        'result'
                                        ]), 10)
