import math

import pytest

import functions as fun

F = fun.functions

VALORES = [
    ("c", 7, 1), ("x", 3, 3), ("-x", 3, -3), ("2x", 3, 6), ("x^2", 3, 9), ("x^3", -2, -8),
    ("x^4", 2, 16), ("x^2+1", 2, 5), ("x^3-2x+1", 2, 5), ("|x|", -4, 4), ("1/x", 4, 0.25),
    ("1/x^2", 2, 0.25), ("1/(1+x^2)", 1, 0.5), ("sqrt(x)", 9, 3), ("cbrt(x)", -8, -2),
    ("sin", math.pi / 2, 1), ("cos", 0, 1), ("sin^2", math.pi / 2, 1), ("cos^2", 0, 1),
    ("sin(x^2)", 0, 0), ("x*sin(x)", math.pi / 2, math.pi / 2),
    ("asin", 1, math.pi / 2), ("acos", 1, 0), ("atan", 1, math.pi / 4),
    ("e^x", 0, 1), ("e^-x", 0, 1), ("e^(x^2)", 0, 1), ("e^(-x^2)", 0, 1), ("2^x", 3, 8),
    ("ln", math.e, 1), ("log10", 1000, 3), ("log2", 8, 3), ("x*ln(x)", math.e, math.e),
    ("x*e^x", 1, math.e), ("semicirculo", 0, 1), ("semielipse", 0, 1),
    ("parabola", 2, 1), ("triangulo", 0, 1),
]

def test_el_registro_no_esta_vacio_y_todo_es_callable():
    assert len(F) > 30 and all(callable(f) for f in F.values())

@pytest.mark.parametrize("nombre,x,esperado", VALORES, ids=[v[0] for v in VALORES])
def test_valor_de_cada_funcion(nombre, x, esperado):
    assert F[nombre](x) == pytest.approx(esperado)

def test_todas_las_funciones_estan_cubiertas_por_los_tests():
    assert set(F) == {v[0] for v in VALORES}

def test_cbrt_conserva_el_signo():
    assert F["cbrt(x)"](-27) == pytest.approx(-3)
    assert F["cbrt(x)"](27) == pytest.approx(3)