# MathLang

MathLang is a specially designed programming language for maths.

## Features

MathLang can:

* Solve maths equations

* Plot 2D graphs of functions

* Differentiate and integrate any functions
  
_(and many more...)_

And what's the best thing about it? You can do any of this with a single line!

## Examples

A simple MathLang program looks like this:
```
# Define f(x)
# x is a reserved name for variables
f = 5*x^2 + 11*x - 16;

# Calculate f(x) at x = 2 -> f(2)
PRINT f(2);

# Solve f(x) for real roots
real_roots = SOLVE f IN REAL;

# Print real roots of f(x)
PRINT real_roots;

# Differentiate f(x)
f1 = DIFFERENTIATE f TO x;

# Print the first derivative of f(x)
PRINT f1;
```

## Documentation

_To be updated..._

## Limitation

As of now, the backend of MathLang is a MathLang-to-Python transpiler. In other words, Grapher source code is translated
to Python source code, which is then executed with a Python engine.

Hence, the performance of MathLang largely depends on Python itself (and various other dependencies).
The reason for this is that Python has a repertoire of libraries that make symbolic maths and plotting simpler to do.

However, in the future, we aim to either (1) develop a MathLang-to-C transpiler or (2) incorporate a Python-to-C
transpiler with the current Grapher-to-Python one.

## License

This project is licensed under the MIT licence.
