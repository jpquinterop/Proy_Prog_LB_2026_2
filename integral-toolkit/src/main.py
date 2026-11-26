import argparse
import ast
import math
import operator
import sys

from calculo_integral import METODOS, __version__, listar_funciones, obtener_funcion
from calculo_integral.exceptions.exception import ErrorIntegral
from calculo_integral.integral_definida.metodos_numericos.calculo_errores import (
    error_absoluto,
    error_por_refinamiento,
    error_relativo,
)

_OPERADORES = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}
_CONSTANTES = {"pi": math.pi, "e": math.e}

def _evaluar(nodo):
    if isinstance(nodo, ast.Expression):
        return _evaluar(nodo.body)
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
        return nodo.value
    if isinstance(nodo, ast.Name) and nodo.id in _CONSTANTES:
        return _CONSTANTES[nodo.id]
    if isinstance(nodo, ast.BinOp) and type(nodo.op) in _OPERADORES:
        return _OPERADORES[type(nodo.op)](_evaluar(nodo.left), _evaluar(nodo.right))
    if isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _OPERADORES:
        return _OPERADORES[type(nodo.op)](_evaluar(nodo.operand))
    raise ValueError("expresión no permitida")

def numero(texto):
    try:
        return float(_evaluar(ast.parse(texto.strip(), mode="eval")))
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError, TypeError):
        raise argparse.ArgumentTypeError(f"'{texto}' no es un número válido") from None

def crear_parser():
    p = argparse.ArgumentParser(
        prog="integral-toolkit",
        description="Área bajo la curva (usa |f|) con métodos numéricos.",
    )
    p.add_argument("-f", "--funcion", help="nombre de la función (ver --listar)")
    p.add_argument("-a", type=numero, help="límite inferior (acepta pi, 2*pi, ...)")
    p.add_argument("-b", type=numero, help="límite superior")
    p.add_argument("-m", "--metodo", choices=sorted(METODOS), default="simpson_13")
    p.add_argument("-n", type=int, default=100, help="subintervalos (por defecto 100)")
    p.add_argument("--exacto", type=numero, help="valor exacto del área, para calcular el error")
    p.add_argument("--graficar", action="store_true", help="muestra la gráfica")
    p.add_argument("--guardar", metavar="ARCHIVO", help="guarda la gráfica en un archivo")
    p.add_argument("--listar", action="store_true", help="lista las funciones disponibles")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return p

def main(argv=None):
    parser = crear_parser()
    args = parser.parse_args(argv)

    if args.listar:
        print("\n".join(listar_funciones()))
        return 0
    if args.funcion is None or args.a is None or args.b is None:
        parser.error("se requieren --funcion, -a y -b (o usa --listar)")

    try:
        f = obtener_funcion(args.funcion)
        metodo = METODOS[args.metodo]
        area = metodo(args.a, args.b, f, args.n)

        print(f"Función  : {args.funcion}")
        print(f"Intervalo: [{args.a:g}, {args.b:g}]")
        print(f"Método   : {args.metodo} (n = {args.n})")
        print(f"Área ≈ {area:.8f}")
        print(f"Error estimado (refinamiento): {error_por_refinamiento(metodo, args.a, args.b, f, args.n):.3e}")
        if args.exacto is not None:
            print(f"Error absoluto: {error_absoluto(args.exacto, area):.3e}")
            if args.exacto != 0:
                print(f"Error relativo: {error_relativo(args.exacto, area):.3e}")

        if args.graficar or args.guardar:
            from calculo_integral.graficos import graficar_area  # matplotlib solo si hace falta

            graficar_area(
                f, args.a, args.b, n=args.n, metodo=args.metodo, exacto=args.exacto,
                metodo_fn=metodo, guardar=args.guardar, mostrar=args.graficar,
            )
    except ErrorIntegral as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())