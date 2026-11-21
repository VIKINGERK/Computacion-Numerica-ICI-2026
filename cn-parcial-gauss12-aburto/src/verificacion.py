import math
from decimal import Decimal, localcontext
from fractions import Fraction

from gauss import resolver_con_LU, resolver_transpuesta_LU


def leer_matriz_texto(ruta_archivo):
    with open(ruta_archivo, encoding="utf-8") as archivo:
        return [linea.strip().split(",") for linea in archivo if linea.strip()]


def leer_vector_texto(ruta_archivo):
    with open(ruta_archivo, encoding="utf-8") as archivo:
        return [linea.strip() for linea in archivo if linea.strip()]


def a_fracciones(lista_textos):
    if lista_textos and isinstance(lista_textos[0], list):
        return [[Fraction(texto) for texto in fila] for fila in lista_textos]
    return [Fraction(texto) for texto in lista_textos]


def a_floats(lista_textos):
    if lista_textos and isinstance(lista_textos[0], list):
        return [[float(texto) for texto in fila] for fila in lista_textos]
    return [float(texto) for texto in lista_textos]


def solucion_racional(matriz_exacta, vector_exacto):
    dimension = len(matriz_exacta)
    matriz_aumentada = [
        fila[:] + [vector_exacto[indice_fila]]
        for indice_fila, fila in enumerate(matriz_exacta)
    ]
    for paso in range(dimension):
        indice_pivote = next(
            indice
            for indice in range(paso, dimension)
            if matriz_aumentada[indice][paso] != 0
        )
        matriz_aumentada[paso], matriz_aumentada[indice_pivote] = (
            matriz_aumentada[indice_pivote],
            matriz_aumentada[paso],
        )
        for indice_fila in range(paso + 1, dimension):
            multiplicador = matriz_aumentada[indice_fila][paso] / matriz_aumentada[paso][paso]
            for indice_columna in range(paso, dimension + 1):
                matriz_aumentada[indice_fila][indice_columna] -= (
                    multiplicador * matriz_aumentada[paso][indice_columna]
                )
    solucion = [Fraction(0)] * dimension
    for indice_fila in range(dimension - 1, -1, -1):
        suma_parcial = matriz_aumentada[indice_fila][dimension] - sum(
            matriz_aumentada[indice_fila][indice_columna] * solucion[indice_columna]
            for indice_columna in range(indice_fila + 1, dimension)
        )
        solucion[indice_fila] = suma_parcial / matriz_aumentada[indice_fila][indice_fila]
    return solucion


def residuo_exacto(matriz_exacta, vector_exacto, solucion):
    solucion_fraccion = [Fraction(valor) for valor in solucion]
    return [
        vector_exacto[indice_fila]
        - sum(
            matriz_exacta[indice_fila][indice_columna] * solucion_fraccion[indice_columna]
            for indice_columna in range(len(solucion_fraccion))
        )
        for indice_fila in range(len(vector_exacto))
    ]


def norma_inf(vector):
    return max(abs(elemento) for elemento in vector)


def a_decimal(fraccion, precision=60):
    with localcontext() as contexto:
        contexto.prec = precision
        return Decimal(fraccion.numerator) / Decimal(fraccion.denominator)


def fmt_sci(valor, cifras_significativas):
    if isinstance(valor, Fraction):
        valor = a_decimal(valor)
    elif isinstance(valor, float):
        valor = Decimal(valor)
    return format(valor, f".{max(cifras_significativas - 1, 0)}e")


def digitos_correctos(solucion, solucion_referencia):
    lista_digitos = []
    for valor_calculado, valor_referencia in zip(solucion, solucion_referencia):
        error = abs((Fraction(valor_calculado) - valor_referencia) / valor_referencia)
        if error == 0:
            lista_digitos.append(30.0)
        else:
            lista_digitos.append(-math.log10(float(error)))
    return lista_digitos


