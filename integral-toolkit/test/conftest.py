import os
import sys

import matplotlib

matplotlib.use("Agg")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RAIZ, "src")
DEFINIDA = os.path.join(SRC, "calculo_integral", "integral_definida")
METODOS = os.path.join(DEFINIDA, "metodos_numericos")

for ruta in (METODOS, DEFINIDA, SRC):
    if ruta not in sys.path:
        sys.path.insert(0, ruta)