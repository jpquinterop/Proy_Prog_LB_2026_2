import math

import pytest

import functions as fun
import metodo_trapecio as trap
import regla_simpson as simp
from calculo_integral.exceptions.exception import (
    ErrorRelativoIndefinidoError,
    LimitesInvalidosError,
    MetodoDesconocidoError,
    NoConvergenciaError,
    ParametroInvalidoError,
    TipoInvalidoError,
)
from calculo_integral.integral_definida.metodos_numericos import calculo_errores as ce

F = fun.functions
EXACTO_EXP = math.e - 1

def test_error_absoluto():
    assert ce.error_absoluto(10, 9.5) == pytest.approx(0.5)
    assert ce.error_absoluto(9.5, 10) == pytest.approx(0.5)

def test_error_relativo_y_porcentual():
    assert ce.error_relativo(10, 9) == pytest.approx(0.1)
    assert ce.error_porcentual(10, 9) == pytest.approx(10.0)

def test_error_relativo_con_exacto_cero():
    with pytest.raises(ErrorRelativoIndefinidoError):
        ce.error_relativo(0, 1)

@pytest.mark.parametrize("malo", ["1", None, True, float("nan"), float("inf")])
def test_error_absoluto_rechaza_valores_invalidos(malo):
    with pytest.raises((TipoInvalidoError, ParametroInvalidoError)):
        ce.error_absoluto(malo, 1)

def test_error_por_refinamiento_es_pequeno_si_converge():
    assert ce.error_por_refinamiento(simp.compuesto13_n, 0, 1, F["e^x"], 50) < 1e-7

def test_refinar_hasta_tolerancia():
    aprox, n, err = ce.refinar_hasta_tolerancia(trap.compuesto_n, 0, 1, F["e^x"], tol=1e-6)
    assert err < 1e-6
    assert aprox == pytest.approx(EXACTO_EXP, abs=1e-5)
    assert n >= 20

def test_refinar_hasta_tolerancia_no_converge():
    with pytest.raises(NoConvergenciaError):
        ce.refinar_hasta_tolerancia(trap.compuesto_n, 0, 1, F["e^x"], tol=1e-15, n_inicial=2, n_max=8)

@pytest.mark.parametrize("tol", [0, -1e-3])
def test_refinar_tolerancia_invalida(tol):
    with pytest.raises(ParametroInvalidoError):
        ce.refinar_hasta_tolerancia(trap.compuesto_n, 0, 1, F["x"], tol=tol)

def test_orden_convergencia_trapecio_es_2():
    p = ce.orden_convergencia(trap.compuesto_n, 0, 1, F["e^x"], 20, EXACTO_EXP)
    assert p == pytest.approx(2, abs=0.1)

def test_orden_convergencia_simpson_es_4():
    p = ce.orden_convergencia(simp.compuesto13_n, 0, 1, F["e^x"], 10, EXACTO_EXP)
    assert p == pytest.approx(4, abs=0.2)

def test_orden_convergencia_infinito_si_es_exacto():
    assert ce.orden_convergencia(trap.compuesto_n, 0, 1, F["x"], 4, 0.5) == math.inf

def test_cota_error_trapecio():
    assert ce.cota_error("trapecio", 0, 2, 10, 4) == pytest.approx(8 / 12 * 4 / 100)

def test_cota_error_realmente_acota():
    M = ce.estimar_max_derivada(F["e^x"], 0, 1, 2)
    cota = ce.cota_error("trapecio", 0, 1, 20, M)
    real = abs(trap.compuesto_n(0, 1, F["e^x"], 20) - EXACTO_EXP)
    assert real <= cota

def test_cota_error_metodo_desconocido():
    with pytest.raises(MetodoDesconocidoError):
        ce.cota_error("gauss", 0, 1, 10, 1)

def test_cota_error_M_negativo():
    with pytest.raises(ParametroInvalidoError):
        ce.cota_error("trapecio", 0, 1, 10, -1)

