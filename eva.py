from environment import Environment
from transformer.transformer import Transformer


def _add(op1, op2):
    return op1 + op2


def _sub(op1, op2=None):
    if op2:
        return op1 - op2
    return -op1


def _mul(op1, op2):
    return op1 * op2


def _div(op1, op2):
    return op1 / op2


global_transformer = Transformer()

global_environment = Environment({
    None: None,
    True: True,
    False: False,

    'VERSION': '0.1',

    # built-in function for functional math
    '+': _add,
    '-': _sub,
    '*': _mul,
    '/': _div,

    # built-in functions for comparison
    '>': lambda op1, op2: op1 > op2,
    '>=': lambda op1, op2: op1 >= op2,
    '<': lambda op1, op2: op1 < op2,
    '<=': lambda op1, op2: op1 <= op2,
    '==': lambda op1, op2: op1 == op2,

    # built-in print
    'print': print,
})

global_built_in_variable_names = ['+', '-', '*', '/', '>', '>=', '<', '<=', '==']


class Function():
    """
    store a function's params
    """

    def __init__(self, params: list, body: str, env: Environment) -> None:
        self.params = params
        self.body = body
        self.env = env


class Eva():
    """
    Eva interpreter
    """

    def __init__(self, global_env=global_environment, transformer: Transformer = global_transformer):
        """
        Creat Eva instance with global environment
        :param global_env:
        """
        self.global_env = global_env
        self.transformer = transformer

    def eval(self, exp, env=None):
        """
        Evaluation an expression in the given environment
        :param exp: an expression
        :param env:
        :return:
        """

        if env is None:
            env = self.global_env

        # ------------------------------------------------------------
        # self evaluation expression
        # interpret number
        if self._isNumber(exp):
            return exp

        # interpret string
        if self._isString(exp):
            exp = exp[1:-1]
            if exp == 'True':
                return True
            if exp == 'False':
                return False
            if exp == 'None':
                return None
            return exp

        # ------------------------------------------------------------
        # Block declarations
        if exp[0] == 'begin':
            return self.__eval_block(exp, env)

        # ------------------------------------------------------------
        # Variable declaration
        if exp[0] == 'var':
            name, value, = exp[1], exp[2]
            env.record[name] = self.eval(value, env)
            return env.record[name]

        # ------------------------------------------------------------
        # Variable assignment: (set foo 10)
        if exp[0] == 'set':
            name, value, = exp[1], exp[2]
            return env.assign(name, self.eval(value, env))

        # ------------------------------------------------------------
        # Variable access
        if self._isVariableName(exp):
            return env.lookup(exp)

        # ------------------------------------------------------------
        # if expression:
        # only support: IF CONDITION SEQUENCE ALTERNATIVE
        # the default exp contains the ALTERNATIVE part
        # but a de-packing mechanism do NOT allowed that num of args is more that len of a sequence.
        # todo: if the alternative does not exist, return 0
        if exp[0] == 'if':
            _tag, condition, sequence, alternative = exp
            if self.eval(condition, env):
                return self.eval(sequence, env)
            return self.eval(alternative, env)

        if exp[0] == 'while':
            _tag, condition, body = exp
            result = 0  # no loop return 0
            while self.eval(condition, env):
                result = self.eval(body, env)
            return result

        # ------------------------------------------------------------
        # Function declarations: (def square (x) (* x x))
        #
        # Syntactic suger for: (var square (lambda (x) (* x x)))
        if exp[0] == 'def':
            varExp = self.transformer.transform_def_to_var_lambda(exp)
            return self.eval(varExp, env)

        # ------------------------------------------------------------
        # switch-expression: (switch (cond1, block1) ...)
        if exp[0] == 'switch':
            varExp = self.transformer.transform_switch_to_if(exp)
            return self.eval(varExp, env)

        # ------------------------------------------------------------
        # for-loop: (for init condition modifier body)
        # Syntactic suger for: (begin init (while condition (begin body modifier)))
        if exp[0] == 'for':
            varExp = self.transformer.transform_for_to_while(exp)
            return self.eval(varExp, env)

        # --------------------------------------------
        # Increment: (++ foo)
        #
        # Syntactic sugar
        # for: (set foo (+ foo 1))
        if exp[0] == '++':
            varExp = self.transformer.transform_inc_to_set(exp)
            return self.eval(varExp, env)
        # --------------------------------------------
        # Increment: (-- foo)
        #
        # Syntactic sugar
        # for: (set foo (+ foo 1))
        if exp[0] == '--':
            varExp = self.transformer.transform_sub_to_set(exp)
            return self.eval(varExp, env)

        # --------------------------------------------
        # Increment: (++ foo val)
        #
        # Syntactic sugar
        # for: (set foo (+ foo val))
        if exp[0] == '+=':
            varExp = self.transformer.transform_inc_val_to_set(exp)
            return self.eval(varExp, env)

        # --------------------------------------------
        # Increment: (-= foo val)
        #
        # Syntactic sugar
        # for: (set foo (- foo val))
        if exp[0] == '-=':
            varExp = self.transformer.transform_sub_val_to_set(exp)
            return self.eval(varExp, env)

        # ------------------------------------------------------------
        # lambda declarations: lambda (data) (* data 10))
        if exp[0] == 'lambda':
            _tag, params, body = exp
            fn = Function(
                params,
                body,
                env,  # Closure
            )
            return fn

        # ------------------------------------------------------------
        # Function calls:
        # (print 'hello' 'world')
        # (+ x 5)
        # (> foo bar)
        if isinstance(exp, (list, tuple)):
            # get function-name
            fn = self.eval(exp[0], env)

            # get its arguments
            args = [self.eval(arg, env) for arg in exp[1:]]

            # 1. built-in functions
            if callable(fn):
                return fn(*args)

            # 2. User-defined functions
            activation_record = {}
            for (index, param) in enumerate(fn.params):  # add all params to the active-environment
                activation_record[param] = args[index]
            activation_evn = Environment(
                activation_record,
                # env # ! dynamic closure, which parent-evn refers to where it's called.
                fn.env  # static closure, which parent-evn refers to where it's defined
            )
            return self.__eval_body(fn.body, activation_evn)

        raise RuntimeError(f"Un-implement: {exp}")

    def __eval_body(self, body, env):
        if body[0] == 'begin':
            return self.__eval_block(body, env)
        return self.eval(body, env)

    def __eval_block(self, val, env):
        block_env = Environment({}, env)
        block = val[1:]
        result = None
        for expression in block:
            result = self.eval(expression, block_env)
        return result

    @staticmethod
    def _isNumber(val):
        """

        :return: True: val is a number
        """
        return isinstance(val, (int, float))

    @staticmethod
    def _isString(val):
        # is a string and contained by ""
        return isinstance(val, str) and (val[0] == '"') and (val[-1] == '"')

    @staticmethod
    def _isVariableName(val):
        return isinstance(val, str) and \
            (val.isidentifier() or (val in global_built_in_variable_names))
