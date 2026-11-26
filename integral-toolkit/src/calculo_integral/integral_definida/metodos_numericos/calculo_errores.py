import math

from excepciones import (
    ErrorIntegral,
    ErrorRelativoIndefinidoError,
    MetodoDesconocidoError,
    NoConvergenciaError,
    ParametroInvalidoError,
    LimitesInvalidosError,
    funcion_segura,
    validar_limites,
    validar_no_negativo,
    validar_numero,
    validar_positivo,
    validar_subintervalos,
)

def error_absoluto(exacto, aproximado):
    """|exacto - aproximado|"""
    validar_numero(exacto, "exacto")
    validar_numero(aproximado, "aproximado")
    return abs(exacto - aproximado)

def error_relativo(exacto, aproximado):
    """|exacto - aproximado| / |exacto|. No está definido si exacto == 0."""
    validar_numero(exacto, "exacto")
    validar_numero(aproximado, "aproximado")
    if exacto == 0:
        raise ErrorRelativoIndefinidoError(
            "El valor exacto es 0: el error relativo no está definido. "
            "Usa el error absoluto."
        )
    return abs(exacto - aproximado) / abs(exacto)

def error_porcentual(exacto, aproximado):
    """Error relativo expresado en %."""
    return error_relativo(exacto, aproximado) * 100

def error_por_refinamiento(metodo, a, b, f, n):
    """
    Estima el error de I(n) sin conocer el valor exacto:
        |I(2n) - I(n)|
    Es una cota razonable del error de I(n) cuando el método ya converge.
    """
    validar_limites(a, b)
    validar_subintervalos(n)
    return abs(metodo(a, b, f, 2 * n) - metodo(a, b, f, n))


def refinar_hasta_tolerancia(metodo, a, b, f, tol=1e-6, n_inicial=10, n_max=100_000):
    """
    Duplica n hasta que |I(2n) - I(n)| < tol.
    Devuelve (aproximacion, n_usado, error_estimado).
    Lanza NoConvergenciaError si no converge antes de n_max.
    """
    validar_limites(a, b)
    validar_subintervalos(n_inicial)
    validar_positivo(tol, "tol")

    n = n_inicial
    err = math.inf
    actual = metodo(a, b, f, n)
    while n <= n_max:
        siguiente = metodo(a, b, f, 2 * n)
        err = abs(siguiente - actual)
        if err < tol:
            return siguiente, 2 * n, err
        actual, n = siguiente, 2 * n
    raise NoConvergenciaError(
        f"No se alcanzó la tolerancia {tol} con n <= {n_max} "
        f"(último error estimado: {err:.3e})."
    )

ORDEN_TEORICO = {
    "rectangulo": 1,
    "punto_medio": 2,
    "trapecio": 2,
    "simpson_13": 4,
    "simpson_38": 4,
}


def orden_convergencia(metodo, a, b, f, n, exacto):
    """
    p ≈ log2( e(n) / e(2n) ).
    Debería dar ≈1 (rectángulo), ≈2 (trapecio, punto medio), ≈4 (Simpson).
    Devuelve math.inf si el método es exacto para esa función (error 0).
    """
    validar_limites(a, b)
    validar_subintervalos(n)
    e1 = error_absoluto(exacto, metodo(a, b, f, n))
    e2 = error_absoluto(exacto, metodo(a, b, f, 2 * n))
    if e1 == 0 or e2 == 0:
        return math.inf
    return math.log2(e1 / e2)

_COTAS = {
    "rectangulo":  (lambda L: L**2 / 2,   1),
    "punto_medio": (lambda L: L**3 / 24,  2),
    "trapecio":    (lambda L: L**3 / 12,  2),
    "simpson_13":  (lambda L: L**5 / 180, 4),
    "simpson_38":  (lambda L: L**5 / 80,  4),
}


def _constante_cota(metodo_nombre):
    if metodo_nombre not in _COTAS:
        raise MetodoDesconocidoError(
            f"Método '{metodo_nombre}' desconocido. "
            f"Opciones: {', '.join(_COTAS)}."
        )
    return _COTAS[metodo_nombre]


