from eva import Eva
from sexpdata import dumps, loads, Symbol

eva = Eva()


def eva_to_lst(lst):
    return remove_symbol(loads(lst))


def remove_symbol(str_raw):
    """
    remove the 'Symbol' in the eva raw.
    e.g. `Symbol('*')` -> '*'
    :param str_raw:
    :return:
    """
    if isinstance(str_raw, list):
        return [remove_symbol(item) for item in str_raw]
    elif isinstance(str_raw, Symbol):
        return str_raw.value()
    else:
        return str_raw
