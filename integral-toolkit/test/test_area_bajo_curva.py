import math

import pytest

from calculo_integral import functions as fun
from calculo_integral.integral_definida.metodos_numericos import metodo_rectangulo as rect
from calculo_integral.integral_definida.metodos_numericos import metodo_trapecio as trap
from calculo_integral.integral_definida.metodos_numericos import punto_medio as pm
from calculo_integral.integral_definida.metodos_numericos import regla_simpson as simp
from calculo_integral.integral_definida import sumas_riemann as riemann

F = fun.functions

CASOS = [
    ("c", 0, 5, 5.0),
    ("x", 0, 2, 2.0),
    ("x", -1, 1, 1.0),                      # |x| -> área 1, integral 0
    ("-x", 0, 2, 2.0),                      # f<0: el área es positiva
    ("x^2", 0, 3, 9.0),
    ("x^3", -1, 1, 0.5),                    # integral 0, área 1/2
    ("sin", 0, math.pi, 2.0),
    ("sin", 0, 2 * math.pi, 4.0),           # integral 0, área 4
    ("cos", 0, math.pi / 2, 1.0),
    ("e^x", 0, 1, math.e - 1),
    ("1/(1+x^2)", 0, 1, math.pi / 4),
    ("semicirculo", -1, 1, math.pi / 2),
]

METODOS = {
    "rectangulo": rect.n,
    "riemann": riemann.n,
    "punto_medio": pm.mid_n,
    "trapecio": trap.compuesto_n,
    "simpson_13": simp.compuesto13_n,
    "simpson_38": simp.compuesto38_n,
}

def _id(caso):
    return f"{caso[0]}[{caso[1]:.2f},{caso[2]:.2f}]"

@pytest.mark.parametrize("a_nombre", ["trapecio", "punto_medio", "simpson_13", "simpson_38"])
@pytest.mark.parametrize("caso", CASOS, ids=_id)
def test_area_converge_al_valor_exacto(a_nombre, caso):
    nombre, a, b, exacto = caso
    if nombre == "semicirculo":
        pytest.skip("derivada infinita en los extremos: converge lento")
    aprox = METODOS[a_nombre](a, b, F[nombre], 3000)
    assert aprox == pytest.approx(exacto, rel=1e-3, abs=1e-4)

@pytest.mark.parametrize("a_nombre", list(METODOS))
@pytest.mark.parametrize("caso", CASOS, ids=_id)
def test_area_nunca_es_negativa(a_nombre, caso):
    nombre, a, b, _ = caso
    assert METODOS[a_nombre](a, b, F[nombre], 60) >= 0

@pytest.mark.parametrize("a_nombre", list(METODOS))
def test_funcion_negativa_da_mismo_area_que_su_opuesta(a_nombre):
    metodo = METODOS[a_nombre]
    arriba = metodo(0, 2, lambda x: x**2, 60)
    abajo = metodo(0, 2, lambda x: -(x**2), 60)
    assert abajo == pytest.approx(arriba, rel=1e-12)

@pytest.mark.parametrize("a_nombre", ["rectangulo", "riemann", "punto_medio", "trapecio", "simpson_13", "simpson_38"])
def test_seno_un_periodo_completo_no_se_cancela(a_nombre):
    # Sin abs() esto daría ~0; con abs() debe dar ~4.
    aprox = METODOS[a_nombre](0, 2 * math.pi, F["sin"], 600)
    assert aprox == pytest.approx(4.0, rel=2e-2)

def test_trapecio_exacto_para_rectas():
    assert trap.compuesto_n(0, 4, F["2x"], 7) == pytest.approx(16.0)

def test_simpson_13_exacto_hasta_grado_3():
    assert simp.compuesto13_n(0, 2, F["x^3"], 4) == pytest.approx(4.0)
    assert simp.compuesto13_n(0, 3, F["x^2"], 4) == pytest.approx(9.0)

def test_simpson_38_exacto_hasta_grado_3():
    assert simp.compuesto38_n(0, 2, F["x^3"], 6) == pytest.approx(4.0)

def test_punto_medio_exacto_para_rectas():
    assert pm.mid_n(0, 4, F["2x"], 5) == pytest.approx(16.0)

def test_funcion_constante_todos_exactos():
    for nombre, metodo in METODOS.items():
        if nombre in ("rectangulo", "riemann"):
            continue  # ver test de la suma de Riemann más abajo
        assert metodo(0, 5, F["c"], 12) == pytest.approx(5.0), nombre

