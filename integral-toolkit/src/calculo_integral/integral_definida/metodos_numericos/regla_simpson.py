import math, functions as fun

f = fun.functions

def h(a,b,n):
    return (b-a)/n

def compuesto13_n(a,b,f,n):
    if n % 2 != 0:
        n += 2 - n % 2 

    f0 = f(a)
    fn = f(b)
    sum1 = 0
    sum2 = 0
    h = h(a,b,n)
    for i in range(1, n):
        xi = a + i*h
        if i % 2 == 0:
            sum1 += abs(f(xi))
        else:
            sum2 += abs(f(xi))

    totalSum = (h/3)*(f0 + (2*sum1) + (4*sum2) + fn)
    return totalSum

def compuesto38_n(a, b, f, n):
    if n % 3 != 0:
        n += 3 - n % 3        

    h = h(a,b,n)
    f0 = abs(f(a))
    fn = abs(f(b))
    sum1 = sum2 = sum3 = 0

    for i in range(1, n):
        xi = a + i * h
        if i % 3 == 1:
            sum1 += abs(f(xi))
        elif i % 3 == 2:
            sum2 += abs(f(xi))
        else:
            sum3 += abs(f(xi))

    total = f0 + 3 * (sum1 + sum2) + 2 * sum3 + fn
    return 3 * h / 8 * total

def compuesto13_n10(a,b,f):

    return compuesto13_n(a,b,f,10)

def compuesto13_n100(a,b,f):

    return compuesto13_n(a,b,f,100)

def compuesto13_n1000(a,b,f):
    
    return compuesto13_n(a,b,f,1000)

def compuesto13_n10000(a,b,f):

    return compuesto13_n(a,b,f,10000)

def compuesto38_n12(a,b,f):

    return compuesto38_n(a,b,f,12)

def compuesto38_n120(a,b,f):

    return compuesto38_n(a,b,f,120)

def compuesto38_n1200(a,b,f):

    return compuesto38_n(a,b,f,1200)

def compuesto38_n12000(a,b,f):

    return compuesto38_n(a,b,f,12000)

def simple_13(a,b,f):
    ba = b-a
    fa = f(a)
    fb = f(b)
    fmid = f((a+b)/2)
    sum = 0 
    sum+=(ba/6)*(fa+(4*fmid)+fb)
    return sum

def simple38(a,b,f):
    fa = f(a)
    fb = f(b)
    h = (b-a)/3
    f2ab = f((2*a+b)/3)
    fa2b = f((a+(2*b))/3)
    sum = 3*(h/8)*(fa + (3*f2ab) + (3*fa2b) + fb)

    return sum