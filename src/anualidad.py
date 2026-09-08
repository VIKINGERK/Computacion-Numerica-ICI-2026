import os
import matplotlib.pyplot as plt
import numpy as np
from cargar_datos import cargar_datos_dolar
from errores import redondear, error_absoluto, error_relativo


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    graficos_dir = os.path.join(base_dir, "graficos")
    os.makedirs(graficos_dir, exist_ok=True)

    precios, etiquetas, anios, _ = cargar_datos_dolar()

    # A3: cancelacion dic-2022 vs dic-2023
    p22, p23 = 875.66, 874.67
    p22_3c, p23_3c = redondear(p22, 3), redondear(p23, 3)
    ea22, ea23 = abs(p22 - p22_3c), abs(p23 - p23_3c)
    delta = p23_3c - p22_3c
    ea_delta = ea22 + ea23
    er_delta = (ea_delta / abs(delta)) * 100
    print(f"A3: DeltaP = {delta:.2f} +/- {ea_delta:.2f} CLP (Er = {er_delta:.2f}%)")

    # A4: variacion enero-diciembre por año
    resultados_anio = []
    for anio in np.unique(anios):
        precios_anio = precios[anios == anio]
        p_ene, p_dic = precios_anio[0], precios_anio[-1]
        p_ene_3c, p_dic_3c = redondear(p_ene, 3), redondear(p_dic, 3)
        ea = abs(p_ene - p_ene_3c) + abs(p_dic - p_dic_3c)
        d = p_dic_3c - p_ene_3c
        er = (ea / abs(d)) * 100 if d != 0 else np.nan
        resultados_anio.append((anio, d, ea, er))

    resultados_anio.sort(key=lambda x: x[3])
    mejor, peor = resultados_anio[0], resultados_anio[-1]
    print(f"A4: año más confiable {mejor[0]} (Er={mejor[3]:.2f}%), "
          f"menos confiable {peor[0]} (Er={peor[3]:.2f}%)")

    tabla_anual = np.rec.fromrecords(
        resultados_anio, names="anio,delta_p,error_absoluto,error_relativo_pct"
    )
    ruta_anual = os.path.join(base_dir, "data", "evaluacion_errores_anual.csv")
    np.savetxt(
        ruta_anual, tabla_anual, delimiter=",", header=",".join(tabla_anual.dtype.names),
        comments="", fmt=["%d", "%.2f", "%.2f", "%.2f"]
    )

    # A5: minimo vs maximo global
    i_min, i_max = np.argmin(precios), np.argmax(precios)
    p_min, p_max = precios[i_min], precios[i_max]
    p_min_2c, p_max_2c = redondear(p_min, 2), redondear(p_max, 2)
    ea_min, ea_max = abs(p_min - p_min_2c), abs(p_max - p_max_2c)

    rentabilidad = ((p_max_2c - p_min_2c) / p_min_2c) * 100
    er_rent = ((ea_min / p_min_2c) + (ea_max / p_max_2c)) * 100
    ea_rent = abs(rentabilidad) * (er_rent / 100)
    print(f"A5: comprar en {etiquetas[i_min]}, vender en {etiquetas[i_max]} -> "
          f"rentabilidad = {rentabilidad:.2f}% +/- {ea_rent:.2f}% (Er={er_rent:.2f}%)")

    # --- graficos ---
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    plt.figure(figsize=(12, 5))
    plt.plot(etiquetas, precios, marker="o", linewidth=1.2)
    plt.xticks(rotation=90, fontsize=8)
    plt.title("Dólar observado mensual 2022-2025")
    plt.ylabel("CLP")
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_dir, "1_serie_mensual.png"), dpi=300)
    plt.close()

    delta_mensual = np.diff(precios)
    plt.figure(figsize=(12, 5))
    plt.bar(etiquetas[1:], delta_mensual, color=np.where(delta_mensual >= 0, "green", "red"))
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
    plt.xticks(rotation=90, fontsize=8)
    plt.title("Variación mes a mes")
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_dir, "2_variacion_mes_a_mes.png"), dpi=300)
    plt.close()

    aprox2 = redondear(precios, 2)
    er2 = error_relativo(error_absoluto(precios, aprox2), precios)
    plt.figure(figsize=(12, 5))
    plt.bar(etiquetas, er2, color="orange")
    plt.xticks(rotation=90, fontsize=8)
    plt.title("Error relativo al redondear a 2 cifras significativas")
    plt.ylabel("%")
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_dir, "3_error_representacion.png"), dpi=300)
    plt.close()

    sub = precios[i_min:]
    etiquetas_sub = etiquetas[i_min:]
    aprox_sub = redondear(sub, 2)
    ea_sub = abs(sub - aprox_sub)
    rent_sub = ((aprox_sub - p_min_2c) / p_min_2c) * 100
    er_sub = ((ea_min / p_min_2c) + (ea_sub / aprox_sub)) * 100
    err_rent_sub = abs(rent_sub) * (er_sub / 100)

    plt.figure(figsize=(10, 5))
    plt.errorbar(etiquetas_sub, rent_sub, yerr=err_rent_sub, fmt="-o", ecolor="red", capsize=3)
    plt.xticks(rotation=90, fontsize=8)
    plt.title("Rentabilidad comprando en el mínimo")
    plt.ylabel("%")
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_dir, "4_rentabilidad_desde_minimo.png"), dpi=300)
    plt.close()

    print("Gráficos guardados en /graficos")


if __name__ == "__main__":
    main()