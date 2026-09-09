import os
import numpy as np


def cargar_datos_dolar(ruta_csv=None):
    if ruta_csv is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_csv = os.path.join(base_dir, "data", "dolar_observado_sii_2022_2025.csv")

    matriz = np.genfromtxt(ruta_csv, delimiter=",", skip_header=1, usecols=(1, 2, 3, 4))

    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    anios_lista = [2022, 2023, 2024, 2025]

    precios = matriz.T.flatten()
    etiquetas = []
    anios = []
    for anio in anios_lista:
        for mes in meses:
            etiquetas.append(f"{mes[:3]}-{anio}")
            anios.append(anio)

    return precios, np.array(etiquetas), np.array(anios), meses


if __name__ == "__main__":
    precios, etiquetas, anios, meses = cargar_datos_dolar()
    print(f"{len(precios)} meses cargados")
    print(f"Min: {precios.min():.2f} ({etiquetas[np.argmin(precios)]})")
    print(f"Max: {precios.max():.2f} ({etiquetas[np.argmax(precios)]})")