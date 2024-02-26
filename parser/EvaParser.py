from sexpdata import dumps, loads, Symbol


def eva_to_lst(raw):
    return remove_symbol(loads(raw))


def to_block(raw):
    return f"(begin {raw})"


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
