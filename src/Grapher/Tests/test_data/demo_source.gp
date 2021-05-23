# Input a, b, and c
INPUT "Input a: " > a
INPUT "Input b: " > b
INPUT "Input c: " > c

# Define function f
f = a*x^2+b*x+c;

# Get value of f(x) at x = 0 -> f(0)
PRINT f(0);

# Find real roots of f
roots = SOLVE f IN REALS;

# Plot function f
PLOT f;
