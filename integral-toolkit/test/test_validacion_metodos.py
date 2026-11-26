import math

import pytest

from calculo_integral import functions as fun
from calculo_integral.integral_definida.metodos_numericos import metodo_rectangulo as rect
from calculo_integral.integral_definida.metodos_numericos import metodo_trapecio as trap
from calculo_integral.integral_definida.metodos_numericos import punto_medio as pm
from calculo_integral.integral_definida.metodos_numericos import regla_simpson as simp
from calculo_integral.integral_definida import sumas_riemann as riemann
from calculo_integral.exceptions.exception import (
    ErrorIntegral,
    EvaluacionError,
    FueraDeDominioError,
    LimitesInvalidosError,
    SingularidadError,
    SubintervalosInvalidosError,
    TipoInvalidoError,
)

F = fun.functions

CON_N = {
    "riemann": riemann.n,
    "rectangulo": rect.n,
    "trapecio": trap.compuesto_n,
    "punto_medio": pm.mid_n,
    "simpson_13": simp.compuesto13_n,
    "simpson_38": simp.compuesto38_n,
}

SIN_N = {
    "trapecio_simple": trap.simple,
    "simpson_13_simple": simp.simple_13,
    "simpson_38_simple": simp.simple38,
}

ATAJOS = {
    "rect.n10": rect.n10, "rect.n10000": rect.n10000,
    "riemann.n_10": riemann.n_10, "riemann.n_10000": riemann.n_10000,
    "trap.n10": trap.compuesto_n10, "trap.n10000": trap.compuesto_n10000,
    "pm.n100": pm.mid_n100, "pm.n10000": pm.mid_n10000,
    "s13.n10": simp.compuesto13_n10, "s13.n10000": simp.compuesto13_n10000,
    "s38.n12": simp.compuesto38_n12, "s38.n12000": simp.compuesto38_n12000,
}
SIN_N_Y_ATAJOS = {**SIN_N, **ATAJOS}

def llamar(metodo, a, b, f, n=10):
    """Llama al método con n si lo acepta."""
    return metodo(a, b, f, n) if metodo in CON_N.values() else metodo(a, b, f)

TODOS = {**CON_N, **SIN_N_Y_ATAJOS}

@pytest.mark.parametrize("nombre", TODOS)
@pytest.mark.parametrize("a,b", [(1, 0), (2, 2)])
def test_limites_invalidos(nombre, a, b):
    with pytest.raises(LimitesInvalidosError):
        llamar(TODOS[nombre], a, b, F["x"])

@pytest.mark.parametrize("nombre", TODOS)
@pytest.mark.parametrize("a,b", [(0, math.inf), (-math.inf, 1), (math.nan, 1)])
def test_limites_no_finitos(nombre, a, b):
    with pytest.raises(LimitesInvalidosError):
        llamar(TODOS[nombre], a, b, F["x"])

@pytest.mark.parametrize("nombre", TODOS)
@pytest.mark.parametrize("a,b", [("0", 1), (0, None)])
def test_limites_de_tipo_incorrecto(nombre, a, b):
    with pytest.raises(TipoInvalidoError):
        llamar(TODOS[nombre], a, b, F["x"])

@pytest.mark.parametrize("nombre", CON_N)
@pytest.mark.parametrize("n", [0, -4])
def test_n_no_positivo(nombre, n):
    with pytest.raises(SubintervalosInvalidosError):
        CON_N[nombre](0, 1, F["x"], n)

@pytest.mark.parametrize("nombre", CON_N)
@pytest.mark.parametrize("n", [2.5, "10", None, True])
def test_n_de_tipo_incorrecto(nombre, n):
    with pytest.raises(TipoInvalidoError):
        CON_N[nombre](0, 1, F["x"], n)

@pytest.mark.parametrize("nombre", CON_N)
def test_n_por_keyword(nombre):
    assert CON_N[nombre](0, 1, F["x"], n=10) >= 0
    with pytest.raises(SubintervalosInvalidosError):
        CON_N[nombre](0, 1, F["x"], n=0)

@pytest.mark.parametrize("nombre", TODOS)
def test_singularidad_en_el_intervalo(nombre):
    with pytest.raises(SingularidadError):
        llamar(TODOS[nombre], -1, 1, F["1/x"])

@pytest.mark.parametrize("nombre", TODOS)
def test_intervalo_fuera_del_dominio(nombre):
    with pytest.raises(FueraDeDominioError):
        llamar(TODOS[nombre], -1, 1, F["sqrt(x)"])

@pytest.mark.parametrize("nombre", TODOS)
def test_logaritmo_en_cero(nombre):
    with pytest.raises(FueraDeDominioError):
        llamar(TODOS[nombre], 0, 1, F["ln"])

@pytest.mark.parametrize("nombre", TODOS)
def test_dominio_valido_no_lanza(nombre):
    assert llamar(TODOS[nombre], 1, 2, F["1/x"]) > 0

@pytest.mark.parametrize("nombre", TODOS)
def test_funcion_propia_que_falla_en_un_punto(nombre):
    with pytest.raises(EvaluacionError):
        llamar(TODOS[nombre], 0, 1, lambda x: 1 / 0)


@pytest.mark.parametrize("nombre", TODOS)
def test_evaluacion_error_conserva_causa(nombre):
    with pytest.raises(EvaluacionError) as info:
        llamar(TODOS[nombre], 0, 1, lambda x: 1 / 0)
    assert isinstance(info.value.causa, ZeroDivisionError)
    assert isinstance(info.value, ArithmeticError)

@pytest.mark.parametrize("nombre", TODOS)
def test_funcion_propia_devuelve_infinito(nombre):
    with pytest.raises(EvaluacionError):
        llamar(TODOS[nombre], 0, 1, lambda x: math.inf)


@pytest.mark.parametrize("nombre", TODOS)
def test_funcion_propia_devuelve_complejo(nombre):
    with pytest.raises(EvaluacionError):
        llamar(TODOS[nombre], 0, 1, lambda x: complex(1, 1))

@pytest.mark.parametrize("nombre", TODOS)
def test_todos_los_errores_son_de_la_libreria(nombre):
    """Se puede atrapar cualquier fallo con `except ErrorIntegral`."""
    casos = [(1, 0, F["x"]), (-1, 1, F["1/x"]), (0, 1, lambda x: 1 / 0)]
    for a, b, f in casos:
        with pytest.raises(ErrorIntegral):
            llamar(TODOS[nombre], a, b, f)

@pytest.mark.parametrize("nombre", TODOS)
def test_funcion_valida_sigue_funcionando(nombre):
    assert llamar(TODOS[nombre], 0, 1, F["x"]) == pytest.approx(0.5, rel=0.1)

def test_el_decorador_conserva_nombre_y_docstring():
    assert trap.compuesto_n.__name__ == "compuesto_n"
    assert simp.compuesto13_n.__name__ == "compuesto13_n"