def refinar(
    eliminacion,
    matriz_exacta,
    vector_exacto,
    solucion_inicial,
    solucion_referencia,
    maximo_pasadas,
    contador_operaciones,
    tol=None,
):
    solucion_actual = [Fraction(valor) for valor in solucion_inicial]
    norma_referencia = norma_inf(solucion_referencia)
    historial = []

    for iteracion in range(maximo_pasadas):
        residuo = residuo_exacto(matriz_exacta, vector_exacto, solucion_actual)
        diferencia_referencia = [
            solucion_actual[indice] - solucion_referencia[indice]
            for indice in range(len(solucion_actual))
        ]
        registro = {
            "iter": iteracion,
            "residuo_inf": norma_inf(residuo),
            "error_inf_rel": norma_inf(diferencia_referencia) / norma_referencia,
            "x": solucion_actual[:],
        }
        correccion = resolver_con_LU(
            eliminacion, [float(valor) for valor in residuo], contador_operaciones
        )
        registro["delta"] = correccion
        registro["delta_inf_rel"] = Fraction(max(abs(valor) for valor in correccion)) / norma_referencia
        historial.append(registro)
        solucion_actual = [
            solucion_actual[indice] + Fraction(correccion[indice])
            for indice in range(len(solucion_actual))
        ]
        if tol is not None and registro["delta_inf_rel"] < Fraction(tol):
            break

    residuo = residuo_exacto(matriz_exacta, vector_exacto, solucion_actual)
    diferencia_final = [
        solucion_actual[indice] - solucion_referencia[indice]
        for indice in range(len(solucion_actual))
    ]
    historial.append({
        "iter": len(historial),
        "residuo_inf": norma_inf(residuo),
        "error_inf_rel": norma_inf(diferencia_final) / norma_referencia,
        "x": solucion_actual[:],
    })
    return historial, solucion_actual


def _estimar_norma1_inversa(resolver_directo, resolver_transpuesto, dimension, maximo_iteraciones=6):
    vector_x = [1.0 / dimension] * dimension
    estimacion = 0.0
    for iteracion in range(maximo_iteraciones):
        vector_y = resolver_directo(vector_x)
        estimacion_nueva = sum(abs(valor) for valor in vector_y)
        vector_signos = [1.0 if valor >= 0 else -1.0 for valor in vector_y]
        vector_z = resolver_transpuesto(vector_signos)
        indice_maximo = max(range(dimension), key=lambda indice: abs(vector_z[indice]))
        if iteracion > 0 and estimacion_nueva <= estimacion:
            break
        estimacion = estimacion_nueva
        producto_punto = sum(
            valor_z * valor_x for valor_z, valor_x in zip(vector_z, vector_x)
        )
        if abs(vector_z[indice_maximo]) <= producto_punto:
            break
        vector_x = [0.0] * dimension
        vector_x[indice_maximo] = 1.0
    return estimacion


def estimar_kappa(eliminacion, matriz):
    dimension = len(matriz)
    norma_1 = max(
        sum(abs(matriz[indice_fila][indice_columna]) for indice_fila in range(dimension))
        for indice_columna in range(dimension)
    )
    norma_infinito = max(sum(abs(valor) for valor in fila) for fila in matriz)
    inversa_1 = _estimar_norma1_inversa(
        lambda vector: resolver_con_LU(eliminacion, vector),
        lambda vector: resolver_transpuesta_LU(eliminacion, vector),
        dimension,
    )
    inversa_infinito = _estimar_norma1_inversa(
        lambda vector: resolver_transpuesta_LU(eliminacion, vector),
        lambda vector: resolver_con_LU(eliminacion, vector),
        dimension,
    )
    return {
        "norma1_A": norma_1,
        "norma1_inv": inversa_1,
        "kappa1": norma_1 * inversa_1,
        "normainf_A": norma_infinito,
        "normainf_inv": inversa_infinito,
        "kappainf": norma_infinito * inversa_infinito,
    }