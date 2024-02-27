
## Abstract
 a succinct Interpreter for Eva, which supports:
- Self-evaluating expressions: integer numbers and strings.
- Mathematical binary operations: addition, subtraction, multiplication, and division, including any logical composition of them.
- Comparison operators: greater than (`>`), less than (`<`), greater than or equal to (`>=`), less than or equal to (`<=`), equals (`==`).
- Variable access.
- Block expressions.
- Branching: `if` conditions and `switch` statements.
- Loops: `while` and `for`.
- Lambda functions.
- Function declarations and calls: This includes native or built-in functions, as well as user-defined functions.
- Object-Oriented Programming: Ability to define a class and initialize it.
- Modules.


## IDE Setup
- **PyCharm**: Version 2022.3.2
- **Python**: Version 3.11
- **Relevant Third-party Libraries**:
  - `sexpdata`
  - `pyInstaller`


## Project Structure
- **modules/**: Contains modules for import location.
- **parser/**: Translates raw Eva language into list form, e.g., `(+ 1 3)` -> `['+', 1, 3]`.
- **tests/**: Houses test cases.
- **transformer/**: Utilizes syntactic sugar to translate an expression in Eva language to another logically identical form, e.g., `(++ i)` -> `(set i (+ i 1))`. This technique is also used to transform `for` loops into `while` loops, and `switch` statements into nested `if` conditions.
- **environment.py**: Defines the environment for Eva, which preserves variables in the current block, as well as in the parent environment.
- **eva.py**: Contains the main logic of the Interpreter.
- **main.py**: Serves as the entry point of the Interpreter.

## How to run
  To generate an executable file for your project, run the command `pyinstaller --onefile --name eva main.py` in the terminal, making sure you're in the directory where `main.py` is located. This process will create an executable named `eva` inside the `dist/` directory.
  Here is an example of how to use the code:

```
> eva -e "(+ 1 4)"
> 5
> eva -e "(+ (+ 1 3) (* 7 3))"
> 25
```

## code example
```
# self-evaluation: num & str
-3
5
"a string"

# math binary operations
(+ 1 2)
(- 2 3) 
(* 2 4) 
(/ 4 3) 
(+ (+ 1 3) (* 7 3))

# variable access
(var foo 47)
foo

# block
(begin
     (var foo 42)
     (set bar (* foo 2))
     (+ foo var)
)

# Branch if
# (if <condition> 
#     <consequent>
#     <alternative>)

(if (> x 0)
    (set y 10)
    (begin: 
        (set y 20))
)

# Switch: 
# (switch <condition1> <block1>
#        <condition2> <block2>
#         ....
#         <conditionN> <blockN>
#         <alternative>
#)

(switch ((> x 0) 100)
        ((< x 0) 200)
        (else 300)
)

# while 
# (while <condition> 
#        <block>)

(while (> x 0)
    (set x (- x 1))
    (set result (+ result x))
)

# for loop: 
# (for <init>
#     <condition>
#     <modifier>
#     <exp>)

(for (var x 10)
     (> x 0)
     (set x (- x 1))
    (print x)
)


# lambda functions: (lambda <args> <body>)

(lambda (x) (x * x))


# function declaration: 
# (def <name> <args> 
#    <body>)
#
# (def square (x)
#    (* x x)
# )

# call function: (<fn> <args>)
(square 10) 


# Class Defination and Initialization: 
#
# (class <name> <parent>
# 		<body>)
#
# (new <class> <args>)

(class Point null
    (begin
        (def constructor (this x y)
            (begin
                (set (prop this x) x)
                (set (prop this y) y)
            )
         )

        (def calc(this)
         (+ (prop this x) (prop this y))
        )
    )
)

(var p (new Point 10 20))

((prop p calc) p)


# Module: 
# (module <name> <body>)
# 
# (import <name>)

(module Math
  (begin
      (def abs (value)
         (if (< value 0)
           (- value)
           value )
      )

      (def square(x)
          (* x x))

      (var MAX_VALUE 1000)
  )
)

((prop Math abs) (- 10))
```
