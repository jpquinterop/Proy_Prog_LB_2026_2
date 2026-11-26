import math, functions as fun

from calculo_integral.exceptions.exception import controlar_integracion

f = fun.functions

@controlar_integracion
def mid_n(a,b,f,n):
    h = (b-a)/n
    sum = 0

    for i in range(n):
        midXi = a + (i + 0.5) * h
        sum += abs(f(midXi))

    return h*sum

def mid_n100(a,b,f):

    return mid_n(a,b,f,100)

def mid_n1000(a,b,f):

    return mid_n(a,b,f,1000)

def mid_n10000(a,b,f):

    return mid_n(a,b,f,10000)