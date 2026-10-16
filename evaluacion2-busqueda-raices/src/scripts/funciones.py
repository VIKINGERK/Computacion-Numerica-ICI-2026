import numpy as np

Tolerancia = 1e-6
Max_iteraciones = 100


# Polinomica Simple
def func_polinomica_simple(x):
    return x**3 - x - 2

def dfunc_polinomica_simple(x):
    return 3 * x**2 - 1

def d2func_polinomica_simple(x):
    return 6 * x

def g_polinomica_simple(x):
    return np.cbrt(x + 2)


# Polinomica Doble
def func_polinomica_doble(x):
    return (x - 2)**2

def dfunc_polinomica_doble(x):
    return 2 * (x - 2)

def d2func_polinomica_doble(x):
    return np.full_like(x, 2.0) if isinstance(x, np.ndarray) else 2.0

def g_polinomica_doble(x):
    return x + (x - 2)**2


# Logaritmica
def func_log(x):
    return np.log(x) + x - 4

def dfunc_log(x):
    return (1.0 / x) + 1.0

def d2func_log(x):
    return -1.0 / (x**2)

def g_log(x):
    return 4.0 - np.log(x)


# Exponencial
def func_exponencial(x):
    return np.exp(-x) - x

def dfunc_exponencial(x):
    return -np.exp(-x) - 1.0

def d2func_exponencial(x):
    return np.exp(-x)

def g_exponencial(x):
    return np.exp(-x)


# Trigonometrica
def func_trigonometrica(x):
    return np.cos(x) - x

def dfunc_trigonometrica(x):
    return -np.sin(x) - 1.0

def d2func_trigonometrica(x):
    return -np.cos(x)

def g_trigonometrica(x):
    return np.cos(x)


# Mixta
def func_mixta(x):
    return np.sqrt(x) - np.cos(x)

def dfunc_mixta(x):
    return 0.5 / np.sqrt(x) + np.sin(x)

def d2func_mixta(x):
    return -0.25 * (x**-1.5) + np.cos(x)

def g_mixta(x):
    return x - 0.8 * (np.sqrt(x) - np.cos(x))


FUNCIONES = [
    {
        "id": "polinomica_simple",
        "categoria": "Polinómica (raíz simple)",
        "texto": "f(x) = x^3 − x − 2",
        "f": func_polinomica_simple,
        "df": dfunc_polinomica_simple,
        "d2f": d2func_polinomica_simple,
        "g": g_polinomica_simple,
        "g_texto": "g(x) = (x + 2)^(1/3)",
        "a": 1.0, "b": 2.0, "x0": 1.5, "x1": 2.0, "x0_secante": 1.0,
        "tipo": "simple",
    },
    {
        "id": "polinomica_doble",
        "categoria": "Polinómica (raíz doble)",
        "texto": "f(x) = (x − 2)^2",
        "f": func_polinomica_doble,
        "df": dfunc_polinomica_doble,
        "d2f": d2func_polinomica_doble,
        "g": g_polinomica_doble,
        "g_texto": "g(x) = x + (x − 2)^2",
        "a": 1.0, "b": 3.0, "x0": 1.2, "x1": 1.5, "x0_secante": 1.2,
        "tipo": "doble",
        "raiz_exacta": 2.0,
    },
    {
        "id": "logaritmica",
        "categoria": "Logarítmica",
        "texto": "f(x) = ln(x) + x − 4",
        "f": func_log,
        "df": dfunc_log,
        "d2f": d2func_log,
        "g": g_log,
        "g_texto": "g(x) = 4 − ln(x)",
        "a": 2.0, "b": 3.0, "x0": 2.5, "x1": 3.0, "x0_secante": 2.0,
        "tipo": "simple",
    },
    {
        "id": "exponencial",
        "categoria": "Exponencial",
        "texto": "f(x) = e^(−x) − x",
        "f": func_exponencial,
        "df": dfunc_exponencial,
        "d2f": d2func_exponencial,
        "g": g_exponencial,
        "g_texto": "g(x) = e^(−x)",
        "a": 0.0, "b": 1.0, "x0": 0.5, "x1": 1.0, "x0_secante": 0.0,
        "tipo": "simple",
    },
    {
        "id": "trigonometrica",
        "categoria": "Trigonométrica",
        "texto": "f(x) = cos(x) − x",
        "f": func_trigonometrica,
        "df": dfunc_trigonometrica,
        "d2f": d2func_trigonometrica,
        "g": g_trigonometrica,
        "g_texto": "g(x) = cos(x)",
        "a": 0.0, "b": 1.0, "x0": 0.5, "x1": 1.0, "x0_secante": 0.0,
        "tipo": "simple",
    },
    {
        "id": "mixta",
        "categoria": "Mixta",
        "texto": "f(x) = sqrt(x) − cos(x)",
        "f": func_mixta,
        "df": dfunc_mixta,
        "d2f": d2func_mixta,
        "g": g_mixta,
        "g_texto": "g(x) = x − 0.8·(sqrt(x) − cos x)",
        "a": 0.1, "b": 1.0, "x0": 0.55, "x1": 1.0, "x0_secante": 0.1,
        "tipo": "simple",
    },
]


def raiz_referencia(fun):
    if "raiz_exacta" in fun:
        return fun["raiz_exacta"]

    f, a, b = fun["f"], fun["a"], fun["b"]
    
    # Bisección
    for _ in range(200):
        c = (a + b) / 2.0
        if f(a) * f(c) <= 0:
            b = c
        else:
            a = c

    return (a + b) / 2.0