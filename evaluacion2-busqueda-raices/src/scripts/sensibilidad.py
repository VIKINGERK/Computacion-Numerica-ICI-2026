import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from funciones import FUNCIONES, Tolerancia, Max_iteraciones
import metodos as m

# Configuración de rutas
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

MAPA_FUNCIONES = {f["id"]: f for f in FUNCIONES}


def registrar_resultado(funcion_id: str, metodo: str, parametro: str, resultado: dict) -> dict:
    historial = resultado.get("historial", [])
    ultima_raiz = historial[-1][1] if historial else ""
    return {
        "funcion_id": funcion_id,
        "metodo": metodo,
        "parametro": parametro,
        "estado": resultado.get("estado", "error"),
        "iteraciones": len(historial),
        "raiz": ultima_raiz,
    }


def ejecutar_experimentos_intervalo(fn_meta: dict):
    resultados = []
    f = fn_meta["f"]
    intervalos = [(1.0, 2.0), (1.4, 1.6), (0.0, 5.0), (-10.0, 10.0), (1.0, 100.0)]

    for a, b in intervalos:
        res_bis = m.biseccion(f, a, b, Tolerancia, Max_iteraciones)
        resultados.append(registrar_resultado(fn_meta["id"], "Bisección", f"[{a}, {b}]", res_bis))

        res_fal = m.falsa_posicion(f, a, b, Tolerancia, Max_iteraciones)
        resultados.append(registrar_resultado(fn_meta["id"], "Falsa posición", f"[{a}, {b}]", res_fal))

    return resultados


def ejecutar_experimentos_punto_inicial(fn_meta: dict, x0_list: list[float]):
    resultados = []
    f = fn_meta["f"]
    df = fn_meta.get("df")
    d2f = fn_meta.get("d2f")
    g = fn_meta.get("g")

    for x0 in x0_list:
        if df:
            r_newton = m.newton(f, df, x0, Tolerancia, Max_iteraciones)
            resultados.append(registrar_resultado(fn_meta["id"], "Newton-Raphson", f"x0={x0}", r_newton))

        if df and d2f:
            r_mejorado = m.newton_mejorado(f, df, d2f, x0, Tolerancia, Max_iteraciones)
            resultados.append(registrar_resultado(fn_meta["id"], "Newton mejorado", f"x0={x0}", r_mejorado))

        r_secante = m.secante(f, x0, x0 + 0.5, Tolerancia, Max_iteraciones)
        resultados.append(registrar_resultado(fn_meta["id"], "Secante", f"x0={x0}, x1={x0 + 0.5}", r_secante))

        if g:
            r_pfijo = m.punto_fijo(f, g, x0, Tolerancia, Max_iteraciones)
            resultados.append(registrar_resultado(fn_meta["id"], "Punto fijo", f"x0={x0}", r_pfijo))

    return resultados


def graficar_sensibilidad_intervalo(filas: list[dict], ruta_salida: Path):
    intervalos_etiquetas = ["[1, 2]", "[1.4, 1.6]", "[0, 5]", "[-10, 10]", "[1, 100]"]
    metodos = ["Bisección", "Falsa posición"]
    colores = ["#2b5c8f", "#d95f02"]
    
    datos_filtrados = [r for r in filas if r["funcion_id"] == "polinomica_simple" and r["metodo"] in metodos]
    
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    ancho = 0.35

    for j, nombre_metodo in enumerate(metodos):
        iteraciones = [r["iteraciones"] for r in datos_filtrados if r["metodo"] == nombre_metodo]
        posiciones_x = np.arange(len(iteraciones)) + (j - 0.5) * ancho
        
        bars = ax.bar(
            posiciones_x, iteraciones, ancho, 
            label=nombre_metodo, 
            color=colores[j], 
            alpha=0.85, 
            edgecolor="black", 
            linewidth=0.6
        )
        
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{int(height)}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 2), textcoords="offset points",
                ha="center", va="bottom", fontsize=8, fontfamily="serif"
            )

    ax.set_xticks(range(len(intervalos_etiquetas)))
    ax.set_xticklabels(intervalos_etiquetas, fontfamily="serif")
    ax.set_xlabel("Intervalo inicial [a, b]", fontsize=10, fontfamily="serif")
    ax.set_ylabel("N° de Iteraciones", fontsize=10, fontfamily="serif")
    ax.set_title("Sensibilidad al intervalo inicial — $f(x) = x^3 - x - 2$", fontsize=11, fontfamily="serif", pad=12)
    
    ax.grid(axis="y", color="#cccccc", linestyle="--", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=True, facecolor="white", edgecolor="none")
    
    fig.tight_layout()
    fig.savefig(ruta_salida, dpi=200)
    plt.close(fig)


