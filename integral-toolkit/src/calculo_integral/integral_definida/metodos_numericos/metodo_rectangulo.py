import math, sumas_riemann as riemann, functions as fun

f = fun.functions

def metodo_n(a,b,f,n):
    h = (b-a)/n
    sum = riemann.n(a,b,f,n)
    return sum*h

def metodo_n10(a,b,f):

    return metodo_n(a,b,f,10)

def metodo_n100(a,b,f):

    return metodo_n(a,b,f,100)

def metodo_n1000(a,b,f):

    return metodo_n(a,b,f,1000)

def metodo_n10000(a,b,f):
    
    return metodo_n(a,b,f,10000)