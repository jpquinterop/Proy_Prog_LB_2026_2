from calculo_integral.functions import listar_funciones, obtener_funcion
from calculo_integral.integral_definida.metodos_numericos import (
    metodo_rectangulo,
    metodo_trapecio,
    punto_medio,
    regla_simpson,
)

__version__ = "0.1.0"
from . import metodo_rectangulo, metodo_trapecio, punto_medio, regla_simpson

METODOS = {
    "rectangulo": metodo_rectangulo.n,
    "punto_medio": punto_medio.mid_n,
    "trapecio": metodo_trapecio.compuesto_n,
    "simpson_13": regla_simpson.compuesto13_n,
    "simpson_38": regla_simpson.compuesto38_n,
}

__all__ = ["listar_funciones", "obtener_funcion", "METODOS", "__version__"]