
import functools
import math
import numbers
from dataclasses import dataclass

class ErrorIntegral(Exception):
    """Base de todas las excepciones de la librería."""

class TipoInvalidoError(ErrorIntegral, TypeError):
    """Un argumento no es del tipo esperado (texto en vez de número, etc.)."""

class LimitesInvalidosError(ErrorIntegral, ValueError):
    """Límites de integración inválidos (a >= b, no finitos, ...)."""

class SubintervalosInvalidosError(ErrorIntegral, ValueError):
    """n no es un entero positivo (o excede el máximo permitido)."""

class ParametroInvalidoError(ErrorIntegral, ValueError):
    """Un parámetro numérico (tolerancia, M, orden, ...) no es válido."""

class MetodoDesconocidoError(ErrorIntegral, ValueError):
    """El nombre del método pedido no existe."""

class FueraDeDominioError(ErrorIntegral, ValueError):
    """El intervalo se sale del dominio de la función."""

class SingularidadError(FueraDeDominioError):
    """El intervalo contiene un punto donde la función no está definida
    (asíntota): la integral es impropia y estos métodos no la soportan."""

class EvaluacionError(ErrorIntegral, ArithmeticError):
    """f(x) no se pudo evaluar en un punto concreto (división por 0,
    overflow, resultado complejo o no finito)."""

    def __init__(self, x, nombre, causa):
        self.x = x
        self.nombre = nombre
        self.causa = causa
        super().__init__(
            f"No se pudo evaluar {nombre or 'f'}(x) en x = {x!r}: {causa}"
        )

class ErrorRelativoIndefinidoError(ErrorIntegral, ZeroDivisionError):
    """El error relativo no existe porque el valor exacto es 0."""


class NoConvergenciaError(ErrorIntegral, RuntimeError):
    """El refinamiento no alcanzó la tolerancia pedida."""

class FuncionDesconocidaError(ErrorIntegral, ValueError):
    """La función pedida no está en functions.py."""

def _es_real(v):
    return isinstance(v, numbers.Real) and not isinstance(v, bool)

def validar_numero(valor, nombre):
    """Debe ser un número real finito."""
    if not _es_real(valor):
        raise TipoInvalidoError(
            f"'{nombre}' debe ser numérico, no {type(valor).__name__}."
        )
    if not math.isfinite(valor):
        raise ParametroInvalidoError(
            f"'{nombre}' debe ser finito (recibido: {valor})."
        )

def validar_positivo(valor, nombre):
    validar_numero(valor, nombre)
    if valor <= 0:
        raise ParametroInvalidoError(
            f"'{nombre}' debe ser positivo (recibido: {valor})."
        )

def validar_no_negativo(valor, nombre):
    validar_numero(valor, nombre)
    if valor < 0:
        raise ParametroInvalidoError(
            f"'{nombre}' debe ser >= 0 (recibido: {valor})."
        )

def validar_limites(a, b):
    """a y b numéricos, finitos y con a < b."""
    for nombre, v in (("a", a), ("b", b)):
        if not _es_real(v):
            raise TipoInvalidoError(
                f"El límite '{nombre}' debe ser numérico, no {type(v).__name__}."
            )
        if not math.isfinite(v):
            raise LimitesInvalidosError(
                f"El límite '{nombre}' debe ser finito (recibido: {v}). "
                "Las integrales impropias no están soportadas."
            )
    if a == b:
        raise LimitesInvalidosError(
            f"El intervalo tiene longitud 0 (a = b = {a}); la integral es 0."
        )
    if a > b:
        raise LimitesInvalidosError(
            f"Se requiere a < b (recibido a={a}, b={b}). "
            "Intercambia los límites y cambia el signo del resultado."
        )


def validar_subintervalos(n, multiplo=None, n_max=10_000_000):
    """n entero positivo; opcionalmente múltiplo de 'multiplo' y <= n_max."""
    if isinstance(n, bool) or not isinstance(n, numbers.Integral):
        raise TipoInvalidoError(f"n debe ser un entero, no {type(n).__name__}.")
    if n <= 0:
        raise SubintervalosInvalidosError(
            f"n debe ser un entero positivo (recibido: {n})."
        )
    if n > n_max:
        raise SubintervalosInvalidosError(
            f"n = {n} excede el máximo permitido ({n_max})."
        )
    if multiplo is not None and n % multiplo != 0:
        raise SubintervalosInvalidosError(
            f"n debe ser múltiplo de {multiplo} (recibido: {n})."
        )

