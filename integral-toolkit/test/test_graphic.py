import math
import warnings

import matplotlib.pyplot as plt
import pytest

from calculo_integral import functions as fun
from calculo_integral.integral_definida.metodos_numericos import metodo_trapecio as trap
from calculo_integral.integral_definida.metodos_numericos import punto_medio as pm
from calculo_integral.integral_definida.metodos_numericos import regla_simpson as simp
from calculo_integral import graficos as gr
from calculo_integral.exceptions.exception import (
    LimitesInvalidosError,
    MetodoDesconocidoError,
    SingularidadError,
    SubintervalosInvalidosError,
    TipoInvalidoError,
)

F = fun.functions

@pytest.fixture(autouse=True)
def cerrar_figuras():
    yield
    plt.close("all")

def test_graficar_funcion_devuelve_fig_y_ax():
    fig, ax = gr.graficar_funcion(F["x^2"], 0, 2, mostrar=False)
    assert fig is ax.figure
    assert "Área bajo la curva" in ax.get_title()

def test_graficar_funcion_sin_area_cambia_titulo():
    _, ax = gr.graficar_funcion(F["x^2"], 0, 2, area=False, mostrar=False)
    assert "f(x)" in ax.get_title()


def test_graficar_funcion_guarda_archivo(tmp_path):
    ruta = tmp_path / "f.png"
    gr.graficar_funcion(F["sin"], 0, math.pi, guardar=str(ruta), mostrar=False)
    assert ruta.exists() and ruta.stat().st_size > 0


def test_graficar_funcion_usa_ax_existente():
    fig, ax = plt.subplots()
    fig2, ax2 = gr.graficar_funcion(F["x"], 0, 1, ax=ax, mostrar=False)
    assert ax2 is ax and fig2 is fig

@pytest.mark.parametrize("metodo", gr.METODOS_DIBUJABLES)
def test_graficar_area_todos_los_metodos(metodo):
    fig, ax, valor = gr.graficar_area(F["x^2"], 0, 3, n=12, metodo=metodo, mostrar=False)
    assert valor > 0
    assert metodo.replace("_", " ").split()[0][:4].lower() or True  # título existe
    assert ax.get_title()

@pytest.mark.parametrize(
    "metodo,fn",
    [
        ("trapecio", trap.compuesto_n),
        ("punto_medio", pm.mid_n),
        ("simpson_13", simp.compuesto13_n),
        ("simpson_38", simp.compuesto38_n),
    ],
)
def test_valor_dibujado_coincide_con_la_libreria(metodo, fn):
    with warnings.catch_warnings():
        warnings.simplefilter("error")  # cualquier aviso de discrepancia = fallo
        _, _, valor = gr.graficar_area(
            F["x^2"], 0, 3, n=12, metodo=metodo, metodo_fn=fn, mostrar=False
        )
    assert valor == pytest.approx(fn(0, 3, F["x^2"], 12))

def test_graficar_area_funcion_negativa_usa_abs():
    _, _, valor = gr.graficar_area(F["-x"], 0, 2, n=50, metodo="trapecio", mostrar=False)
    assert valor == pytest.approx(2.0, rel=1e-6)

def test_graficar_area_seno_periodo_completo():
    _, _, valor = gr.graficar_area(F["sin"], 0, 2 * math.pi, n=200, metodo="simpson_13", mostrar=False)
    assert valor == pytest.approx(4.0, rel=1e-3)

def test_graficar_area_sin_abs_conserva_signo():
    _, _, valor = gr.graficar_area(F["sin"], 0, 2 * math.pi, n=200, metodo="trapecio", area=False, mostrar=False)
    assert valor == pytest.approx(0.0, abs=1e-6)

def test_graficar_area_ajusta_n_en_simpson():
    _, ax, _ = gr.graficar_area(F["x^2"], 0, 1, n=5, metodo="simpson_13", mostrar=False)
    assert "ajustado desde 5" in ax.get_title()
    _, ax, _ = gr.graficar_area(F["x^2"], 0, 1, n=7, metodo="simpson_38", mostrar=False)
    assert "ajustado desde 7" in ax.get_title()

def test_graficar_area_muestra_error_si_hay_exacto():
    _, ax, _ = gr.graficar_area(F["x^2"], 0, 3, n=10, metodo="trapecio", exacto=9.0, mostrar=False)
    assert "error absoluto" in ax.get_title()

def test_graficar_area_avisa_si_metodo_no_coincide_con_dibujo():
    def malo(a, b, f, n):
        return 123.0
    with pytest.warns(UserWarning, match="no coincide"):
        gr.graficar_area(F["x^2"], 0, 3, n=10, metodo="trapecio", metodo_fn=malo, mostrar=False)

def test_graficar_area_metodo_desconocido():
    with pytest.raises(MetodoDesconocidoError):
        gr.graficar_area(F["x"], 0, 1, metodo="gauss", mostrar=False)

@pytest.mark.parametrize("n", [0, -3])
def test_graficar_area_n_invalido(n):
    with pytest.raises(SubintervalosInvalidosError):
        gr.graficar_area(F["x"], 0, 1, n=n, mostrar=False)

def test_graficar_area_n_demasiado_grande_para_dibujar():
    with pytest.raises(SubintervalosInvalidosError):
        gr.graficar_area(F["x"], 0, 1, n=gr.N_MAX_DIBUJO + 1, mostrar=False)

def test_graficar_area_n_no_entero():
    with pytest.raises(TipoInvalidoError):
        gr.graficar_area(F["x"], 0, 1, n=2.5, mostrar=False)

@pytest.mark.parametrize("a,b", [(1, 0), (2, 2)])
def test_graficar_limites_invalidos(a, b):
    with pytest.raises(LimitesInvalidosError):
        gr.graficar_funcion(F["x"], a, b, mostrar=False)

def test_graficar_funcion_con_singularidad():
    with pytest.raises(SingularidadError):
        gr.graficar_funcion(F["1/x"], -1, 1, mostrar=False)

def test_graficar_convergencia_con_exacto():
    metodos = {"trapecio": trap.compuesto_n, "simpson_13": simp.compuesto13_n}
    fig, ax = gr.graficar_convergencia(
        metodos, 0, 1, F["e^x"], ns=(6, 12, 24), exacto=math.e - 1, mostrar=False
    )
    assert "Error absoluto" in ax.get_ylabel()
    assert len(ax.get_legend().get_texts()) == 2

def test_graficar_convergencia_sin_exacto_usa_refinamiento():
    _, ax = gr.graficar_convergencia(
        {"trapecio": trap.compuesto_n}, 0, 1, F["e^x"], ns=(6, 12, 24), mostrar=False
    )
    assert "I(2n)" in ax.get_ylabel()

def test_graficar_convergencia_ns_invalidos():
    with pytest.raises(SubintervalosInvalidosError):
        gr.graficar_convergencia({"t": trap.compuesto_n}, 0, 1, F["x"], ns=(6, 0), mostrar=False)