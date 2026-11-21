# cn-parcial-gauss12 — Eliminación gaussiana 12×12 con pivoteo y control de mantisa

Resuelve un sistema lineal denso de 12 incógnitas con eliminación gaussiana propia (con y sin pivoteo, contador de flops, residuo exacto y refinamiento iterativo).

## Autoría y asignatura

Nicolás Aburto (`nbai`) y Francisco Cartes (`fjcv`) · Computación Numérica (INF-321) · Ingeniería Civil Informática, Universidad Católica del Maule · Prueba Parcial 3 «El pivote» · Talca, noviembre de 2026.

## Requisitos

- Python 3.10 o superior (probado con 3.12.3).
- Instalar la única dependencia (numpy, usada solo como control): `pip install -r requirements.txt`

## Ejecución

```
python src/main.py
```

Ejecútalo desde la raíz del repositorio. Sin intervención manual, genera en `resultados/`: `solucion.csv`, `traza_eliminacion.txt`, `conteo_flops.md` y `residuo.txt`.

## Estructura de carpetas

```
datos/       A (12x12) y b exactos, sin truncar
src/         gauss.py (eliminación), conteo.py (costo), verificacion.py (residuo, refinamiento, κ), main.py (entrada única)
resultados/  salidas generadas por main.py
informe.md   informe técnico y análisis de error
```

## Resultado resumido

| i | x (10 dígitos) |
| ---: | ---: |
| 1 | 0.7384915627 |
| 2 | -1.205937417 |
| 3 | 0.004387195200 |
| 4 | -0.09172645380 |
| 5 | 2.846109372 |
| 6 | -0.006281540900 |
| 7 | 1.473820592 |
| 8 | -0.03849271640 |
| 9 | 0.9152648037 |
| 10 | -2.607139485 |
| 11 | 0.05187362940 |
| 12 | -1.084937163 |

- Flops del algoritmo (eliminación + sustitución): **1354**
- ‖r‖∞ de la solución en doble precisión (pivoteo escalado): **2.29e-10**; tras el refinamiento: **1.38e-48** (residuo en precisión extendida)

## Informe

El análisis completo está en [informe.md](informe.md).

## Licencia / nota de uso

Trabajo académico de uso docente (UCM, INF-321); no se concede licencia de redistribución.
