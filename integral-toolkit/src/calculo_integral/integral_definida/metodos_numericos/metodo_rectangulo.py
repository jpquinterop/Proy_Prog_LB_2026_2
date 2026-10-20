import math

f = {
    "x^2": lambda x: x**2,
    "sin": lambda x: math.sin(x),
    "cos": lambda x: math.cos(x),
    "e^x": lambda x: math.exp(x),
    }

def metodo_n10(a,b,f):
    h = (b-a)/10
    sum = 0

    for i in range(1,11):
        xi = (a+i*h)
        sum += abs(f(xi))

    return sum*h


def metodo_n100(a,b,f):
    h = (b-a)/100
    sum = 0

    for i in range(1,101):
        xi = (a+i*h)
        sum += abs(f(xi))

    return sum*h

def metodo_n1000(a,b,f):
    h = (b-a)/1000
    sum = 0

    for i in range(1,1001):
        xi = (a+i*h)
        sum += abs(f(xi))

    return sum*h

def metodo_n10000(a,b,f):
    h = (b-a)/10000
    sum = 0

    for i in range(1,10001):
        xi = (a+i*h)
        sum += abs(f(xi))

    return sum*h

def metodo_n(a,b,f,n):
    h = (b-a)/n
    sum = 0

    for i in range(1,n+1):
        xi = (a+i*h)
        sum += abs(f(xi))

    return sum*h