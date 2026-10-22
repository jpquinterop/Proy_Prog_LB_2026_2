import math

f = {
    "x^2": lambda x: x**2,
    "sin": lambda x: math.sin(x),
    "cos": lambda x: math.cos(x),
    "e^x": lambda x: math.exp(x),
    }

def n(a,b,f,n):
    h = (b-a)/n
    sum = 0
    for i in range(0,n):
        xi = (a+i*h)
        sum += abs(f(xi))
    return sum*h