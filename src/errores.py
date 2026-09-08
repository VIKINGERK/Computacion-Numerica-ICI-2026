import os
import numpy as np
from cargar_datos import cargar_datos_dolar


def error_absoluto(real, aprox):
    return np.abs(real - aprox)


def error_relativo(ea, real):
    return (ea / np.abs(real)) * 100.0


def redondear(valores, cifras):
    """Redondea a N cifras significativas (base 10)."""
    valores = np.asarray(valores, dtype=float)
    resultado = np.zeros_like(valores)
    no_cero = valores != 0
    exp = np.floor(np.log10(np.abs(valores[no_cero])))
    factor = 10 ** exp
    resultado[no_cero] = np.round(valores[no_cero] / factor, cifras - 1) * factor
    return resultado if resultado.ndim > 0 else float(resultado)


def propagar_mult(e1, e2):
    # multiplicacion / division -> se suman los errores relativos
    return e1 + e2


def propagar_resta(e1, e2):
    # suma / resta -> se suman los errores absolutos
    return e1 + e2


def calcular_pares(precios, etiquetas, monto=1_000_000):
    aprox = redondear(precios, 3)
    er_precio = error_absoluto(precios, aprox) / precios

    compra = aprox[:, None]
    venta = aprox[None, :]
    er_compra = er_precio[:, None]
    er_venta = er_precio[None, :]

    usd = monto / compra
    pesos = usd * venta
    ganancia = pesos - monto

    er_total = propagar_mult(er_compra, er_venta)
    error_pesos = pesos * er_total
    error_ganancia = propagar_resta(error_pesos, 0)
    error_ganancia_pct = error_relativo(error_ganancia, ganancia)

    i, j = np.triu_indices(len(precios), k=1)

    return np.rec.fromarrays(
        [etiquetas[i], precios[i], etiquetas[j], precios[j],
         usd.flatten()[i], pesos[i, j], ganancia[i, j],
         error_ganancia[i, j], error_ganancia_pct[i, j]],
        names="mes_compra,p_compra,mes_venta,p_venta,usd,pesos_final,ganancia,error_ganancia,error_ganancia_pct"
    )


if __name__ == "__main__":
    precios, etiquetas, _, _ = cargar_datos_dolar()

    # A1
    aprox2 = redondear(precios, 2)
    er2 = error_relativo(error_absoluto(precios, aprox2), precios)
    peor = np.argmax(er2)
    print(f"A1: mayor error relativo en {etiquetas[peor]} -> Er = {er2[peor]:.4f}%")

    # A2 (ejemplo: compra Ene-2022, venta Jul-2022)
    pares = calcular_pares(precios, etiquetas)
    ejemplo = pares[(pares.mes_compra == "Ene-2022") & (pares.mes_venta == "Jul-2022")][0]
    print(f"A2: comprando en {ejemplo.mes_compra} y vendiendo en {ejemplo.mes_venta} -> "
          f"ganancia = ${ejemplo.ganancia:,.2f} +/- ${ejemplo.error_ganancia:,.2f} CLP")

    carpeta = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta = os.path.join(carpeta, "data", "evaluacion_errores_parejas.csv")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    np.savetxt(
        ruta, pares, delimiter=",", header=",".join(pares.dtype.names),
        comments="", fmt=["%s", "%.2f", "%s", "%.2f", "%.2f", "%.2f", "%.2f", "%.2f", "%.2f"]
    )
    print(f"CSV guardado en {ruta}")