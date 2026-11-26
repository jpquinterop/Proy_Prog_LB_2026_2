from calculo_integral.exceptions.exception import controlar_integracion

@controlar_integracion
def compuesto_n(a, b, f, n):
    h = (b - a) / n
    interior = sum(abs(f(a + i * h)) for i in range(1, n))
    return h * (abs(f(a)) / 2 + interior + abs(f(b)) / 2)

@controlar_integracion
def simple(a,b,f):
    h = b - a
    fa = abs(f(a))
    fb = abs(f(b))
    return (h / 2) * (fa + fb)

def compuesto_n10(a,b,f):

    return compuesto_n(a,b,f,10)

def compuesto_n100(a,b,f):

    return compuesto_n(a,b,f,100)

def compuesto_n1000(a,b,f):

    return compuesto_n(a,b,f,1000)

def compuesto_n10000(a,b,f):

    return compuesto_n(a,b,f,10000)

