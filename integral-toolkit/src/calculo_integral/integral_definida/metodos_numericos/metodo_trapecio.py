import math, sumas_riemann as riemann, functions as fun

f = fun.functions

def compuesto_n(a,b,f,n):
    h = (b-a)/n
    fa = abs(f(a))
    fb = abs(f(b))
    sum = 2*riemann.n(a,b,f,n) + (fa+fb)
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

