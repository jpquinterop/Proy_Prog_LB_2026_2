import math

f = {
    "x^2": lambda x: x**2,
    "sin": lambda x: math.sin(x),
    "cos": lambda x: math.cos(x),
    "e^x": lambda x: math.exp(x),
    }

def simple_13(a,b,f):
    ba = b-a
    fa = f(a)
    fb = f(b)
    fmid = f((a+b)/2)
    sum = 0 
    sum+=(ba/6)*(fa+(4*fmid)+fb)
    return sum

def compuesto13_n10(a,b,f):
    f0 = f(a)
    fn = f(b)
    sum1 = 0
    sum2 = 0
    h = (b-a)/10
    for i in range(1,(10/2)+1):
        xi = a + i*h
        if i % 2 == 0:
            sum1 += abs(f(xi))
        else:
            sum2 += abs(f(xi))

    totalSum = (h/3)*(f0 + (2*sum1) + (4*sum2) + fn)
    return totalSum

def compuesto13_n100(a,b,f):
    f0 = f(a)
    fn = f(b)
    sum1 = 0
    sum2 = 0
    h = (b-a)/100
    for i in range(1,100):
        xi = a + i*h
        if i % 2 == 0:
            sum1 += abs(f(xi))
        else:
            sum2 += abs(f(xi))

    totalSum = (h/3)*(f0 + (2*sum1) + (4*sum2) + fn)
    return totalSum

def compuesto13_n1000(a,b,f):
    f0 = f(a)
    fn = f(b)
    sum1 = 0
    sum2 = 0
    h = (b-a)/1000
    for i in range(1,1000):
        xi = a + i*h
        if i % 2 == 0:
            sum1 += abs(f(xi))
        else:
            sum2 += abs(f(xi))

    totalSum = (h/3)*(f0 + (2*sum1) + (4*sum2) + fn)
    return totalSum

def compuesto13_n10000(a,b,f):
    f0 = f(a)
    fn = f(b)
    sum1 = 0
    sum2 = 0
    h = (b-a)/10000
    for i in range(1,10000):
        xi = a + i*h
        if i % 2 == 0:
            sum1 += abs(f(xi))
        else:
            sum2 += abs(f(xi))

    totalSum = (h/3)*(f0 + (2*sum1) + (4*sum2) + fn)
    return totalSum

def compuesto13_n(a,b,f,n):
    f0 = f(a)
    fn = f(b)
    sum1 = 0
    sum2 = 0
    h = (b-a)/n
    for i in range(1, n):
        xi = a + i*h
        if i % 2 == 0:
            sum1 += abs(f(xi))
        else:
            sum2 += abs(f(xi))

    totalSum = (h/3)*(f0 + (2*sum1) + (4*sum2) + fn)
    return totalSum

def simple38(a,b,f):
    fa = f(a)
    fb = f(b)
    h = (b-a)/3
    f2ab = f((2*a+b)/3)
    fa2b = f((a+(2*b))/3)
    sum = 3*(h/8)*(fa + (3*f2ab) + (3*fa2b) + fb)

    return sum

def compuesto38_n12(a,b,f):
    h = (b - a) / 12
    f0 = abs(f(a))
    fn = abs(f(b))
    sum1 = 0   
    sum2 = 0   
    sum3 = 0   

    for i in range(1, 12):
        xi = a + i * h
        if i % 3 == 1:
            sum1 += abs(f(xi))
        elif i % 3 == 2:
            sum2 += abs(f(xi))
        else:
            sum3 += abs(f(xi))

    total = f0 + 3 * (sum1 + sum2) + 2 * sum3 + fn
    return 3 * (h/8) * total

def compuesto38_n120(a,b,f):
    h = (b - a) / 120
    f0 = abs(f(a))
    fn = abs(f(b))
    sum1 = 0   
    sum2 = 0   
    sum3 = 0   

    for i in range(1, 120):
        xi = a + i * h
        if i % 3 == 1:
            sum1 += abs(f(xi))
        elif i % 3 == 2:
            sum2 += abs(f(xi))
        else:
            sum3 += abs(f(xi))

    total = f0 + 3 * (sum1 + sum2) + 2 * sum3 + fn
    return 3 * (h/8) * total

def compuesto38_n1200(a,b,f):
    h = (b - a) / 1200
    f0 = abs(f(a))
    fn = abs(f(b))
    sum1 = 0   
    sum2 = 0   
    sum3 = 0   

    for i in range(1, 1200):
        xi = a + i * h
        if i % 3 == 1:
            sum1 += abs(f(xi))
        elif i % 3 == 2:
            sum2 += abs(f(xi))
        else:
            sum3 += abs(f(xi))

    total = f0 + 3 * (sum1 + sum2) + 2 * sum3 + fn
    return 3 * (h/8) * total

def compuesto38_n12000(a,b,f):
    h = (b - a) / 12000
    f0 = abs(f(a))
    fn = abs(f(b))
    sum1 = 0   
    sum2 = 0   
    sum3 = 0   

    for i in range(1, 12000):
        xi = a + i * h
        if i % 3 == 1:
            sum1 += abs(f(xi))
        elif i % 3 == 2:
            sum2 += abs(f(xi))
        else:
            sum3 += abs(f(xi))

    total = f0 + 3 * (sum1 + sum2) + 2 * sum3 + fn
    return 3 * (h/8) * total

def compuesto38_n(a, b, f, n):
    if n % 3 != 0:
        n += 3 - n % 3        

    h = (b - a) / n
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