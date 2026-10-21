import math

f = {
    "x^2": lambda x: x**2,
    "sin": lambda x: math.sin(x),
    "cos": lambda x: math.cos(x),
    "e^x": lambda x: math.exp(x),
    }

def compuesto_n(a,b,f,n):
    h = (b-a)/n
    fa = f(a)
    fb = f(b)
    sum = 0
    for i in range(1,n):
        xi = a + i*h
        sum+=abs(f(xi))

    sum=(sum*2)+(fa+fb)
    return (sum*h)/2

def simple(a,b,f):
    h = b-a
    sum=0
    fa = f(a)
    fb = f(b)
    sum = (h/2)*(fa+fb)

    return sum

def compuesto_n10(a,b,f):

    return compuesto_n(a,b,f,10)

def compuesto_n100(a,b,f):

    return compuesto_n(a,b,f,100)

def compuesto_n1000(a,b,f):

    return compuesto_n(a,b,f,1000)

def compuesto_n10000(a,b,f):

    return compuesto_n(a,b,f,10000)

