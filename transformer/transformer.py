class Transformer():
    """
    AST transformer
    """

    def transform_def_to_var_lambda(self, defExp: list) -> list:
        """
            Translate `def` -expressions(function declaration) into a variable declaration
        with a lambda expression

        :param defExp:
        :return:
        """
        _tag, name, params, body = defExp
        varExp = ['var', name, ['lambda', params, body]]
        return varExp

    def transform_switch_to_if(self, defExp: list) -> list:
        """
            Transform `switch` to nested `-if` expressions
        """
        _tag, *cases, = defExp
        if_exp = ['if',
                  None,  # condition
                  None,  # block
                  None  # else
                  ]
        cur = if_exp
        print(cur, cur[1])
        for i in range(0, len(cases) - 1):
            current_cond, current_block = cases[i]
            cur[1] = current_cond
            cur[2] = current_block

            next_case = cases[i + 1]
            next_cond, next_block = next_case

            # last `else` block, or next nest block
            cur[3] = (next_block if next_cond == 'else' else ['if', None, None, None])
            cur = cur[3]

        return if_exp

    def transform_for_to_while(self, defExp: list) -> list:
        """

        :param list:
        :return:
        """
        _tag, _init, condition, modifier, exp = defExp
        _while_exp = ['begin',
                      _init,
                      ['while', condition,
                       ['begin',
                        exp,
                        modifier]
                       ]
                      ]
        return _while_exp
