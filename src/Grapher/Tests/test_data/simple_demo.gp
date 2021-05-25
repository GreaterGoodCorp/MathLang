# Input a, b, and c and cast them to int
INPUT "Input a: " > a;
a = a AS INTEGER;
INPUT "Input b: " > b;
b = b AS INTEGER;
INPUT "Input c: " > c;
c = c AS INTEGER;

# Define function f
f = a*x^2+b*x+c;

# Get value of f(x) at x = 0 -> f(0)
PRINT f(0);

# Find real roots of f, and cast to string for printing
roots = SOLVE f AS REAL;

# Print real roots of f
PRINT "Real roots of f are", roots AS STRING;

# Plot function f
PLOT f;
