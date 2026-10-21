import math

f = {
    "x^2": lambda x: x**2,
    "sin": lambda x: math.sin(x),
    "cos": lambda x: math.cos(x),
    "e^x": lambda x: math.exp(x),
    }

def metodo_n(a,b,f,n):
    h = (b-a)/n
    sum = 0

    for i in range(0,n):
        xi = (a+i*h)
        sum += abs(f(xi))

    return sum*h

def metodo_n10(a,b,f):

    return metodo_n(a,b,f,10)

def metodo_n100(a,b,f):

    return metodo_n(a,b,f,100)

def metodo_n1000(a,b,f):

    return metodo_n(a,b,f,1000)

def metodo_n10000(a,b,f):
    
    return metodo_n(a,b,f,10000)