@dataclass(frozen=True)
class Dominio:
    minimo: float = -math.inf
    maximo: float = math.inf
    min_incluido: bool = True
    max_incluido: bool = True
    excluidos: tuple = ()
    nota: str = ""

    def descripcion(self):
        if self.excluidos:
            pts = ", ".join(str(p) for p in self.excluidos)
            return f"todo R excepto x = {pts}"
        izq = "[" if self.min_incluido and math.isfinite(self.minimo) else "("
        der = "]" if self.max_incluido and math.isfinite(self.maximo) else ")"
        return f"{izq}{self.minimo}, {self.maximo}{der}"

DOMINIOS = {
    # Asíntotas en x = 0
    "1/x":   Dominio(excluidos=(0,), nota="Asíntota vertical en x = 0."),
    "1/x^2": Dominio(excluidos=(0,), nota="Asíntota vertical en x = 0."),

    # Raíz y trigonométricas inversas
    "sqrt(x)": Dominio(minimo=0),
    "asin":    Dominio(minimo=-1, maximo=1),
    "acos":    Dominio(minimo=-1, maximo=1),

    # Logaritmos (x = 0 excluido: la integral converge, pero f(0) no se
    # puede evaluar y el método la evaluaría en el extremo)
    "ln":      Dominio(minimo=0, min_incluido=False, nota="Usa a > 0; f(0) no está definida."),
    "log10":   Dominio(minimo=0, min_incluido=False, nota="Usa a > 0; f(0) no está definida."),
    "log2":    Dominio(minimo=0, min_incluido=False, nota="Usa a > 0; f(0) no está definida."),
    "x*ln(x)": Dominio(minimo=0, min_incluido=False, nota="Usa a > 0; f(0) no se puede evaluar en float."),

    # Curvas geométricas
    "semicirculo": Dominio(minimo=-1, maximo=1),
    "semielipse":  Dominio(minimo=-2, maximo=2),

    # Overflow de float en exp / potencias
    "e^x":      Dominio(minimo=-700, maximo=700, nota="Evita overflow de exp."),
    "e^-x":     Dominio(minimo=-700, maximo=700, nota="Evita overflow de exp."),
    "x*e^x":    Dominio(minimo=-700, maximo=700, nota="Evita overflow de exp."),
    "e^(x^2)":  Dominio(minimo=-26, maximo=26, nota="Evita overflow de exp(x^2)."),
    "2^x":      Dominio(minimo=-1000, maximo=1000, nota="Evita overflow de 2**x."),
}


def validar_dominio(nombre, a, b):
    d = DOMINIOS.get(nombre)
    if d is None:
        return

    for p in d.excluidos:
        if a <= p <= b:
            raise SingularidadError(
                f"'{nombre}' no está definida en x = {p}, y el intervalo "
                f"[{a}, {b}] lo contiene. Dominio: {d.descripcion()}. {d.nota}".strip()
            )

    fuera_izq = a < d.minimo or (a == d.minimo and not d.min_incluido)
    fuera_der = b > d.maximo or (b == d.maximo and not d.max_incluido)
    if fuera_izq or fuera_der:
        raise FueraDeDominioError(
            f"El intervalo [{a}, {b}] se sale del dominio de '{nombre}': "
            f"{d.descripcion()}. {d.nota}".strip()
        )


def nombre_de_funcion(f):
    try:
        from calculo_integral.functions import functions as registro
    except ImportError:
        return None
    original = getattr(f, "_original", f)
    for nombre, g in registro.items():
        if g is original:
            return nombre
    return None

def funcion_segura(f, nombre=None):
    if getattr(f, "_es_segura", False):
        return f

    def segura(x):
        try:
            y = f(x)
        except (ValueError, ZeroDivisionError, OverflowError) as e:
            raise EvaluacionError(x, nombre, e) from e
        if isinstance(y, complex) or not math.isfinite(y):
            raise EvaluacionError(x, nombre, "resultado no real o no finito")
        return y

    segura._es_segura = True
    segura._original = f
    return segura

def controlar_integracion(metodo):
    @functools.wraps(metodo)
    def envoltura(a, b, f, *args, **kwargs):
        validar_limites(a, b)
        if args:
            validar_subintervalos(args[0])
        elif "n" in kwargs:
            validar_subintervalos(kwargs["n"])

        nombre = nombre_de_funcion(f)
        if nombre is not None:
            validar_dominio(nombre, a, b)
        return metodo(a, b, funcion_segura(f, nombre), *args, **kwargs)

    return envoltura