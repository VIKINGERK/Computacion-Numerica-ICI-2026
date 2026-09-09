import os
import matplotlib.pyplot as plt
import numpy as np
from cargar_datos import cargar_datos_dolar
from errores import redondear


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    graficos_dir = os.path.join(base_dir, "graficos")
    os.makedirs(graficos_dir, exist_ok=True)

    # B1
    val = 1000.76
    val_3c = redondear(val, 3)
    ea = abs(val - val_3c)
    er = (ea / val) * 100
    print(f"B1: 1000.76 -> {val_3c} (Ea={ea:.2f}, Er={er:.4f}%)")

    # B2: ida y vuelta en float32
    precios, etiquetas, _, _ = cargar_datos_dolar()
    monto = 1_000_000.0
    derivas = []
    for p in precios:
        p32 = np.float32(p)
        m32 = np.float32(monto)
        usd = m32 / p32
        final = usd * p32
        derivas.append(final - monto)

    plt.figure(figsize=(12, 5))
    plt.plot(etiquetas, derivas, marker="s", linestyle="-")
    plt.axhline(0, color="black", linestyle="--", linewidth=0.8)
    plt.xticks(rotation=90, fontsize=8)
    plt.title("Deriva ida y vuelta en float32")
    plt.ylabel("Monto final - Monto inicial (CLP)")
    plt.tight_layout()
    plt.savefig(os.path.join(graficos_dir, "5_deriva_ida_y_vuelta.png"), dpi=300)
    plt.close()

    # B4
    v1, v2 = 874.67, 875.66
    diff32 = np.float32(v1) - np.float32(v2)
    diff64 = np.float64(v1) - np.float64(v2)
    print(f"B4: resta float64 = {diff64:.8f}, float32 = {diff32:.8f}, "
          f"diferencia = {abs(diff64 - diff32):.8f}")


if __name__ == "__main__":
    main()