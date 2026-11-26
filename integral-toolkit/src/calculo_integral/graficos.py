import warnings

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

from calculo_integral.exceptions.exception import (
    MetodoDesconocidoError,
    SubintervalosInvalidosError,
    funcion_segura,
    nombre_de_funcion,
    validar_dominio,
    validar_limites,
    validar_subintervalos,
)
from calculo_integral.integral_definida.metodos_numericos.calculo_errores import (
    error_absoluto,
    error_por_refinamiento,
)

METODOS_DIBUJABLES = ("rectangulo", "punto_medio", "trapecio", "simpson_13", "simpson_38")
N_MAX_DIBUJO = 200

_COLOR_NEGATIVO = "#D62728"
_COLORES = {
    "rectangulo": "#4C78A8",
    "punto_medio": "#54A24B",
    "trapecio": "#F58518",
    "simpson_13": "#B279A2",
    "simpson_38": "#72B7B2",
}
_ETIQUETAS = {
    "rectangulo": "Rectángulo (izquierda)",
    "punto_medio": "Punto medio",
    "trapecio": "Trapecio",
    "simpson_13": "Simpson 1/3",
    "simpson_38": "Simpson 3/8",
}


def _preparar(f, a, b):
    validar_limites(a, b)
    nombre = nombre_de_funcion(f)
    if nombre is not None:
        validar_dominio(nombre, a, b)
    return funcion_segura(f, nombre)


def _ajustar_n(metodo, n):
    if metodo == "simpson_13" and n % 2:
        n += 1
    if metodo == "simpson_38" and n % 3:
        n += 3 - n % 3
    return n


def _figura(ax):
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))
    else:
        fig = ax.figure
    return fig, ax


def _cerrar(fig, guardar, mostrar):
    fig.tight_layout()
    if guardar:
        fig.savefig(guardar, dpi=150)
    if mostrar:
        plt.show()


def _curva(ax, g, a, b):
    xx = np.linspace(a, b, 400)
    yy = np.array([g(x) for x in xx])
    ax.plot(xx, yy, color="black", lw=1.6, label="f(x)")
    ax.axhline(0, color="black", lw=0.6)
    return yy


def _leyenda(ax, color, area, hay_negativo):
    handles, _ = ax.get_legend_handles_labels()
    if area and hay_negativo:
        handles.append(Patch(facecolor=color, alpha=0.45, edgecolor="black", label="Suma al área (f ≥ 0)"))
        handles.append(Patch(facecolor=_COLOR_NEGATIVO, alpha=0.45, edgecolor="black", label="Suma al área (f < 0, se toma |f|)"))
    else:
        handles.append(Patch(facecolor=color, alpha=0.45, edgecolor="black", label="Región"))
    ax.legend(handles=handles, loc="best")


def _relleno(ax, xx, yy, color, area):
    xx = np.asarray(xx, dtype=float)
    yy = np.asarray(yy, dtype=float)
    estilo = dict(interpolate=True, alpha=0.45, edgecolor="black", linewidth=0.7)
    ax.fill_between(xx, yy, where=yy >= 0, color=color, **estilo)
    ax.fill_between(xx, yy, where=yy < 0,
                    color=_COLOR_NEGATIVO if area else color, **estilo)


def _barras(ax, xs, alturas, h, color, area):
    colores = [_COLOR_NEGATIVO if (area and y < 0) else color for y in alturas]
    ax.bar(xs, alturas, width=h, align="edge", alpha=0.45, color=colores, edgecolor="black", linewidth=0.7)


def _polinomio(ax, x0, h, ys, grado, color, area):
    xs_rel = np.arange(grado + 1) * h
    coef = np.polyfit(xs_rel, ys, grado)
    xx = np.linspace(0, grado * h, 40)
    _relleno(ax, x0 + xx, np.polyval(coef, xx), color, area)


def graficar_funcion(f, a, b, area=True, ax=None, guardar=None, mostrar=True):
    g = _preparar(f, a, b)
    fig, ax = _figura(ax)
    xx = np.linspace(a, b, 400)
    yy = np.array([g(x) for x in xx])
    _relleno(ax, xx, yy, "#4C78A8", area)
    _curva(ax, g, a, b)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(f"Área bajo la curva en [{a}, {b}]" if area else f"f(x) en [{a}, {b}]")
    ax.grid(alpha=0.3)
    _leyenda(ax, "#4C78A8", area, bool((yy < 0).any()))
    _cerrar(fig, guardar, mostrar)
    return fig, ax


