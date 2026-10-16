import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from funciones import FUNCIONES, Tolerancia, Max_iteraciones, raiz_referencia
import metodos as m

SRC = Path(__file__).resolve().parents[1]
DATA = SRC / "data"
ASSETS = SRC / "assets"
DATA.mkdir(exist_ok=True)
ASSETS.mkdir(exist_ok=True)

ORDEN_METODOS = ["Bisección", "Falsa posición", "Punto fijo", "Secante",
                 "Newton-Raphson", "Newton mejorado"]
COLORES = dict(zip(ORDEN_METODOS,
                   ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]))
MARCAS = dict(zip(ORDEN_METODOS, ["o", "s", "^", "D", "v", "P"]))


def correr_metodos(fun, tol=Tolerancia, max_it=Max_iteraciones):
    f, df, d2f, g = fun["f"], fun["df"], fun["d2f"], fun["g"]
    return {
        "Bisección": m.biseccion(f, fun["a"], fun["b"], tol, max_it),
        "Falsa posición": m.falsa_posicion(f, fun["a"], fun["b"], tol, max_it),
        "Punto fijo": m.punto_fijo(f, g, fun["x0"], tol, max_it),
        "Secante": m.secante(f, fun["x0_secante"], fun["x1"], tol, max_it),
        "Newton-Raphson": m.newton(f, df, fun["x0"], tol, max_it),
        "Newton mejorado": m.newton_mejorado(f, df, d2f, fun["x0"], tol, max_it),
    }


def main():
    resumen, historial, ambiente = [], [], []
    resultados = {}

    for fun in FUNCIONES:
        f = fun["f"]
        raiz = raiz_referencia(fun)
        fun["raiz"] = raiz

        margen = 0.25 * (fun["b"] - fun["a"])
        xs = np.linspace(fun["a"] - (0 if fun["a"] == 0.0 else 0) , fun["b"], 400)
        if fun["id"] == "polinomica_doble":
            xs = np.linspace(1.0, 3.0, 400)
        with np.errstate(all="ignore"):
            ys = f(xs)
        with open(DATA / f"{fun['id']}.csv", "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["x", "f(x)"])
            w.writerows(zip(xs, ys))

        fa, fb = f(fun["a"]), f(fun["b"])
        demo = ("cambio de signo (Bolzano): f(a)·f(b) < 0" if fa * fb < 0
                else "tangencia al eje: f(2)=0 y f'(2)=0, f(x) ≥ 0 en todo R")
        ambiente.append([fun["categoria"], fun["texto"], fun["a"], fun["b"], fa, fb,
                         fa * fb, fun["x0"], fun["x0_secante"], fun["x1"],
                         Tolerancia, Max_iteraciones, demo])

        res = correr_metodos(fun)
        resultados[fun["id"]] = res
        for nombre in ORDEN_METODOS:
            r = res[nombre]
            h = r["historial"]
            errores = [abs(x - raiz) for (_, x, _, _) in h]
            for (k, x, fx, paso), e in zip(h, errores):
                historial.append([fun["id"], nombre, k, x, fx, paso, e])
            if h:
                k, x, fx, _ = h[-1]
                serie = [p for (_, _, _, p) in h] if nombre == "Bisección" else errores
                resumen.append([fun["id"], fun["texto"], nombre, r["estado"], len(h), x,
                                abs(fx), abs(x - raiz), m.estimar_orden(serie), r["nota"]])
            else:
                resumen.append([fun["id"], fun["texto"], nombre, r["estado"], 0,
                                "", "", "", "", r["nota"]])

    with open(DATA / "ambiente_controlado.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["categoria", "funcion", "a", "b", "f(a)", "f(b)", "f(a)*f(b)",
                    "x0 (punto fijo/Newton)", "x0 (secante)", "x1 (secante)",
                    "tolerancia", "tope_iteraciones", "demostracion_de_la_raiz"])
        w.writerows(ambiente)
    with open(DATA / "historial_convergencia.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["funcion", "metodo", "iteracion", "x", "f(x)", "paso", "error_real"])
        w.writerows(historial)
    with open(DATA / "resumen_convergencia.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["funcion_id", "funcion", "metodo", "estado", "iteraciones", "raiz",
                    "|f(raiz)|", "error_real", "orden_estimado", "nota"])
        w.writerows(resumen)

    for fun in FUNCIONES:
        graficar_funcion(fun)
        graficar_convergencia(fun, resultados[fun["id"]])
    graficar_resumen(resultados)
    print("Listo. Archivos en", DATA, "y", ASSETS)
    imprimir_resumen(resumen)


