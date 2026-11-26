from . import metodo_rectangulo, metodo_trapecio, punto_medio, regla_simpson

METODOS = {
    "rectangulo": metodo_rectangulo.n,
    "punto_medio": punto_medio.mid_n,
    "trapecio": metodo_trapecio.compuesto_n,
    "simpson_13": regla_simpson.compuesto13_n,
    "simpson_38": regla_simpson.compuesto38_n,
}