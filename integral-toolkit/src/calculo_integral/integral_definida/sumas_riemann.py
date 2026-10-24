import functions as fun

f = fun.functions

def n(a,b,f,n):
    h = (b-a)/n
    sum = 0
    for i in range(0,n):
        xi = (a+i*h)
        sum += abs(f(xi))
    return sum*h

def n_10(a,b,f):

    return n(a,b,f,10)

def n_100(a,b,f):
    
    return n(a,b,f,100)

def n_1000(a,b,f):
    
    return n(a,b,f,1000)

def n_10000(a,b,f):
    
    return n(a,b,f,10000)