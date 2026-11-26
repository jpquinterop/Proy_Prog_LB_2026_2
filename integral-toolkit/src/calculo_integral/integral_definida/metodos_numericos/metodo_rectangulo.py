import math, sumas_riemann as riemann, functions as fun

f = fun.functions

def n(a, b, f, n):
    return riemann.n(a, b, f, n)  

def n10(a,b,f):

    return n(a,b,f,10)

def n100(a,b,f):

    return n(a,b,f,100)

def n1000(a,b,f):

    return n(a,b,f,1000)

def n10000(a,b,f):
    
    return n(a,b,f,10000)