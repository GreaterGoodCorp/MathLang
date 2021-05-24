# Input a, b, and c
INPUT "Input a: " > a AS REAL;
INPUT "Input b: " > b AS REAL;
INPUT "Input c: " > c AS REAL;

# Define function f
f = a*x^2+b*x+c;

# Get value of f(x) at x = 0 -> f(0)
PRINT f(0);

# Find real roots of f
roots = SOLVE f AS REAL;

# Print real roots of f
PRINT "Real roots of f are", roots;

# Plot function f
PLOT f;