def graficar_sensibilidad_x0(filas: list[dict], x0s: list[float], ruta_salida: Path):
    metodos = ["Newton-Raphson", "Newton mejorado", "Secante", "Punto fijo"]
    colores = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a"]
    
    fig, ax = plt.subplots(figsize=(9.5, 4.5))
    ancho = 0.8 / len(metodos)

    for j, nombre_metodo in enumerate(metodos):
        for i, x0 in enumerate(x0s):
            item = next((
                r for r in filas 
                if r["funcion_id"] == "polinomica_simple" 
                and r["metodo"] == nombre_metodo 
                and f"x0={x0}" in r["parametro"]
            ), None)

            pos_x = i + (j - 1.5) * ancho
            exito = item["estado"] == "convergio"
            num_iter = item["iteraciones"] if exito else Max_iteraciones

            ax.bar(
                pos_x, num_iter, ancho,
                color=colores[j] if exito else "#f8d7da",
                edgecolor=colores[j] if exito else "#dc3545",
                linewidth=0.8,
                linestyle="-" if exito else "--",
                alpha=0.9 if exito else 0.6,
                label=nombre_metodo if i == 0 else None
            )

            texto = str(item["iteraciones"]) if exito else "Fallo"
            color_texto = "#222222" if exito else "#dc3545"
            
            ax.annotate(
                texto,
                xy=(pos_x, num_iter),
                xytext=(0, 2), textcoords="offset points",
                ha="center", va="bottom", fontsize=7.5, fontfamily="serif", 
                color=color_texto, fontweight="bold" if not exito else "normal"
            )

    ax.set_xticks(range(len(x0s)))
    ax.set_xticklabels([f"$x_0={v:g}$" for v in x0s], fontfamily="serif")
    ax.set_ylabel("N° de Iteraciones", fontsize=10, fontfamily="serif")
    ax.set_title("Sensibilidad a la estimación inicial $x_0$ — $f(x) = x^3 - x - 2$", fontsize=11, fontfamily="serif", pad=12)
    
    ax.grid(axis="y", color="#cccccc", linestyle="--", alpha=0.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(ncol=4, frameon=True, facecolor="white", edgecolor="none", loc="upper center", bbox_to_anchor=(0.5, -0.15))
    
    fig.tight_layout()
    fig.savefig(ruta_salida, dpi=200)
    plt.close(fig)


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    filas_resultados = []

    # 1. Pruebas de intervalo en Polinomica Simple
    fx_simple = MAPA_FUNCIONES["polinomica_simple"]
    filas_resultados.extend(ejecutar_experimentos_intervalo(fx_simple))

    # 2. Pruebas de x0 en Polinomica Simple
    x0_poli = [1.5, 1.0, 5.0, 50.0, 0.5, 0.58, 0.0, -1.0]
    filas_resultados.extend(ejecutar_experimentos_punto_inicial(fx_simple, x0_poli))

    # 3. Pruebas en Trigonometrica
    fx_trig = MAPA_FUNCIONES["trigonometrica"]
    filas_resultados.extend(ejecutar_experimentos_punto_inicial(fx_trig, [0.5, 1.0, 3.0, 10.0, 100.0]))

    # 4. Pruebas en Logaritmica
    fx_log = MAPA_FUNCIONES["logaritmica"]
    filas_resultados.extend(ejecutar_experimentos_punto_inicial(fx_log, [2.5, 0.01, 10.0, 50.0, -1.0]))

    # 5. Pruebas en Raiz Doble
    fx_doble = MAPA_FUNCIONES["polinomica_doble"]
    filas_resultados.extend(ejecutar_experimentos_punto_inicial(fx_doble, [1.2, 0.0, 1.9, 5.0]))

    # CSV
    csv_path = DATA_DIR / "sensibilidad.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["funcion_id", "metodo", "parametro", "estado", "iteraciones", "raiz"])
        writer.writeheader()
        writer.writerows(filas_resultados)

    print("Resultados guardados")

    graficar_sensibilidad_intervalo(filas_resultados, ASSETS_DIR / "sensibilidad_intervalo.png")
    graficar_sensibilidad_x0(filas_resultados, x0_poli, ASSETS_DIR / "sensibilidad_x0.png")
    print("Gráficos generados correctamente.")


if __name__ == "__main__":
    main()