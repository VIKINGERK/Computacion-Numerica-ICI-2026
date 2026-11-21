import math

MODOS = ("sin_pivoteo", "parcial", "escalado")


def _nuevo():
    return {"mul": 0, "div": 0, "sum": 0, "res": 0,
            "cmp": 0, "div_piv": 0, "swap": 0}


class Contador:
    def __init__(self, n):
        self.n = n
        self.pre = _nuevo()                       # escalas de fila
        self.pasos = [_nuevo() for _ in range(n - 1)]
        self.sust = _nuevo()                      # sustitución regresiva

    def flops(self, d):
        return d["mul"] + d["div"] + d["sum"] + d["res"]

    def muldiv(self, d):
        return d["mul"] + d["div"]

    def sumres(self, d):
        return d["sum"] + d["res"]

    def flops_eliminacion(self):
        return sum(self.flops(d) for d in self.pasos)

    def flops_total(self):
        return self.flops_eliminacion() + self.flops(self.sust)

    def comparaciones(self):
        return self.pre["cmp"] + sum(d["cmp"] for d in self.pasos)

    def divisiones_pivoteo(self):
        return self.pre["div_piv"] + sum(d["div_piv"] for d in self.pasos)

    def intercambios(self):
        return sum(d["swap"] for d in self.pasos)


class Eliminacion:
    def __init__(self, modo, n, U, c, L, permutacion, contador, max_inicial=0.0):
        self.modo = modo
        self.n = n
        self.U = U
        self.c = c
        self.L = L
        self.permutacion = permutacion
        self.contador = contador
        self.trazas = []
        self.max_mult = 0.0
        self.max_mult_pos = (0, 0)
        self.mult_max_por_paso = []
        self.crecimiento_por_paso = []
        self.max_inicial = max_inicial
        self.factor_crecimiento = 1.0
        self.pivotes = []
        self.bits_por_paso = []
        self.bits_alineamiento_max = 0.0


def eliminar(A, b, modo="escalado", barrer_col_k=False, recalcular_mult=False):
    n = len(A)
    M = [[float(v) for v in fila] for fila in A]
    c = [float(v) for v in b]
    L = [[0.0] * n for _ in range(n)]
    permutacion = list(range(n))
    contador = Contador(n)

    escala = None
    if modo == "escalado":
        escala = []
        for i in range(n):
            s = abs(M[i][0])
            for j in range(1, n):
                contador.pre["cmp"] += 1
                if abs(M[i][j]) > s:
                    s = abs(M[i][j])
            escala.append(s)

    max_inicial = max(abs(v) for fila in M for v in fila)
    res = Eliminacion(modo, n, M, c, L, permutacion, contador, max_inicial=max_inicial)
    mayor = max_inicial

    for k in range(n - 1):
        d = contador.pasos[k]

        # eleccion de pivote
        p = k
        if modo == "parcial":
            mejor = abs(M[k][k])
            for i in range(k + 1, n):
                d["cmp"] += 1
                if abs(M[i][k]) > mejor:
                    mejor, p = abs(M[i][k]), i
        elif modo == "escalado":
            mejor = abs(M[k][k]) / escala[k]
            d["div_piv"] += 1
            for i in range(k + 1, n):
                r = abs(M[i][k]) / escala[i]
                d["div_piv"] += 1
                d["cmp"] += 1
                if r > mejor:
                    mejor, p = r, i
        if p != k:
            d["swap"] += 1
            M[k], M[p] = M[p], M[k]
            c[k], c[p] = c[p], c[k]
            permutacion[k], permutacion[p] = permutacion[p], permutacion[k]
            L[k][:k], L[p][:k] = L[p][:k], L[k][:k]
            if escala is not None:
                escala[k], escala[p] = escala[p], escala[k]
        res.pivotes.append(M[k][k])

        # el barrido va de la columna k+1 en adelante
        akk = M[k][k]
        mmax_paso = 0.0
        bits_paso = 0.0
        for i in range(k + 1, n):
            aik = M[i][k]
            m = aik / akk
            d["div"] += 1
            L[i][k] = m
            if abs(m) > mmax_paso:
                mmax_paso = abs(m)
            if abs(m) > res.max_mult:
                res.max_mult, res.max_mult_pos = abs(m), (i, k)
            if barrer_col_k:                    # variante de contraste
                _ = aik - m * akk
                d["mul"] += 1
                d["res"] += 1
            for j in range(k + 1, n):
                if recalcular_mult:             # variante penalizada
                    m = aik / akk
                    d["div"] += 1
                prod = m * M[k][j]
                d["mul"] += 1
                if prod != 0.0 and M[i][j] != 0.0:
                    perdida = math.log2(abs(prod) / abs(M[i][j]))
                    if perdida > bits_paso:
                        bits_paso = perdida
                M[i][j] -= prod
                d["res"] += 1
            if recalcular_mult:
                m = aik / akk
                d["div"] += 1
            c[i] -= m * c[k]                    # actualización de b
            d["mul"] += 1
            d["res"] += 1
            M[i][k] = 0.0                       # anulado por construcción

        res.mult_max_por_paso.append(mmax_paso)
        res.bits_por_paso.append(bits_paso)
        res.bits_alineamiento_max = max(res.bits_alineamiento_max, bits_paso)
        mayor_paso = max(abs(v) for fila in M for v in fila)
        res.crecimiento_por_paso.append(mayor_paso)
        mayor = max(mayor, mayor_paso)
        res.trazas.append(([fila[:] + [c[i]] for i, fila in enumerate(M)], permutacion[:]))

    res.pivotes.append(M[n - 1][n - 1])
    res.factor_crecimiento = mayor / max_inicial
    return res


def sustitucion_regresiva(U, y, d=None):
    n = len(U)
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = y[i]
        for j in range(i + 1, n):
            s -= U[i][j] * x[j]
            if d is not None:
                d["mul"] += 1
                d["res"] += 1
        x[i] = s / U[i][i]
        if d is not None:
            d["div"] += 1
    return x


def resolver_con_LU(el, rhs, d=None):
    n = el.n
    y = [rhs[el.permutacion[i]] for i in range(n)]
    for i in range(n):
        for j in range(i):
            y[i] -= el.L[i][j] * y[j]
            if d is not None:
                d["mul"] += 1
                d["res"] += 1
    return sustitucion_regresiva(el.U, y, d)


def resolver_transpuesta_LU(el, z):
    n = el.n
    w = [0.0] * n                               # U^T w = z
    for i in range(n):
        s = z[i]
        for j in range(i):
            s -= el.U[j][i] * w[j]
        w[i] = s / el.U[i][i]
    v = [0.0] * n                               # L^T v = w
    for i in range(n - 1, -1, -1):
        s = w[i]
        for j in range(i + 1, n):
            s -= el.L[j][i] * v[j]
        v[i] = s
    y = [0.0] * n                               # y = P^T v
    for i in range(n):
        y[el.permutacion[i]] = v[i]
    return y


def resolver(A, b, modo="escalado", **kw):
    el = eliminar(A, b, modo, **kw)
    x = sustitucion_regresiva(el.U, el.c, el.contador.sust)
    return el, x