def graficar_area(f, a, b, n=10, metodo="trapecio", area=True, exacto=None, metodo_fn=None, ax=None, guardar=None, mostrar=True):
    if metodo not in METODOS_DIBUJABLES:
        raise MetodoDesconocidoError(
            f"Método '{metodo}' desconocido. Opciones: {', '.join(METODOS_DIBUJABLES)}."
        )
    validar_subintervalos(n)
    if n > N_MAX_DIBUJO:
        raise SubintervalosInvalidosError(
            f"Para dibujar usa n <= {N_MAX_DIBUJO} (recibido: {n})."
        )

    g = _preparar(f, a, b)
    w = (lambda x: abs(g(x))) if area else g
    n_original = n
    n = _ajustar_n(metodo, n)
    h = (b - a) / n
    color = _COLORES[metodo]
    fig, ax = _figura(ax)

    if metodo == "rectangulo":
        xs = a + h * np.arange(n)
        _barras(ax, xs, [g(x) for x in xs], h, color, area)
        aprox = h * sum(w(x) for x in xs)

    elif metodo == "punto_medio":
        xs = a + h * np.arange(n)
        alturas = [g(x + h / 2) for x in xs]
        _barras(ax, xs, alturas, h, color, area)
        ax.plot(xs + h / 2, alturas, "o", color="black", ms=3)
        aprox = h * sum(w(x + h / 2) for x in xs)

    elif metodo == "trapecio":
        ys = [g(a + i * h) for i in range(n + 1)]
        for i in range(n):
            _relleno(ax, [a + i * h, a + (i + 1) * h], ys[i:i + 2], color, area)
        wy = [w(a + i * h) for i in range(n + 1)]
        aprox = h * (wy[0] / 2 + sum(wy[1:-1]) + wy[-1] / 2)

    elif metodo == "simpson_13":
        ys = [g(a + i * h) for i in range(n + 1)]
        for k in range(0, n, 2):
            _polinomio(ax, a + k * h, h, ys[k:k + 3], 2, color, area)
        wy = [w(a + i * h) for i in range(n + 1)]
        aprox = (h / 3) * (wy[0] + wy[-1]
                           + 4 * sum(wy[1:-1:2]) + 2 * sum(wy[2:-1:2]))

    else:
        ys = [g(a + i * h) for i in range(n + 1)]
        for k in range(0, n, 3):
            _polinomio(ax, a + k * h, h, ys[k:k + 4], 3, color, area)
        wy = [w(a + i * h) for i in range(n + 1)]
        interior = sum(wy[i] * (2 if i % 3 == 0 else 3) for i in range(1, n))
        aprox = (3 * h / 8) * (wy[0] + interior + wy[-1])

    yy = _curva(ax, g, a, b)

    valor = aprox
    if metodo_fn is not None:
        valor = metodo_fn(a, b, f, n_original)
        if abs(valor - aprox) > 1e-9 * max(1.0, abs(aprox)):
            warnings.warn(
                f"El método de la librería ({valor:.10g}) no coincide con la "
                f"geometría dibujada ({aprox:.10g}) para n={n_original}.",
                stacklevel=2,
            )

    titulo = f"{_ETIQUETAS[metodo]}, n = {n}"
    if n != n_original:
        titulo += f" (ajustado desde {n_original})"
    titulo += f"\nÁrea ≈ {valor:.6f}" if area else f"\nIntegral ≈ {valor:.6f}"
    if exacto is not None:
        titulo += f"   |   error absoluto = {error_absoluto(exacto, valor):.3e}"
    ax.set_title(titulo)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.grid(alpha=0.3)
    _leyenda(ax, color, area, bool((yy < 0).any()))
    _cerrar(fig, guardar, mostrar)
    return fig, ax, valor


def graficar_convergencia(metodos, a, b, f, ns=(6, 12, 24, 48, 96, 192, 384, 768, 1536), exacto=None, ax=None, guardar=None, mostrar=True):
    validar_limites(a, b)
    for n in ns:
        validar_subintervalos(n)

    fig, ax = _figura(ax)
    ns = list(ns)
    inicio = None

    for nombre, metodo in metodos.items():
        if exacto is not None:
            errores = [error_absoluto(exacto, metodo(a, b, f, n)) for n in ns]
        else:
            errores = [error_por_refinamiento(metodo, a, b, f, n) for n in ns]
        puntos = [(n, e) for n, e in zip(ns, errores) if e > 0]
        if not puntos:
            continue
        if inicio is None:
            inicio = puntos[0]
        ax.loglog([p[0] for p in puntos], [p[1] for p in puntos], "o-", label=_ETIQUETAS.get(nombre, nombre), lw=1.6, ms=4)

    if inicio is not None:
        n0, e0 = inicio
        nn = np.array([ns[0], ns[-1]], dtype=float)
        for p in (1, 2, 4):
            ax.loglog(nn, e0 * (n0 / nn) ** p, ":", color="gray", lw=1)
            ax.annotate(f"$n^{{-{p}}}$", (nn[-1], e0 * (n0 / nn[-1]) ** p),
                        color="gray", fontsize=9, va="bottom", ha="right")

    ax.set_xlabel("n (subintervalos)")
    ax.set_ylabel("Error absoluto" if exacto is not None else "Error estimado |I(2n) − I(n)|")
    ax.set_title("Convergencia del error")
    ax.grid(alpha=0.3, which="both")
    ax.legend()
    _cerrar(fig, guardar, mostrar)
    return fig, ax