def graficar_funcion(fun):
    f, raiz = fun["f"], fun["raiz"]
    if fun["id"] == "polinomica_doble":
        xs = np.linspace(1.0, 3.0, 400)
    else:
        xs = np.linspace(fun["a"], fun["b"], 400)
    ys = f(xs)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(xs, ys, color="#1f77b4", lw=2, label=fun["texto"])
    ax.axhline(0, color="black", lw=1)
    ax.plot(raiz, f(raiz), "r*", ms=16, zorder=5, label=f"raíz ≈ {raiz:.6f}")
    if fun["tipo"] == "doble":
        ax.annotate("tangencia al eje x\n(no hay cambio de signo)", xy=(raiz, 0),
                    xytext=(2.25, 0.8), arrowprops=dict(arrowstyle="->"))
    else:
        ax.axvspan(fun["a"], fun["b"], color="gold", alpha=0.15,
                   label=f"intervalo [{fun['a']}, {fun['b']}]")
        ax.plot([fun["a"], fun["b"]], [f(fun["a"]), f(fun["b"])], "ko", label="f(a), f(b)")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(f"{fun['categoria']}: {fun['texto']}")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(ASSETS / f"funcion_{fun['id']}.png", dpi=130)
    plt.close(fig)


def graficar_convergencia(fun, res):
    raiz = fun["raiz"]
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    hay = False
    for nombre in ORDEN_METODOS:
        h = res[nombre]["historial"]
        if not h:
            continue
        ks = [k for (k, _, _, _) in h]
        es = [max(abs(x - raiz), 1e-17) for (_, x, _, _) in h]
        ax.semilogy(ks, es, marker=MARCAS[nombre], ms=4, color=COLORES[nombre], label=nombre)
        hay = True
    ax.axhline(Tolerancia, color="gray", ls="--", lw=1, label="tol = 1e-6")
    ax.set_xlabel("iteración")
    ax.set_ylabel("|error| = |x - raíz|  (escala log)")
    ax.set_title(f"Convergencia - {fun['texto']}")
    ax.grid(alpha=0.3, which="both")
    na = [n for n in ORDEN_METODOS if res[n]["estado"] == "no_aplica"]
    if na:
        ax.text(0.98, 0.97, "No aplican (sin cambio de signo):\n" + ", ".join(na),
                transform=ax.transAxes, ha="right", va="top", fontsize=8,
                bbox=dict(boxstyle="round", fc="white", ec="gray"))
    if hay:
        ax.legend(fontsize=8, loc="center right")
    fig.tight_layout()
    fig.savefig(ASSETS / f"convergencia_{fun['id']}.png", dpi=130)
    plt.close(fig)


def graficar_resumen(resultados):
    ids = [f["id"] for f in FUNCIONES]
    etiquetas = [f["categoria"].replace(" (", "\n(") for f in FUNCIONES]
    n = len(ORDEN_METODOS)
    ancho = 0.8 / n
    fig, ax = plt.subplots(figsize=(12, 5.5))
    for j, nombre in enumerate(ORDEN_METODOS):
        for i, fid in enumerate(ids):
            r = resultados[fid][nombre]
            x = i + (j - (n - 1) / 2) * ancho
            if r["estado"] == "convergio":
                ax.bar(x, len(r["historial"]), ancho, color=COLORES[nombre],
                       label=nombre if i == 0 else None)
                ax.text(x, len(r["historial"]) + 1, str(len(r["historial"])), ha="center", fontsize=7)
            elif r["estado"] == "no_aplica":
                ax.text(x, 1, "N/A", ha="center", rotation=90, fontsize=7, color=COLORES[nombre])
            else:
                ax.bar(x, Max_iteraciones, ancho, color=COLORES[nombre], hatch="////", alpha=0.5,
                       edgecolor="red", label=nombre if i == 0 else None)
                ax.text(x, Max_iteraciones + 1, "✗", ha="center", fontsize=9, color="red")
    ax.set_xticks(range(len(ids)))
    ax.set_xticklabels(etiquetas, fontsize=8)
    ax.set_ylabel("iteraciones (tol = 1e-6)")
    ax.set_title("Iteraciones por método y función  (N/A = no aplica, ✗ = no convergió / falló)")
    ax.grid(axis="y", alpha=0.3)
    handles, labels = ax.get_legend_handles_labels()
    vistos = {}
    for h, l in zip(handles, labels):
        vistos.setdefault(l, h)
    ax.legend(vistos.values(), vistos.keys(), fontsize=8, ncol=3)
    fig.tight_layout()
    fig.savefig(ASSETS / "resumen_iteraciones.png", dpi=130)
    plt.close(fig)


def imprimir_resumen(resumen):
    print(f"{'función':<20}{'método':<18}{'estado':<12}{'it':>4}  {'raíz':>12}  {'error real':>11}  {'orden':>6}")
    for r in resumen:
        fid, _, met, est, it, raiz, _, err, p, nota = r
        raiz_s = f"{raiz:.8f}" if raiz != "" else "-"
        err_s = f"{err:.2e}" if err != "" else "-"
        p_s = f"{p:.2f}" if p != "" and not np.isnan(p) else "-"
        print(f"{fid:<20}{met:<18}{est:<12}{it:>4}  {raiz_s:>12}  {err_s:>11}  {p_s:>6}  {nota}")


if __name__ == "__main__":
    main()