def test_trapecio_simple():
    assert trap.simple(0, 2, F["x"]) == pytest.approx(2.0)

def test_simpson_13_simple_parabola():
    assert simp.simple_13(0, 3, F["x^2"]) == pytest.approx(9.0)

def test_simpson_38_simple_cubica():
    assert simp.simple38(0, 2, F["x^3"]) == pytest.approx(4.0)

@pytest.mark.parametrize("fn", [trap.simple, simp.simple_13, simp.simple38])
def test_reglas_simples_funcion_negativa_usan_abs(fn):
    # Para f(x) = -x^2 en [0,3] el ÁREA es 9, no -9.
    assert fn(0, 3, lambda x: -2 * x) == pytest.approx(9.0)

def test_simpson_13_ajusta_n_impar():
    assert simp.compuesto13_n(0, 2, F["x^2"], 5) == pytest.approx(
        simp.compuesto13_n(0, 2, F["x^2"], 6)
    )

def test_simpson_38_ajusta_n_no_multiplo_de_3():
    assert simp.compuesto38_n(0, 2, F["x^2"], 7) == pytest.approx(
        simp.compuesto38_n(0, 2, F["x^2"], 9)
    )

@pytest.mark.parametrize(
    "atajo,n",
    [
        (rect.n10, 10), (rect.n100, 100), (rect.n1000, 1000), (rect.n10000, 10000),
        (riemann.n_10, 10), (riemann.n_100, 100), (riemann.n_1000, 1000),
        (pm.mid_n100, 100), (pm.mid_n1000, 1000), (pm.mid_n10000, 10000),
        (trap.compuesto_n10, 10), (trap.compuesto_n100, 100), (trap.compuesto_n1000, 1000),
    ],
)
def test_atajos_equivalen_a_su_n(atajo, n):
    base = {
        "rect": rect.n, "riemann": riemann.n, "pm": pm.mid_n, "trap": trap.compuesto_n,
    }
    nombre = atajo.__module__.rsplit(".", 1)[-1]
    metodo = {
        "metodo_rectangulo": base["rect"], "sumas_riemann": base["riemann"],
        "punto_medio": base["pm"], "metodo_trapecio": base["trap"],
    }[nombre]
    assert atajo(0, 1, F["x^2"]) == pytest.approx(metodo(0, 1, F["x^2"], n))

@pytest.mark.parametrize(
    "atajo,n,base",
    [
        (simp.compuesto13_n10, 10, simp.compuesto13_n),
        (simp.compuesto13_n100, 100, simp.compuesto13_n),
        (simp.compuesto38_n12, 12, simp.compuesto38_n),
        (simp.compuesto38_n120, 120, simp.compuesto38_n),
    ],
)
def test_atajos_simpson(atajo, n, base):
    assert atajo(0, 1, F["x^2"]) == pytest.approx(base(0, 1, F["x^2"], n))

def _error(metodo, n, nombre="e^x", a=0, b=1, exacto=math.e - 1):
    return abs(metodo(a, b, F[nombre], n) - exacto)

@pytest.mark.parametrize(
    "metodo,orden_min",
    [(trap.compuesto_n, 1.9), (pm.mid_n, 1.9), (simp.compuesto13_n, 3.8), (simp.compuesto38_n, 3.8)],
)
def test_orden_de_convergencia(metodo, orden_min):
    e1, e2 = _error(metodo, 12), _error(metodo, 24)
    assert math.log2(e1 / e2) >= orden_min

def test_simpson_mejor_que_trapecio():
    assert _error(simp.compuesto13_n, 12) < _error(trap.compuesto_n, 12)

@pytest.mark.parametrize("metodo", [rect.n, riemann.n])
def test_rectangulo_constante_es_exacto(metodo):
    assert metodo(0, 5, F["c"], 10) == pytest.approx(5.0)

@pytest.mark.parametrize("metodo", [rect.n, riemann.n])
def test_rectangulo_coincide_con_suma_izquierda(metodo):
    a, b, n = 0, 3, 12
    h = (b - a) / n
    izquierda = h * sum(abs(F["x^2+1"](a + i * h)) for i in range(n))
    assert metodo(a, b, F["x^2+1"], n) == pytest.approx(izquierda)

def test_rectangulo_converge_con_orden_1():
    e1, e2 = _error(rect.n, 100), _error(rect.n, 200)
    assert math.log2(e1 / e2) == pytest.approx(1, abs=0.15)