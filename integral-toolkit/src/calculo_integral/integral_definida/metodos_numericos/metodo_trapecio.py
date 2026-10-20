import math

f = {
    "x^2": lambda x: x**2,
    "sin": lambda x: math.sin(x),
    "cos": lambda x: math.cos(x),
    "e^x": lambda x: math.exp(x),
    }

def metodo_simple(a,b,f):
    h = b-a
    sum=0
    fa = f(a)
    fb = f(b)
    sum = (h/2)*(fa+fb)

    return sum

def metodo_n10(a,b,f):
    h = (b-a)/10
    fa = f(a)
    fb = f(b)
    sum = 0
    for i in range(1,10):
        xi = a + i*h
        sum+=abs(f(xi))

    sum+=(fa+fb)
    return (sum*h)/2

def metodo_n100(a,b,f):
    h = (b-a)/100
    fa = f(a)
    fb = f(b)
    sum = 0
    for i in range(1,100):
        xi = a + i*h
        sum+=abs(f(xi))

    sum+=(fa+fb)
    return (sum*h)/2

def metodo_n100(a,b,f):
    h = (b-a)/1000
    fa = f(a)
    fb = f(b)
    sum = 0
    for i in range(1,1000):
        xi = a + i*h
        sum+=abs(f(xi))

    sum+=(fa+fb)
    return (sum*h)/2

def metodo_n10000(a,b,f):
    h = (b-a)/10000
    fa = f(a)
    fb = f(b)
    sum = 0
    for i in range(1,10000):
        xi = a + i*h
        sum+=abs(f(xi))

    sum+=(fa+fb)
    return (sum*h)/2

def metodo_n(a,b,f,n):
    h = (b-a)/n
    fa = f(a)
    fb = f(b)
    sum = 0
    for i in range(1,n):
        xi = a + i*h
        sum+=abs(f(xi))

    sum+=(fa+fb)
    return (sum*h)/2