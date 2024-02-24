"""
    For defining an environment of a variable
"""


class Environment():

    def __init__(self, record: dict = None, parent: 'Environment' = None):  # forward declaration
        if record is None:
            record = {}
        self.record = record
        self.parent = parent

    def lookup(self, name: str):
        return self.__resolve(name).get(name)

    def define(self, name: str, val):
        self.record[name] = val

    def assign(self, name: str, val):
        self.__resolve(name)[name] = val
        return val

    def __resolve(self, name):
        if self.record.get(name) is not None:
            # # can not use `self.record.get(name)` directly
            # if it's `0` or sth refers to False, program goes wrong.
            return self.record

        if self.parent is None:
            raise Exception(f'the variable {name} is not found')

        return self.parent.__resolve(name)


if __name__ == '__main__':
    env = Environment()
    print(env.record)
