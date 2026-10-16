import numpy as np

Error_maximo_aceptable = 1e-6
Iteraciones_maximas = 100


def _resultado(metodo, hist, estado, nota=""):
    return {
        "metodo": metodo,
        "historial": hist,
        "convergio": estado == "convergio",
        "estado": estado,
        "nota": nota,
    }


def _finito(*vals):
    return all(np.isfinite(v) and abs(v) < 1e12 for v in vals)


def biseccion(f, a, b, Error_maximo_aceptable=Error_maximo_aceptable, Iteraciones_maximas=Iteraciones_maximas):
    nombre = "Biseccion"
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        return _resultado(nombre, [], "no_aplica", "sin cambio de signo en [a, b]")
    hist = []
    for k in range(1, Iteraciones_maximas + 1):
        c = 0.5 * (a + b)
        fc = f(c)
        paso = 0.5 * (b - a)
        hist.append((k, c, fc, paso))
        if abs(fc) < Error_maximo_aceptable or paso < Error_maximo_aceptable:
            return _resultado(nombre, hist, "convergio")
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    return _resultado(nombre, hist, "no_converge", "se alcanzo el tope de iteraciones")


def falsa_posicion(f, a, b, Error_maximo_aceptable=Error_maximo_aceptable, Iteraciones_maximas=Iteraciones_maximas):
    nombre = "Falsa posicion"
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        return _resultado(nombre, [], "no_aplica", "sin cambio de signo en [a, b]")
    hist = []
    c_prev = np.inf
    for k in range(1, Iteraciones_maximas + 1):
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        paso = abs(c - c_prev)
        hist.append((k, c, fc, paso))
        if abs(fc) < Error_maximo_aceptable or paso < Error_maximo_aceptable:
            return _resultado(nombre, hist, "convergio")
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        c_prev = c
    return _resultado(nombre, hist, "no_converge", "se alcanzo el tope de iteraciones")


def punto_fijo(f, g, x0, Error_maximo_aceptable=Error_maximo_aceptable, Iteraciones_maximas=Iteraciones_maximas):
    nombre = "Punto fijo"
    hist = []
    x = x0
    for k in range(1, Iteraciones_maximas + 1):
        with np.errstate(all="ignore"):
            x_new = g(x)
        if not _finito(x_new):
            return _resultado(nombre, hist, "falla", "la iteracion diverge o sale del dominio")
        fx = f(x_new)
        paso = abs(x_new - x)
        hist.append((k, x_new, fx, paso))
        x = x_new
        if abs(fx) < Error_maximo_aceptable or paso < Error_maximo_aceptable:
            return _resultado(nombre, hist, "convergio")
    return _resultado(nombre, hist, "no_converge", "se alcanzo el tope de iteraciones")


def secante(f, x0, x1, Error_maximo_aceptable=Error_maximo_aceptable, Iteraciones_maximas=Iteraciones_maximas):
    nombre = "Secante"
    hist = []
    f0, f1 = f(x0), f(x1)
    for k in range(1, Iteraciones_maximas + 1):
        if f1 == f0:
            return _resultado(nombre, hist, "falla", "f(x_n) = f(x_n-1): division por cero")
        with np.errstate(all="ignore"):
            x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        if not _finito(x2):
            return _resultado(nombre, hist, "falla", "la iteracion diverge o sale del dominio")
        f2 = f(x2)
        paso = abs(x2 - x1)
        hist.append((k, x2, f2, paso))
        x0, f0, x1, f1 = x1, f1, x2, f2
        if abs(f2) < Error_maximo_aceptable or paso < Error_maximo_aceptable:
            return _resultado(nombre, hist, "convergio")
    return _resultado(nombre, hist, "no_converge", "se alcanzo el tope de iteraciones")


def newton(f, df, x0, Error_maximo_aceptable=Error_maximo_aceptable, Iteraciones_maximas=Iteraciones_maximas):
    nombre = "newton-Raphson"
    hist = []
    x = x0
    for k in range(1, Iteraciones_maximas + 1):
        d = df(x)
        if d == 0:
            return _resultado(nombre, hist, "falla", "f'(x) = 0: division por cero")
        with np.errstate(all="ignore"):
            x_new = x - f(x) / d
        if not _finito(x_new):
            return _resultado(nombre, hist, "falla", "la iteracion diverge o sale del dominio")
        fx = f(x_new)
        paso = abs(x_new - x)
        hist.append((k, x_new, fx, paso))
        x = x_new
        if abs(fx) < Error_maximo_aceptable or paso < Error_maximo_aceptable:
            return _resultado(nombre, hist, "convergio")
    return _resultado(nombre, hist, "no_converge", "se alcanzo el tope de iteraciones")


def newton_mejorado(f, df, d2f, x0, Error_maximo_aceptable=Error_maximo_aceptable, Iteraciones_maximas=Iteraciones_maximas):
    nombre = "newton mejorado"
    hist = []
    x = x0
    for k in range(1, Iteraciones_maximas + 1):
        fx, d1, d2 = f(x), df(x), d2f(x)
        den = d1 * d1 - fx * d2
        if den == 0:
            return _resultado(nombre, hist, "falla", "f'^2 - f f'' = 0: division por cero")
        with np.errstate(all="ignore"):
            x_new = x - fx * d1 / den
        if not _finito(x_new):
            return _resultado(nombre, hist, "falla", "la iteracion diverge o sale del dominio")
        f_new = f(x_new)
        paso = abs(x_new - x)
        hist.append((k, x_new, f_new, paso))
        x = x_new
        if abs(f_new) < Error_maximo_aceptable or paso < Error_maximo_aceptable:
            return _resultado(nombre, hist, "convergio")
    return _resultado(nombre, hist, "no_converge", "se alcanzo el tope de iteraciones")


def estimar_orden(errores):
    e = np.asarray(errores, dtype=float)
    ps = []
    for i in range(1, len(e) - 1):
        trio = e[i - 1:i + 2]
        if np.all(trio > 1e-12) and np.all(trio < 1) and e[i] != e[i - 1] and e[i + 1] != e[i]:
            num = np.log(e[i + 1] / e[i])
            den = np.log(e[i] / e[i - 1])
            if den != 0:
                ps.append(num / den)
    return float(np.median(ps)) if ps else float("nan")
