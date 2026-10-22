import math, functions as fun

f = fun.functions

def mid_n(a,b,f,n):
    h = (b-a)/n
    sum = 0

    for i in range(1,n):
        xi_1 = a + (i-1)*h
        xi = a + i*h
        midXi = (xi_1 + xi)/2
        sum += abs(f(midXi))

    return h*sum

def mid_n100(a,b,f):

    return mid_n(a,b,f,100)

def mid_n1000(a,b,f):

    return mid_n(a,b,f,1000)

def mid_n10000(a,b,f):

    return mid_n(a,b,f,10000)



