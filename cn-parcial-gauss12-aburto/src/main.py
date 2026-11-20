import math
import os
import platform
from fractions import Fraction  # para trabajar con números racionales exactos
import numpy as np
import conteo
import gauss
import verificacion as ver

TOLERANCIA_REFINAMIENTO = Fraction(1, 10 ** 30)
DIGITOS_REFINADA = 30
MAXIMO_PASADAS = 10

def bits_correctos(error_relativo):
    if error_relativo == 0:
        return 53.0
    else:
        return -math.log2(error_relativo)

def escribir_traza(ruta_archivo, corridas):
    dimension = corridas[0][1].n
    lineas_salida = ["TRAZA DE ELIMINACIÓN GAUSSIANA [A | b]", ""]
    for titulo_corrida, eliminacion in corridas:
        lineas_salida.append("=" * 90)
        lineas_salida.append(titulo_corrida)
        lineas_salida.append("=" * 90)
        for paso, (matriz_paso, permutacion_paso) in enumerate(eliminacion.trazas, start=1):
            lineas_salida.append(
                f"\nPaso {paso}/{dimension - 1} | pivote={eliminacion.pivotes[paso - 1]:+.16e} | "
                f"mult_max={eliminacion.mult_max_por_paso[paso - 1]:.6e}"
            )
            cabecera = (
                "fila  "
                + "".join(f"{('c' + str(columna + 1)):>24}" for columna in range(dimension))
                + f"{'b':>24}"
            )
            lineas_salida.append(cabecera)
            for indice_fila, fila in enumerate(matriz_paso):
                etiqueta_fila = f"F{permutacion_paso[indice_fila] + 1}".ljust(6)
                lineas_salida.append(etiqueta_fila + "".join(f"{valor:>24.16e}" for valor in fila))
        ceros_bajo_diagonal = sum(
            1
            for indice_fila in range(dimension)
            for indice_columna in range(indice_fila)
            if eliminacion.U[indice_fila][indice_columna] == 0.0
        )
        lineas_salida.append(
            f"\nCeros bajo diagonal: {ceros_bajo_diagonal}/{dimension * (dimension - 1) // 2}"
        )
        lineas_salida.append(
            f"Permutacion final: {[indice + 1 for indice in eliminacion.permutacion]}\n"
        )
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas_salida) + "\n")


