<!--
vim:spell:nowrap:textwidth=79:colorcolumn=80
-->
# Let's Build A Simple Interpreter

> ___"If you don’t know how compilers work, then you don’t know how computers
> work. If you’re not 100% sure whether you know how compilers work, then you
> don’t know how they work."___ — *Steve Yegge*

## About
First learnt [this](https://ruslanspivak.com/lsbasi-part1/) during the senior
high time. Interpreters and compilers are fun, but somewhat hard, so here the
note is.

### Why would I study interpreters and compilers?
1. To write an interpreter or a compiler I have to have a lot of technical
skills that I need to use together.
2. I really want to know how computers work.
3. I want to create my own programming language or domain specific language.

### What are interpreters and compilers?

#### Interpreter
`source code` processing--> `Interpreter`
#### Compiler
`source code` preprocessing--> `Machine language` processing--> `Machine`

### What will we do in this series?
We'll create a simple interpreter for a large subset of [Pascal](https://en.wikipedia.org/wiki/Pascal_%28programming_language%29)
language. At the end of this series we'll have a working Pascal interpreter
and a source level debugger like Python's [pdb](https://docs.python.org/3/library/pdb.html).

Here is an example of a factorial function in `Pascal`:
```pascal
program factorial;

function factorial(n: integer): longint;
begin
    if n = 0 then
        factorial := 1
    else
        factorial := n * factorial(n - 1);
end;

var
    n: integer;

begin
    for n := 0 to 16 do
        writeln(n, '! = ', factorial(n));
end.
```

## Let's build a calculator firstly

### Lexer
In order for the interpreter to actually understand what to do with strings
like "3+5", it first needs to break the input into components called __tokens__.
A __token__ is an object that has a type and a value. This process is called
__lexical analysis__. The part of the interpreter that does it is called a
__lexical analyzer__, or __lexer__ in short, or __scanner__ and __tokenizer__.
And a __lexemes__ is a sequence of characters that form a token.
For example, we convert "3+5" into tokens `Token(INTEGER, 3)`,
`Token(PLUS, '+'` , `Token(INTEGER, 5)` and `Token(EOF, None)`, so that the
interpreter can deal with them easier.

### Parser
The process of recognizing a phrase in the stream of tokens is called __parsing__.
The part of an interpreter or compiler that preforms that job is called a
__parser__. They are also called __syntax analysis__ and __syntax analyzer__
respectively. In the example above, parser makes sure that the expression is of
the form of `INTEGER`, `PLUS` or `MINUS`, and `INTEGER`.

> Use ___context-free grammars___(___grammars___) or ___BNF___(Backus- Naur Form)
> (modified) to specifying the syntax of a programming language.
>
> For example:\
>   expr : factor ((MUL | DIV) factor)*\
>   factor : INTEGER

### Abstract-Syntax Tree (AST)
___AST___ is an ___intermediate representation___(___IR___), and is one of the
central data structure for our interpreter and future compiler projects.
For example, the AST for the expression `2 * 7 + 3` looks like:
```ebnf
+
├── *
│   ├── 2
│   └── 7
└── 3
```

### Associativity, precedence and unary operators
To deal with associativity and precedence, we can use these rules:
```ebnf
expr : term ((PLUS | MINUS) term)*
term : factor ((MUL | DIV) factor)*
factor : INTEGER | LPAREN expr RPAREN
```
As for unary operators:
```ebnf
factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN
```

### Final work
[Here](~/Documents/VimWiki/files/calc.py) is a working calculator. It supports
addition, subtraction, multiplication and division between integers and floats, 
parentheses are supported as well.

## Let's build a Pascal interpreter

### definition, compound statements and assignment statements
Here is a sample Pascal-like program to introduce new concepts:
```pascal
BEGIN
    BEGIN
        number := 2;
        a := number;
        b := 10 * a + 10 * number / 4;
        c := a - - b
    END;
    x := 11;
END.
```

To parse this program, these rules will be used:
```ebnf
program              : compound_statement DOT
compound_statement   : BEGIN statement_list END

                     | statements SEMI statement_list
statement            : compound_statement
                     | assignment_statement
                     | empty
assignment_statement : variable ASSIGN expr
variable             : ID
empty                :
factor               : PLUS factor
                     | MINUS factor
                     | INTEGER
                     | LPAREN expr RPAREN
                     | variable
```

With them, we can parse the sample and generate this AST:
```ebnf
AST
├── ○
│   ├── ○
│   │   └── :=
│   │       ├── number
│   │       └── 2
│   ├── ○
│   │   └── :=
│   │       ├── a
│   │       └── number
│   ├── ○
│   │   └── :=
│   │       ├── b
│   │       └── +
│   │           ├── *
│   │           │   ├── 10
│   │           │   └── a
│   │           └── /
│   │               ├── *
│   │               │   ├── 10
│   │               │   └── number
│   │               └── 4
│   └── ○
│       └── :=
│           ├── c
│           └── -
│               ├── a
│               └── -
│                   └── b
├── ○
│   └── :=
│       ├── x
│       └── 11
└── ○
```

### symbol table
To make `Assign` and `Var` work properly, we need to maintain a *symbol table*.
A ___symbol table___ is  an abstract data type(___ADT___) for tracking various
symbols in source code. For convenience, we use Python dictionary here. For
example, we declare a GLOBAL_SCOPE in `Interpreter`, and store and get values
via variables' names as keys.
After running the sample, we can get this by `print(interpreter.GLOBAL_SCOPE)`:
```python
{'number': 2, 'a': 2, 'b': 25, 'c': 27, 'x': 11}
```

### program header, variable declarations and divisions
Here is a complete Pascal program:
```pascal
PROGRAM Part10;
VAR
number     : INTEGER;
a, b, c, x : INTEGER;
y          : REAL;

BEGIN {Part10}
  BEGIN
    number := 2;
    a := number;
    b := 10 * a + 10 * number DIV 4;
    c := a - - b
  END;
  x := 11;
  y := 20 / 7 + 3.14;
  { writeln('a = ', a); }
  { writeln('b = ', b); }
  { writeln('c = ', c); }
  { writeln('number = ', number); }
  { writeln('x = ', x); }
  { writeln('y = ', y); }
END.  {Part10}
```

The ___program___ rule begins with the ___PROGRAM___ reserved keyword, the
program name, and a block that ends with a dot.
```pascal
PROGRAM Part10;
BEGIN
END.
```

The ___block___ rule combines a *declaration* rule and a *compound_statement*
rule.
```pascal
VAR
  number : INTEGER;

BEGIN
END
```

Pascal declaration have several parts and each part is optional. This article
cover the variable declaration part only. The ___declarations___ rule has
either a variable declaration sub-rule or it's empty.

Pascal is a statically typed language so every variable needs a declaration
that explicitly specifies its type. The ***variable_declaration*** section
starts with the ___VAR___ reserved keyword.
```pascal
VAR
  number    : INTEGER;
  a, b, c   : INTEGER;
  x         : REAL;
```

The ***type_spec*** rule is for handling *INTEGER* and *REAL* types and is used
in ***variable_declaration***.
```pascal
VAR
  a : INTEGER;
  b : REAL;
```

The division between integers and between floats are different. We use the
___DIV___ keyword for integer division and a forward slash / for float division.
For example, `20 DIV 7 = 2`, and `20 / 7 = 2.85714285714`

The ___factor___ rule is updated to handle both integer and float constants.
Constants are represented by ***INTEGER_CONST*** and ***REAL_CONST*** tokens,
and the ___INTEGER___ token will be used to represent the integer type.

New rules:
```ebnf
program              : PROGRAM variable SEMI block DOT
block                : declarations compound_statement
declarations         : VAR (variable_declaration SEMI)+
                     | empty
variable_declaration : ID (COMMA ID)* COLON type_spec
type_spec            : INTEGER | REAL
term                 : factor ((MUL|INTEGER_DIV| FLOAT_DIV) factor)*
factor               : PLUS factor
                     | MINUS factor
                     | INTEGER_CONST
                     | REAL_CONST
                     | LPAREN expr RPAREN
                     | variable
```
[Here](~/Documents/VimWiki/files/p10_enhanced.py) is a working interpreter.

### semantic analysis
When the parser has finished building the AST, we know that the program is
grammatically correct. However, it doesn't have type checking, so we need
semantic analysis to make it more concrete. The ___semantic analysis___ is  a
process to help us determine whether a program makes sense according to the
language definition.

The Pascal language requires:
- The variables must be declared before they are used
- The variables must have matching types when they are used in expressions
- There should be no duplicate declarations
- A name reference in a call to a procedure must refer to a declared procedure
- A procedure call must have the correct number of arguments and the arguments'
types must match those of formal parameters in the procedure declaration

With AST, we can satisfy these requirements easily so we'll interpret the code
in this way:\
source code--> `Lexer`--> Tokens--> `Parser`--> AST--> `Semantic Analyzer`-->
AST--> `Interpreter`--> output
(build the symbol table during the semantic analysis)

### symbols
To deal with things like type checking, we need symbols. A ___symbol___ is an
identifier of some program entity like a variable, subroutine, or built-in
type. For symbols to be useful they need to have at least the following
information about the program entities they identify:
- Name (for example, 'x', 'y', 'number')
- Category (Is it a variable, subroutine, or built-in type?)
- Type (INTEGER, REAL...)

To represent symbols in code, we can create a base `Symbol` class like:
```python
class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type
```
Here, we have *name* and optional *type* parameter(not all symbols may have a
type associated with them), and we'll encode the category of a symbol in the
class name itself, like `BuiltinTypeSymbol`, `VariableSymbol` etc.

Then, we can use a symbol table to track symbols. A ___symbol table___ is an
abstract data type(___ADT___) for tracking various symbols in source code. To
implement it, we can take it as a separate class with some helper methods,
and automate the process of building the symbol table when walking the AST.

For example, we define a `SymbolTable` and a `SymbolTableBuilder` class, where
we maintain a table in the first class, and have some `visit()` function in the
second class so that we can visit the AST before actually interpreting it.

[Here](~/Documents/VimWiki/files/p13_semantic_analyzer.py) is the full file.

### procedure
A ___procedure declaration___ is a construct that defines an identifier and
associates it with a block of Pascal code. By the way, the Pascal procedures
don't have return statements and can be nested within each other.

#### declaration

##### without parameters
Here is an example of procedure without parameters:
```pascal
PROGRAM Part12;
VAR
   a : INTEGER;

PROCEDURE P1;
VAR
   a : REAL;
   k : INTEGER;

   PROCEDURE P2;
   VAR
      a, z : INTEGER;
   BEGIN {P2}
      z := 777;
   END;  {P2}

BEGIN {P1}

END;  {P1}

BEGIN {Part12}
   a := 10;
END.  {Part12}
```

We can update the *declaration* grammar rule to:
```ebnf
declarations         : VAR (variable_declaration SEMI)+    (* variable *)
                     | (PROCEDURE ID SEMI block SEMI)*  (* declaration *)
                     | empty
```

##### with parameters
Here is an example of procedure with parameters:
```pascal
program Main;
   var x, y: real;

   procedure Alpha(a, b : integer; c : real); { parameters }
      var y : integer;
   begin
      x := a + x + y;
   end;

begin { Main }

end.  { Main }
```

Here is the new *declaration* grammar rule :
```ebnf
declarations          : VAR (variable_declaration SEMI)+
                      | (PROCEDURE ID [LPAREN formal_parameter_list RPAREN] SEMI block SEMI)*
                      | empty
formal_parameter_list : formal_parameters
                      | formal_parameters SEMI formal_parameters
formal_parameters     : ID (COMMA ID)* COLON type_spec
```

#### call
To make our interpreter actually deal with a procedure call, we should make
parser construct the AST and make semantic analyzer and interpreter don't throw
any errors when walking the AST.

That's easy, just add an `ProcedureCall` AST node, update "statements" rule, and
add an empty `visit_ProcedureCall` method in `Interpreter` class.

### memory system
A memory system is a system for storing and accessing data in memory. We used
Python dictionary as the memory system before. However, it's not suitable for
procedure calls, and many other things.

The new memory system is a stack data structure that holds dictionary-like
objects as elements. The stack is called the ***call stack***, and elements are
called ***activation records***, or just __frames__. In fact, every scope symbol
table below is a single activation record.

> [!NOTE]
> The `scope` section below is outdated though still worth reading. They were
introduced in part 15, and the memory system is introduced in part 17.

#### scope
A ___scope___ is a textual region of a program where a name can be used. Pascal
programs are said to be ___lexically scoped___(or ___statically scoped___)
since lexical keywords like *program* and *end* demarcate the textual
boundaries of a scope.
With scopes, we can use isolated name space, re-use the same name in different
scopes and re-declare a variable with the same name in a nested scope.

To implement the concept of a scope in code, we'll use a ___scoped symbol
table___, which is basically a symbol table with a few modifications, that is,
adding scope names and levels.

##### nested scope
In this program, we have nested scope:
```pascal
PROGRAM Main;                       { x_1  y_1  Alpha_1         }
   VAR x, y: REAL;                  {  |    |      |            }
                                    {  |    |      |            }
   PROCEDURE Alpha(a : INTEGER);    {  |           |    a_2 y_2 }
      VAR y : INTEGER;              {  |           |     |   |  }
   BEGIN                            {  |           |     |   |  }
      x := a + x + y;               {  |           |     |   |  }
   END;                             {  |           |     |   |  }
                                    {  |    |      |            }
BEGIN { Main }                      {  |    |      |            }
                                    {  |    |      |            }
END.  { Main }                      {  |    |      |            }
```

`a` and `y` in procedure `Alpha` are only accessible in that procedure, and the
variable declaration of `y` inside `Alpha` override that in global scope.

To implement it in code, we create a separate *scoped symbol table* to represent
the *global scope*, and construct a new instance of `ScopedSymbolTable` every
time we enter a new nested scope. Also, we assign the newly created scope to
the instance variable *current_scope* and other visitor methods that insert or
look up symbols will use it.

##### scope tree
To represent the nested relationship between the *global scope* and *Alpha
scope*, we can chain the tables together. In code, we add a variable
*enclosing_scope* that will hold a pointer to the scope's enclosing scope, and
update the *visit_Program* and *visit_ProcedureDecl* methods to create an
actual link to the scope's enclosing scope.

##### name resolution
*Lexically (statically) scoped* languages like Pascal follow ___the most
closely nested scope___ rule when it comes to name resolution. It means that,
in every scope, a name refers to its lexically closet declaration.
Take the program above for example, the assignment statement is actually
`x_1 := a_2 + x_1 + y_2`.

To implement it, we update the `lookup` function to search up recursively.

However, it leads to the "Duplicate declarations" when declaring a variable in
child-scope that has same name as in father-scope. This is easy to fix by
sending a `current_scope_only` parameter to tell `lookup` function whether
search up recursively or not.

#### call stack

### source-to-source compiler
A ___source-to-source compiler___ is compiler that translates a program in some
source language into a program in the same (or almost the same) source
language. We'll write a source-to-source compiler that takes a Pascal program
as an input and outputs a Pascal-like program where every name is subscripted
with a corresponding scope level, and, in addition to that, every variable
reference also has a type indicator.
For example, we'll take this as the input:
```pascal
PROGRAM Main;
   VAR x, y: REAL;

   PROCEDURE Alpha(a : INTEGER);
      VAR y : INTEGER;
   BEGIN
      x := a + x + y;
   END;

BEGIN { Main }

END.  { Main }
```
And this as the output:
```pascal
PROGRAM Main0;
   VAR x1 : REAL;
   VAR y1 : REAL;
   PROCEDURE Alpha1(a2 : INTEGER);
      VAR y2 : INTEGER;

   BEGIN
      <x1:REAL> := <a2:INTEGER> + <x1:REAL> + <y2:INTEGER>;
   END; {END OF Alpha}

BEGIN

END. {END OF Main}
```
The source-to-source compiler does these things:
1. separates declarations into separate lines
2. subscripts names with a number corresponding to the scope level
3. changes variable references into *<var_name:type>* format
4. adds a comment at the end of every block in the form of *{END OF ...}*

It helps us understand how name resolution works and is helpful when learning
about symbols, nested scopes, and name resolution.

And it can be implemented easily by extending the semantic analyzer.
<!-- TODO: implement a source-to-source compiler -->

### more features
To provide better error message pinpointing where in the code an issue happened,
we need to make the interpreter more user friendly.

#### error report
Instead of stack traces with very generic messages like `Invalid syntax`, we
would like to see something more useful like
`SyntaxError: Unexpected token -> Token(TokenType.SEMI, ‘;’, position=23:13)`.

To implement this, we define a `Error` base class (NOTE: the definition of this
class in part 15 is outdated, use `super().__init__(message)` instead of
`self.message = message`), which takes three arguments: *error_code* , *token* and
*message*, and custom some exceptions: `LexerError`, `ParserError`, and
`SemanticError`. Then we update the `error` methods respectively.

##### Lexer
We add new members `lineno` and `column` to locate tokens, with modified
`advance` to update them.

> Also, to make codes cleaner, we defines token types in the `TokenType`
> enumeration class, and automatically create reserved keywords from it. Then
> we can refactor `get_next_token` method to make it shorter and have a generic
> code that handles single-character tokens.

##### Parser
We update the `eat` method to call the modified `error` method, and refactor
the `declarations` method and move `procedure_declaration` into a separate
method.

##### Semantic Analyzer
We update `visit_VarDecl` and `visit_Var` methods to signal errors by calling
the `error` method, add a `log` method to both the `ScopedSymbolTable` and
`SemanticAnalyzer`, with a command line option `--scope` to turn scope logging
on and off. Also, we add empty `visit_Num` and `visit_UniNode` methods.

#### toggle scope output
Add a "--scope" command to turn scope output on/off.
