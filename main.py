# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import argparse
import os.path

from eva import Eva
from parser.EvaParser import to_block, eva_to_lst

eva = Eva()


def exal_global(expression):
    exp = to_block(expression)
    return eva.eval_global(eva_to_lst(exp))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Example script.")
    parser.add_argument('-e', type=str, help='execute the command line')
    parser.add_argument('-f', type=str, nargs='?', help="path to the .eva file to be executed")
    args = parser.parse_args()

    if args.e:
        result = exal_global(args.e)
        print(result)
    elif args.f:
        file = open(args.f, 'r', buffering=1024)
        src = file.read()
        result = exal_global(src)
        print(result)