@pytest.mark.parametrize("metodo", ["rectangulo", "punto_medio", "trapecio", "simpson_13", "simpson_38"])
def test_n_requerido_cumple_la_tolerancia(metodo):
    tol = 1e-4
    n = ce.n_requerido(metodo, 0, 1, M=5, tol=tol)
    assert ce.cota_error(metodo, 0, 1, n, 5) <= tol

def test_n_requerido_simpson_es_par_y_38_multiplo_de_3():
    assert ce.n_requerido("simpson_13", 0, 1, 5, 1e-3) % 2 == 0
    assert ce.n_requerido("simpson_38", 0, 1, 5, 1e-3) % 3 == 0

def test_n_requerido_M_cero():
    assert ce.n_requerido("trapecio", 0, 1, 0, 1e-6) == 1

def test_estimar_max_derivada_segunda_de_x2():
    assert ce.estimar_max_derivada(F["x^2"], 0, 1, 2) == pytest.approx(2.0, rel=1e-6)

def test_estimar_max_derivada_primera_de_seno():
    assert ce.estimar_max_derivada(F["sin"], 0, math.pi, 1) == pytest.approx(1.0, rel=1e-3)

def test_estimar_max_derivada_orden_invalido():
    with pytest.raises(ParametroInvalidoError):
        ce.estimar_max_derivada(F["x"], 0, 1, 3)

def test_estimar_max_derivada_intervalo_diminuto():
    with pytest.raises(LimitesInvalidosError):
        ce.estimar_max_derivada(F["x"], 0, 0.001, 4)

def test_resumen_error_con_y_sin_exacto():
    r = ce.resumen_error(trap.compuesto_n, 0, 1, F["e^x"], 10, exacto=EXACTO_EXP)
    assert {"n", "aproximacion", "exacto", "error_absoluto", "error_relativo",
            "error_porcentual", "error_estimado_refinamiento"} <= set(r)
    r2 = ce.resumen_error(trap.compuesto_n, 0, 1, F["e^x"], 10)
    assert "error_absoluto" not in r2

def test_resumen_error_exacto_cero_omite_relativo():
    r = ce.resumen_error(trap.compuesto_n, 0, 1, F["c"], 4, exacto=0)
    assert "error_relativo" not in r and "error_absoluto" in r

def test_tabla_convergencia():
    filas = ce.tabla_convergencia(trap.compuesto_n, 0, 1, F["e^x"], [4, 8, 16], exacto=EXACTO_EXP)
    assert [f["n"] for f in filas] == [4, 8, 16]
    assert "dif_con_anterior" not in filas[0] and "dif_con_anterior" in filas[1]
    errores = [f["error_absoluto"] for f in filas]
    assert errores == sorted(errores, reverse=True)

def test_comparar_metodos_ordena_por_error():
    metodos = {"trapecio": trap.compuesto_n, "simpson_13": simp.compuesto13_n}
    filas = ce.comparar_metodos(metodos, 0, 1, F["e^x"], 12, exacto=EXACTO_EXP)
    assert filas[0]["metodo"] == "simpson_13"

def test_comparar_metodos_captura_errores_de_un_metodo():
    def roto(a, b, f, n):
        raise ValueError("boom")

    filas = ce.comparar_metodos({"roto": roto, "trapecio": trap.compuesto_n}, 0, 1, F["x"], 4)
    assert any("error" in f and "boom" in f["error"] for f in filas)
    assert any("aproximacion" in f for f in filas)

def test_imprimir_tabla(capsys):
    ce.imprimir_tabla([{"n": 4, "aproximacion": 1.5}, {"n": 8, "aproximacion": 1.25}])
    salida = capsys.readouterr().out
    assert "aproximacion" in salida and "1.50000000" in salida

def test_imprimir_tabla_vacia(capsys):
    ce.imprimir_tabla([])
    assert "sin datos" in capsys.readouterr().out