def main():
    os.makedirs("resultados", exist_ok=True)

    # Lectura de datos
    matriz_texto = ver.leer_matriz_texto("datos/matriz_a.csv")
    vector_texto = ver.leer_vector_texto("datos/vector_b.csv")
    dimension = len(matriz_texto)
    matriz_exacta = ver.a_fracciones(matriz_texto)
    vector_exacto = ver.a_fracciones(vector_texto)
    matriz_flotante = ver.a_floats(matriz_texto)
    vector_flotante = ver.a_floats(vector_texto)
    solucion_referencia = ver.solucion_racional(matriz_exacta, vector_exacto)
    norma_referencia = ver.norma_inf(solucion_referencia)

    # Ejecución de corridas
    nombres_modos = {
        "sin_pivoteo": "(i) sin pivoteo",
        "parcial": "pivoteo parcial",
        "escalado": "(ii) pivoteo parcial escalado",
    }
    corridas = {}
    soluciones = {}
    informacion_corridas = {}

    for modo in gauss.MODOS:
        eliminacion, solucion = gauss.resolver(matriz_flotante, vector_flotante, modo)
        corridas[modo] = eliminacion
        soluciones[modo] = solucion
        diferencia_exacta = [
            Fraction(solucion[indice]) - solucion_referencia[indice]
            for indice in range(dimension)
        ]
        error_relativo = float(ver.norma_inf(diferencia_exacta) / norma_referencia)
        digitos_significativos = ver.digitos_correctos(solucion, solucion_referencia)
        residuo_doble = max(
            abs(
                vector_flotante[indice_fila]
                - sum(
                    matriz_flotante[indice_fila][indice_columna] * solucion[indice_columna]
                    for indice_columna in range(dimension)
                )
            )
            for indice_fila in range(dimension)
        )
        informacion_corridas[modo] = {
            "error_relativo": error_relativo,
            "digitos": digitos_significativos,
            "bits_ok": bits_correctos(error_relativo),
            "bits_perdidos": 53.0 - bits_correctos(error_relativo),
            "residuo_doble": residuo_doble,
        }

    eliminacion_escalada = corridas["escalado"]
    solucion_escalada = soluciones["escalado"]

    # Refinamiento iterativo
    contador_refinamiento = {
        clave: 0 for clave in ("mul", "div", "sum", "res", "cmp", "div_piv", "swap")
    }
    historial_refinamiento, solucion_final = ver.refinar(
        eliminacion_escalada,
        matriz_exacta,
        vector_exacto,
        solucion_escalada,
        solucion_referencia,
        MAXIMO_PASADAS,
        contador_refinamiento,
        tol=TOLERANCIA_REFINAMIENTO,
    )
    cantidad_pasadas = len(historial_refinamiento) - 1

    contador_refinamiento_sin_pivoteo = {
        clave: 0 for clave in contador_refinamiento
    }
    historial_refinamiento_sin_pivoteo, _ = ver.refinar(
        corridas["sin_pivoteo"],
        matriz_exacta,
        vector_exacto,
        soluciones["sin_pivoteo"],
        solucion_referencia,
        MAXIMO_PASADAS,
        contador_refinamiento_sin_pivoteo,
        tol=TOLERANCIA_REFINAMIENTO,
    )

    # Condicionamiento y control con biblioteca
    condicionamiento = ver.estimar_kappa(eliminacion_escalada, matriz_flotante)
    matriz_numpy = np.array(matriz_flotante)
    vector_numpy = np.array(vector_flotante)
    solucion_libreria = np.linalg.solve(matriz_numpy, vector_numpy)
    digitos_libreria = ver.digitos_correctos(
        [float(valor) for valor in solucion_libreria], solucion_referencia
    )
    kappa_2 = float(np.linalg.cond(matriz_numpy, 2))
    matriz_equilibrada = matriz_numpy / np.abs(matriz_numpy).max(axis=1)[:, None]
    kappa_2_equilibrada = float(np.linalg.cond(matriz_equilibrada, 2))
    epsilon_maquina = 2.0 ** -52

    # 1. Escritura de traza_eliminacion.txt
    escribir_traza(
        "resultados/traza_eliminacion.txt",
        [
            ("CORRIDA (ii): PIVOTEO PARCIAL ESCALADO", eliminacion_escalada),
            ("CORRIDA (i): SIN PIVOTEO", corridas["sin_pivoteo"]),
        ],
    )

    # 2. Escritura de conteo_flops.md
    with open("resultados/conteo_flops.md", "w", encoding="utf-8") as archivo:
        archivo.write(conteo.reporte_markdown(corridas))

    # 3. Escritura de solucion.csv
    digitos_escalada = [
        int(math.floor(digito)) for digito in informacion_corridas["escalado"]["digitos"]
    ]
    filas_csv = [
        "i,x_pivoteo_escalado,digitos_afirmados_pivoteo_escalado,x_refinada,digitos_afirmados_refinada"
    ]
    for indice in range(dimension):
        filas_csv.append(
            f"{indice + 1},{ver.fmt_sci(solucion_escalada[indice], digitos_escalada[indice])},"
            f"{digitos_escalada[indice]},{ver.fmt_sci(solucion_final[indice], DIGITOS_REFINADA)},{DIGITOS_REFINADA}"
        )
    with open("resultados/solucion.csv", "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(filas_csv) + "\n")

    # 4. Escritura de residuo.txt
    lineas_residuo = ["VERIFICACIÓN Y CONDICIONAMIENTO", "=" * 80, ""]
    lineas_residuo.append("1. RESIDUO EXACTO r = b - A x")
    for modo in ("escalado", "sin_pivoteo"):
        residuo = ver.residuo_exacto(matriz_exacta, vector_exacto, soluciones[modo])
        lineas_residuo.append(f"\n[{nombres_modos[modo]}]")
        for indice, valor in enumerate(residuo, start=1):
            lineas_residuo.append(f"  r[{indice:2d}] = {ver.fmt_sci(valor, 12):>22}")
        lineas_residuo.append(f"  ||r||_inf (exacto) = {ver.fmt_sci(ver.norma_inf(residuo), 6)}")
        lineas_residuo.append(f"  ||r||_inf (float)  = {informacion_corridas[modo]['residuo_doble']:.6e}")

    lineas_residuo.append("\n2. REFINAMIENTO ITERATIVO")
    for titulo_historial, historial in (
        ("Pivoteo parcial escalado", historial_refinamiento),
        ("Sin pivoteo", historial_refinamiento_sin_pivoteo),
    ):
        lineas_residuo.append(f"\n[{titulo_historial}]")
        lineas_residuo.append(
            f"{'pasada':>7} {'||r||_inf':>22} {'error_relativo_inf':>22} {'||delta||/||x||':>22}"
        )
        for registro in historial:
            delta_texto = (
                ver.fmt_sci(registro["delta_inf_rel"], 6)
                if "delta_inf_rel" in registro
                else "-"
            )
            lineas_residuo.append(
                f"{registro['iter']:>7} {ver.fmt_sci(registro['residuo_inf'], 6):>22} "
                f"{ver.fmt_sci(registro['error_inf_rel'], 6):>22} {delta_texto:>22}"
            )

    lineas_residuo.append("\n3. COMPARACIÓN DE CORRIDAS")
    lineas_residuo.append(
        f"{'corrida':<30} {'mult_max':>12} {'crecimiento':>12} {'bits_alin':>10} "
        f"{'error_relativo':>16} {'bits_ok':>8} {'bits_perd':>10}"
    )
    for modo in ("sin_pivoteo", "parcial", "escalado"):
        eliminacion = corridas[modo]
        datos_modo = informacion_corridas[modo]
        lineas_residuo.append(
            f"{nombres_modos[modo]:<30} {eliminacion.max_mult:>12.3e} {eliminacion.factor_crecimiento:>12.3e} "
            f"{eliminacion.bits_alineamiento_max:>10.2f} {datos_modo['error_relativo']:>16.3e} "
            f"{datos_modo['bits_ok']:>8.1f} {datos_modo['bits_perdidos']:>10.1f}"
        )
    lineas_residuo.append("\nDígitos correctos por incógnita:")
    for modo in ("sin_pivoteo", "parcial", "escalado"):
        lineas_residuo.append(
            f"  {nombres_modos[modo]:<30} "
            + " ".join(f"{math.floor(digito):>3d}" for digito in informacion_corridas[modo]["digitos"])
        )

    lineas_residuo.append("\n4. CONDICIONAMIENTO")
    lineas_residuo.append(f"  kappa_1  (Hager-Higham) = {condicionamiento['kappa1']:.4e}")
    lineas_residuo.append(f"  kappa_inf (Hager-Higham) = {condicionamiento['kappainf']:.4e}")
    lineas_residuo.append(
        f"  kappa_2  (numpy)        = {kappa_2:.4e}  (cota kappa_2*eps = {kappa_2 * epsilon_maquina:.3e})"
    )
    lineas_residuo.append(
        f"  kappa_2  (escalada)     = {kappa_2_equilibrada:.4e}  (cota kappa_2*eps = {kappa_2_equilibrada * epsilon_maquina:.3e})"
    )

    lineas_residuo.append("\n5. CONTROL CON NUMPY")
    diferencia_libreria = [
        Fraction(float(solucion_libreria[indice])) - solucion_referencia[indice]
        for indice in range(dimension)
    ]
    error_libreria = float(ver.norma_inf(diferencia_libreria) / norma_referencia)
    diferencia_relativa = max(
        abs(solucion_libreria[indice] - solucion_escalada[indice])
        for indice in range(dimension)
    ) / max(abs(valor) for valor in solucion_escalada)
    lineas_residuo.append(f"  error_relativo_inf = {error_libreria:.3e}")
    lineas_residuo.append(f"  diff_rel_vs_propia = {diferencia_relativa:.3e}")
    lineas_residuo.append(
        "  digitos_ok = " + " ".join(f"{math.floor(digito):>3d}" for digito in digitos_libreria)
    )

    with open("resultados/residuo.txt", "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas_residuo) + "\n")

    # Salida por consola
    print(f"Resultados generados en resultados/ (Python {platform.python_version()}, numpy {np.__version__})")
    for modo in ("sin_pivoteo", "parcial", "escalado"):
        eliminacion = corridas[modo]
        datos_modo = informacion_corridas[modo]
        print(
            f"  {nombres_modos[modo]:<30} | flops={eliminacion.contador.flops_total()} | "
            f"mult_max={eliminacion.max_mult:.3e} | crec={eliminacion.factor_crecimiento:.3e} | "
            f"error_relativo={datos_modo['error_relativo']:.3e}"
        )
    print(
        f"  Refinamiento: {cantidad_pasadas} pasadas | "
        f"error_final={float(historial_refinamiento[-1]['error_inf_rel']):.3e} | "
        f"||r||_inf={float(historial_refinamiento[-1]['residuo_inf']):.3e}"
    )


if __name__ == "__main__":
    main()