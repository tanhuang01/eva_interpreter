import unittest
from tests import eva, eva_to_lst


class TestPrint(unittest.TestCase):
    def setUp(self) -> None:
        self.eva = eva

    def test_print(self):
        # sexpdata will remove "" automatically
        # self.eva.eval(eva_to_lst('print "All" "Assertion" "Passed"'))
        self.eva.eval(['print', '"All"', '"Assertions"', '"Passed"'])