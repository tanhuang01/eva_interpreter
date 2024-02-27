import os.path
import pathlib

from environment import Environment
from transformer.transformer import Transformer
from parser.EvaParser import eva_to_lst

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

    def eval_global(self, expressions):
        return self.__eval_block(
            ['block',  # the name 'block' here is trivial, no used.
             expressions], self.global_env
        )

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
        # class-field assignment: (set (prop this x) x)
        if exp[0] == 'set':
            ref, value, = exp[1], exp[2]
            if ref[0] == 'prop':
                _tag, instance, prop_name = ref
                instance_evn = self.eval(instance, env)
                return instance_evn.define(
                    prop_name,
                    self.eval(value, env))

            # simple assignment
            return env.assign(ref, self.eval(value, env))

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
        # class declaration: (class <Name> <Parent> <body>)
        if exp[0] == 'class':
            _tag, name, parent, body = exp

            # A class is an environment! -- a stored methods and shared properties
            try:
                parent_env = self.eval(parent, env)
            except ValueError as e:  # parent is not defined yet
                parent_env = env

            class_env = Environment({}, parent_env)

            # body is evaluate as an environment
            self.__eval_class_block(body, class_env)

            # class is accessible by name
            return env.define(name, class_env)

        # ------------------------------------------------------------
        # super definition: (super <ClassName>)
        if exp[0] == 'super':
            _tag, class_name = exp
            return self.eval(class_name, env).parent

        # ------------------------------------------------------------
        # class instantiation: (new <class> <arguments>)
        if exp[0] == 'new':
            class_env = self.eval(exp[1], env)

            # an instance is also an environment
            # The `parent` component of the instance environment is set to its class
            instance_env = Environment({}, class_env)

            args = [self.eval(arg, env) for arg in exp[2:]]
            self.__call_user_defined_function(
                class_env.lookup('constructor'),
                [instance_env, *args])
            return instance_env

        # ------------------------------------------------------------
        # property access: (prop <instance> <name>)
        if exp[0] == 'prop':
            _tags, instance, name = exp
            instance_env = self.eval(instance, env)
            return instance_env.lookup(name)

        # ------------------------------------------------------------
        # module declaration: (module <name> <body>)
        if exp[0] == 'module':
            _tag, module_name, module_body = exp

            module_env = Environment({}, env)

            self.__eval_class_block(module_body, module_env)

            return env.define(module_name, module_env)

        # ------------------------------------------------------------
        # Module import: (import <module_name>)
        if exp[0] == 'import':
            _tag, module_name = exp

            f = open(f'./modules/{module_name}.eva', 'r', buffering=1024)
            module_src = f.read()
            f.close()
            module_body = eva_to_lst(f"(begin {module_src})")
            module_exp = ['module', module_name, module_body]
            return self.eval(module_exp, self.global_env)

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
            return self.__call_user_defined_function(fn, args)

        raise RuntimeError(f"Un-implement: {exp}")

    def __call_user_defined_function(self, fn, args: list):
        activation_record = {}
        for (index, param) in enumerate(fn.params):  # add all params to the active-environment
            activation_record[param] = args[index]
        activation_evn = Environment(
            activation_record,
            # env # ! dynamic closure, which parent-evn refers to where it's called.
            fn.env  # static closure, which parent-evn refers to where it's defined
        )
        return self.__eval_body(fn.body, activation_evn)

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

    def __eval_class_block(self, val, class_env):
        """
            the class with `begin`.
            but we do not need to create another Environment, or the Environment of the block
        will hold the relevant refers to the class, rather than class Environment.


        :param val:
        :param class_env:
        :return:
        """
        block = val[1:]
        result = None
        for expression in block:
            result = self.eval(expression, class_env)
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
