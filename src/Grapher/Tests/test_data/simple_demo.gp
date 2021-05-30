# Input a, b, and c and cast them to int
a = 1;
b = 7;
c = -8;

# Define function f
f = a*x^2+b*x+c;

# Get value of f(x) at x = 0 -> f(0)
PRINT f(0);

# Find real roots of f, and cast to string for printing
roots = SOLVE f IN REAL;

# Print real roots of f
PRINT roots;

# Plot function f
PLOT f;
