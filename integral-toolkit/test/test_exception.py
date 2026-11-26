import math

import pytest

import functions as fun
import metodo_trapecio as trap
from calculo_integral.exceptions import exception as ex

F = fun.functions

def test_jerarquia_de_excepciones():
    assert issubclass(ex.TipoInvalidoError, (ex.ErrorIntegral, TypeError))
    assert issubclass(ex.LimitesInvalidosError, ValueError)
    assert issubclass(ex.SingularidadError, ex.FueraDeDominioError)
    assert issubclass(ex.EvaluacionError, ArithmeticError)
    assert issubclass(ex.ErrorRelativoIndefinidoError, ZeroDivisionError)
    assert issubclass(ex.NoConvergenciaError, RuntimeError)

@pytest.mark.parametrize("v", [0, 1, -2.5, 1e300])
def test_validar_numero_acepta(v):
    ex.validar_numero(v, "x")

@pytest.mark.parametrize("v", ["1", None, [1], True, 1 + 2j])
def test_validar_numero_tipo_invalido(v):
    with pytest.raises(ex.TipoInvalidoError):
        ex.validar_numero(v, "x")

@pytest.mark.parametrize("v", [math.nan, math.inf, -math.inf])
def test_validar_numero_no_finito(v):
    with pytest.raises(ex.ParametroInvalidoError):
        ex.validar_numero(v, "x")

def test_validar_positivo_y_no_negativo():
    ex.validar_positivo(0.1, "t")
    ex.validar_no_negativo(0, "t")
    with pytest.raises(ex.ParametroInvalidoError):
        ex.validar_positivo(0, "t")
    with pytest.raises(ex.ParametroInvalidoError):
        ex.validar_no_negativo(-1e-9, "t")

def test_validar_limites_ok():
    ex.validar_limites(-1, 1)
    ex.validar_limites(0.5, 0.6)

@pytest.mark.parametrize("a,b", [(1, 0), (3, 3)])
def test_validar_limites_orden(a, b):
    with pytest.raises(ex.LimitesInvalidosError):
        ex.validar_limites(a, b)

@pytest.mark.parametrize("a,b", [(0, math.inf), (-math.inf, 0), (math.nan, 1)])
def test_validar_limites_no_finitos(a, b):
    with pytest.raises(ex.LimitesInvalidosError):
        ex.validar_limites(a, b)

@pytest.mark.parametrize("a,b", [("0", 1), (0, None)])
def test_validar_limites_tipo(a, b):
    with pytest.raises(ex.TipoInvalidoError):
        ex.validar_limites(a, b)

def test_validar_subintervalos_ok():
    ex.validar_subintervalos(10)
    ex.validar_subintervalos(12, multiplo=3)

@pytest.mark.parametrize("n", [0, -5])
def test_validar_subintervalos_no_positivo(n):
    with pytest.raises(ex.SubintervalosInvalidosError):
        ex.validar_subintervalos(n)

@pytest.mark.parametrize("n", [2.0, "10", True, None])
def test_validar_subintervalos_tipo(n):
    with pytest.raises(ex.TipoInvalidoError):
        ex.validar_subintervalos(n)

def test_validar_subintervalos_multiplo_y_maximo():
    with pytest.raises(ex.SubintervalosInvalidosError):
        ex.validar_subintervalos(10, multiplo=3)
    with pytest.raises(ex.SubintervalosInvalidosError):
        ex.validar_subintervalos(11, n_max=10)

@pytest.mark.parametrize("nombre,a,b", [("1/x", -1, 1), ("1/x", 0, 1), ("1/x^2", -2, 0)])
def test_dominio_singularidad(nombre, a, b):
    with pytest.raises(ex.SingularidadError):
        ex.validar_dominio(nombre, a, b)

@pytest.mark.parametrize(
    "nombre,a,b",
    [("sqrt(x)", -1, 1), ("asin", -2, 0), ("semicirculo", -2, 2), ("ln", 0, 1), ("ln", -1, 1), ("e^x", 0, 1000), ("e^(x^2)", 0, 30)],
)
def test_dominio_fuera(nombre, a, b):
    with pytest.raises(ex.FueraDeDominioError):
        ex.validar_dominio(nombre, a, b)

@pytest.mark.parametrize(
    "nombre,a,b",
    [("1/x", 1, 2), ("sqrt(x)", 0, 4), ("ln", 0.1, 5), ("semicirculo", -1, 1), ("e^x", -10, 10), ("sin", -1000, 1000), ("desconocida", -5, 5)],
)
def test_dominio_valido(nombre, a, b):
    ex.validar_dominio(nombre, a, b)

def test_dominio_descripcion():
    assert "excepto" in ex.DOMINIOS["1/x"].descripcion()
    assert ex.DOMINIOS["sqrt(x)"].descripcion().startswith("[0")

def test_todos_los_dominios_corresponden_a_funciones_registradas():
    assert set(ex.DOMINIOS) <= set(F), set(ex.DOMINIOS) - set(F)

def test_nombre_de_funcion_reconoce_el_registro():
    assert ex.nombre_de_funcion(F["1/x"]) == "1/x"
    assert ex.nombre_de_funcion(lambda x: x) is None

def test_funcion_segura_propaga_valor_normal():
    assert ex.funcion_segura(F["x^2"])(3) == 9

def test_funcion_segura_convierte_errores():
    g = ex.funcion_segura(F["1/x"], "1/x")
    with pytest.raises(ex.EvaluacionError) as info:
        g(0)
    assert info.value.x == 0 and info.value.nombre == "1/x"

def test_funcion_segura_resultados_no_validos():
    with pytest.raises(ex.EvaluacionError):
        ex.funcion_segura(lambda x: float("inf"))(1)
    with pytest.raises(ex.EvaluacionError):
        ex.funcion_segura(lambda x: complex(0, 1))(1)
    with pytest.raises(ex.EvaluacionError):
        ex.funcion_segura(lambda x: math.sqrt(x))(-1)

def test_funcion_segura_es_idempotente():
    g = ex.funcion_segura(F["x"])
    assert ex.funcion_segura(g) is g

@ex.controlar_integracion
def _trapecio_controlado(a, b, f, n):
    return trap.compuesto_n(a, b, f, n)

def test_decorador_funciona_en_caso_valido():
    assert _trapecio_controlado(0, 1, F["x"], 10) == pytest.approx(0.5)

def test_decorador_valida_limites_n_y_dominio():
    with pytest.raises(ex.LimitesInvalidosError):
        _trapecio_controlado(1, 0, F["x"], 10)
    with pytest.raises(ex.SubintervalosInvalidosError):
        _trapecio_controlado(0, 1, F["x"], 0)
    with pytest.raises(ex.SingularidadError):
        _trapecio_controlado(-1, 1, F["1/x"], 10)


def test_decorador_acepta_n_por_keyword():
    assert _trapecio_controlado(0, 1, F["x"], n=10) == pytest.approx(0.5)
    with pytest.raises(ex.SubintervalosInvalidosError):
        _trapecio_controlado(0, 1, F["x"], n=-1)

def test_decorador_traduce_fallos_de_evaluacion():
    with pytest.raises(ex.EvaluacionError):
        _trapecio_controlado(0, 1, lambda x: 1 / (x - 0.5), 10)