def estimar_max_derivada(f, a, b, orden, muestras=1000, h=1e-2):
    """
    Estima max |f^(orden)(x)| en [a, b] (orden = 1, 2 o 4) con diferencias
    finitas centradas, muestreando el intervalo. Es una ESTIMACIÓN, no una
    cota rigurosa. Evita los bordes para no salirse del dominio de f.
    """
    validar_limites(a, b)
    if orden not in (1, 2, 4):
        raise ParametroInvalidoError(f"orden debe ser 1, 2 o 4 (recibido: {orden}).")
    margen = (orden // 2 + (orden % 2)) * h
    if b - a <= 2 * margen:
        raise LimitesInvalidosError(
            "Intervalo demasiado pequeño para estimar la derivada."
        )

    g = funcion_segura(f)

    def derivada(x):
        if orden == 1:
            return (g(x + h) - g(x - h)) / (2 * h)
        if orden == 2:
            return (g(x + h) - 2 * g(x) + g(x - h)) / h**2
        return (g(x + 2*h) - 4*g(x + h) + 6*g(x) - 4*g(x - h) + g(x - 2*h)) / h**4

    lo, hi = a + margen, b - margen
    paso = (hi - lo) / muestras
    return max(abs(derivada(lo + i * paso)) for i in range(muestras + 1))


def cota_error(metodo_nombre, a, b, n, M):
    validar_limites(a, b)
    validar_subintervalos(n)
    validar_no_negativo(M, "M")
    K, p = _constante_cota(metodo_nombre)
    return K(b - a) * M / n**p


def n_requerido(metodo_nombre, a, b, M, tol):
    validar_limites(a, b)
    validar_no_negativo(M, "M")
    validar_positivo(tol, "tol")
    K, p = _constante_cota(metodo_nombre)
    if M == 0:
        return 1

    n = max(1, math.ceil((K(b - a) * M / tol) ** (1 / p)))
    if metodo_nombre == "simpson_13" and n % 2:
        n += 1
    if metodo_nombre == "simpson_38" and n % 3:
        n += 3 - n % 3
    return n

def resumen_error(metodo, a, b, f, n, exacto=None):
    validar_limites(a, b)
    validar_subintervalos(n)
    aprox = metodo(a, b, f, n)
    res = {"n": n, "aproximacion": aprox}

    if exacto is not None:
        res["exacto"] = exacto
        res["error_absoluto"] = error_absoluto(exacto, aprox)
        if exacto != 0:
            res["error_relativo"] = error_relativo(exacto, aprox)
            res["error_porcentual"] = error_porcentual(exacto, aprox)
    res["error_estimado_refinamiento"] = abs(metodo(a, b, f, 2 * n) - aprox)
    return res


def tabla_convergencia(metodo, a, b, f, ns, exacto=None):
    validar_limites(a, b)
    filas, previo = [], None
    for n in ns:
        validar_subintervalos(n)
        aprox = metodo(a, b, f, n)
        fila = {"n": n, "aproximacion": aprox}
        if exacto is not None:
            fila["error_absoluto"] = error_absoluto(exacto, aprox)
            if exacto != 0:
                fila["error_relativo"] = error_relativo(exacto, aprox)
        if previo is not None:
            fila["dif_con_anterior"] = abs(aprox - previo)
        previo = aprox
        filas.append(fila)
    return filas


def comparar_metodos(metodos, a, b, f, n, exacto=None):
    validar_limites(a, b)
    validar_subintervalos(n)
    filas = []
    for nombre, metodo in metodos.items():
        try:
            aprox = metodo(a, b, f, n)
        except (ErrorIntegral, ValueError, ArithmeticError) as e:
            filas.append({"metodo": nombre, "error": f"{type(e).__name__}: {e}"})
            continue
        fila = {"metodo": nombre, "aproximacion": aprox}
        if exacto is not None:
            fila["error_absoluto"] = error_absoluto(exacto, aprox)
            if exacto != 0:
                fila["error_relativo"] = error_relativo(exacto, aprox)
        filas.append(fila)

    if exacto is not None:
        filas.sort(key=lambda r: r.get("error_absoluto", math.inf))
    return filas


def imprimir_tabla(filas):
    if not filas:
        print("(sin datos)")
        return
    columnas = []
    for fila in filas:
        for k in fila:
            if k not in columnas:
                columnas.append(k)

    def fmt(v):
        if isinstance(v, float):
            return f"{v:.6e}" if (v != 0 and (abs(v) < 1e-3 or abs(v) >= 1e6)) else f"{v:.8f}"
        return str(v)

    celdas = [[fmt(fila.get(c, "")) for c in columnas] for fila in filas]
    anchos = [max(len(c), *(len(r[i]) for r in celdas)) for i, c in enumerate(columnas)]
    print(" | ".join(c.ljust(w) for c, w in zip(columnas, anchos)))
    print("-+-".join("-" * w for w in anchos))
    for r in celdas:
        print(" | ".join(v.ljust(w) for v, w in zip(r, anchos)))