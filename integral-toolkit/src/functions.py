import math

functions = {
    # --- Aritméticas / polinómicas ---
    "c":        lambda x: 1,
    "x":        lambda x: x,
    "-x":       lambda x: -x,
    "2x":       lambda x: 2 * x,
    "x^2":      lambda x: x**2,
    "x^3":      lambda x: x**3,
    "x^4":      lambda x: x**4,
    "x^2+1":    lambda x: x**2 + 1,
    "x^3-2x+1": lambda x: x**3 - 2*x + 1,
    "|x|":      lambda x: abs(x),
    "1/x":      lambda x: 1 / x,
    "1/x^2":    lambda x: 1 / x**2,
    "1/(1+x^2)": lambda x: 1 / (1 + x**2),
    "sqrt(x)":  lambda x: math.sqrt(x),
    "cbrt(x)":  lambda x: math.copysign(abs(x) ** (1/3), x),

    # --- Trigonométricas ---
    "sin":      lambda x: math.sin(x),
    "cos":      lambda x: math.cos(x),
    "sin^2":    lambda x: math.sin(x) ** 2,
    "cos^2":    lambda x: math.cos(x) ** 2,
    "sin(x^2)": lambda x: math.sin(x**2),
    "x*sin(x)": lambda x: x * math.sin(x),

    # --- Trigonométricas inversas ---
    "asin":     lambda x: math.asin(x),
    "acos":     lambda x: math.acos(x),
    "atan":     lambda x: math.atan(x),

    # --- Exponenciales y logarítmicas ---
    "e^x":      lambda x: math.exp(x),
    "e^-x":     lambda x: math.exp(-x),
    "e^(x^2)":  lambda x: math.exp(x**2),
    "e^(-x^2)": lambda x: math.exp(-x**2),   # gaussiana
    "2^x":      lambda x: 2**x,
    "ln":       lambda x: math.log(x),
    "log10":    lambda x: math.log10(x),
    "log2":     lambda x: math.log2(x),
    "x*ln(x)":  lambda x: x * math.log(x),
    "x*e^x":    lambda x: x * math.exp(x),

    # --- Geométricas (curvas clásicas como y = f(x)) ---
    "semicirculo": lambda x: math.sqrt(1 - x**2),        # círculo unitario, [-1, 1]
    "semielipse":  lambda x: 0.5 * math.sqrt(4 - x**2),  # a=2, b=1, [-2, 2]
    "parabola":    lambda x: x**2 / 4,
    "triangulo":   lambda x: 1 - abs(x),                 # [-1, 1]
}