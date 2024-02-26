# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from sexpdata import loads, dumps, Symbol
from tests import eva_to_lst, remove_symbol


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    s01 = loads('(+ 1 (* 2 (- 5 3)))')
    print(s01)
    print(remove_symbol(s01))

    # todo depack
    lst = ['a','b','c', None]
    lst[3] = 'd'
    a1, *a2 = lst
    print(a1)
    print(a2)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
