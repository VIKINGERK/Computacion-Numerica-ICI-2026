# Informe – Prueba Parcial 3 «El pivote»

## 1. Identificación

- Asignatura: Computación Numérica (INF-321), Universidad Católica del Maule
- Integrantes: Nicolás Aburto (nbai) y Francisco Cartes (fjcv)
- Fecha: 20 de noviembre de 2026
- Repositorio: (https://github.com/VIKINGERK/Computacion-Numerica-ICI-2026.git). Rama evaluada: `main`. Ramas de trabajo: `nbai`, `fjcv` y `test`.

**Uso de IA:** usamos Claude para ayudarnos con el código, analizar resultados y organizar el `.md` del informe.

## 2. Planteamiento

Hay que resolver Ax = b con A de 12×12 densa (los 144 elementos son distintos de cero) y b con 20 dígitos. Los datos están en `datos/`.

Lo difícil del sistema:

- Las filas tienen tamaños muy distintos: desde 8·10⁻⁵ hasta 9.7x10⁵.
- El primer pivote es muy chico: a(1,1) = 1.34x10⁻⁸, y el elemento de abajo, a(2,1), es 1.19x10⁴.
- La fila 7 es casi combinación de las filas 3 y 5 (diferencia de orden 10⁻⁴), lo que hace el sistema más delicado.

## 3. Estrategia de eliminación

- Eliminación gaussiana en 11 pasos, que también actualiza b.
- El multiplicador m = a(i,k)/a(k,k) se calcula una vez por fila y se usa en toda la fila.
- Se trabaja desde la columna k+1; la columna k se deja en 0 directamente porque ya se sabe que da 0.
- Después se hace sustitución regresiva.
- Pivoteo parcial escalado: se calcula s_i = máximo |a_ij| de cada fila y en cada paso se elige la fila con mayor |a_ik|/s_i.
- Se guarda L y la permutación para reutilizarlos en el refinamiento. No se calcula la inversa.

## 4. Conteo de operaciones

Contamos como 1 operación cada suma, resta, multiplicación o división. El contador va sumando mientras el programa corre. La tabla por paso está en `resultados/conteo_flops.md`.

| Parte | Mult/Div | Sumas/Restas | Total |
| --- | ---: | ---: | ---: |
| Eliminación (11 pasos) | 638 | 572 | 1210 |
| Sustitución regresiva | 78 | 66 | 144 |
| **Total** | **716** | **638** | **1354** |

- La cota del enunciado es 1486 (con +/-10 %: de 1337 a 1635). Nuestro total, 1354, queda dentro (8.9 % menos) porque no calculamos los ceros de la columna k.
- Pivoteo parcial escalado, aparte de lo anterior: 198 comparaciones, 77 divisiones para escalar y 8 intercambios de filas.
- Cada pasada de refinamiento cuesta 276 operaciones.

## 5. Análisis de mantisa y pivoteo

Comparamos las dos corridas pedidas, más el pivoteo parcial simple como extra. El error se mide contra la solución exacta (con fracciones).

| Corrida | Mult. máximo | Crecimiento | Error relativo | Bits correctos | Bits perdidos |
| --- | ---: | ---: | ---: | ---: | ---: |
| (i) sin pivoteo | 2.753e13 | 2641 | 2.08e-10 | 32.2 | 20.8 |
| pivoteo parcial | 0.62 | 1.00 | 5.52e-13 | 40.7 | 12.3 |
| (ii) parcial escalado | 2.47e9 | 1.78 | 2.36e-13 | 41.9 | 11.1 |

Dígitos correctos por incógnita (x1 a x12):

- (i) sin pivoteo: 10, 9, 7, 8, 9, 7, 9, 8, 9, 9, 8, 9
- (ii) parcial escalado: 13, 12, 10, 11, 12, 10, 12, 11, 12, 12, 11, 12

Sin pivoteo ningún pivote se anula, así que se puede resolver y comparar. Pero a(1,1) es muy chico: los multiplicadores llegan a 2.75x10¹³ (unos 2^44.7) y los números crecen 2641 veces. Al restar números tan distintos en tamaño, la suma se hace con exponentes alineados y los bits bajos del número pequeño se pierden (hasta 18 bits en un solo paso). Con pivoteo esa pérdida baja a 6–7 bits. Por eso el resultado sin pivoteo pierde 20.8 bits y el escalado solo 11.1: unos 10 bits (≈ 3 dígitos) de diferencia.

El multiplicador máximo del escalado (2.5x10⁹) es grande solo porque las filas tienen tamaños muy distintos; el crecimiento real es 1.78.

## 6. Condicionamiento

| Magnitud | Valor |
| --- | ---: |
| κ₁ (estimador de Hager-Higham, sin calcular la inversa) | 4.47x10¹³ |
| κ∞ (estimador de Hager-Higham) | 5.37x10¹³ |
| κ₂ (numpy, solo control) | 3.08x10¹³ |
| κ₂ con las filas escaladas | 8.1x10³ |

Con κ₂ = 3.08x10¹³ la cota (κ x ε) es 6.8x10⁻³, que casi no garantiza dígitos. Pero medimos de 10 a 13 dígitos. La cota es pesimista porque el κ grande viene sobre todo de los tamaños distintos de las filas. Con las filas escaladas κ baja a 8.1x10³ y la cota queda en 1.8x10⁻¹², que sí coincide con lo medido (unos 12 dígitos). Con doble precisión se pueden defender entre 10 y 13 dígitos según la incógnita.

## 7. Resultados

Con pivoteo parcial escalado y doble precisión (valor con los dígitos que se pueden defender; se cuentan como dígitos correctos los de error relativo menor a 10⁻ᵈ):

| i | x | dígitos |
| ---: | ---: | ---: |
| 1 | 7.384915626999e-1 | 13 |
| 2 | -1.20593741680e+0 | 12 |
| 3 | 4.387195200e-3 | 10 |
| 4 | -9.1726453800e-2 | 11 |
| 5 | 2.84610937250e+0 | 12 |
| 6 | -6.281540899e-3 | 10 |
| 7 | 1.47382059160e+0 | 12 |
| 8 | -3.8492716400e-2 | 11 |
| 9 | 9.15264803700e-1 | 12 |
| 10 | -2.60713948520e+0 | 12 |
| 11 | 5.1873629400e-2 | 11 |
| 12 | -1.08493716250e+0 | 12 |

Después del refinamiento iterativo la solución queda con 30 dígitos en `resultados/solucion.csv`; a 10 dígitos es x₁ = 0.7384915627, x₂ = −1.205937417, x₃ = 0.0043871952, etc.

## 8. Verificación

El residuo r = b − Ax se calculó con fracciones (sin redondear) y datos completos.

| Solución | Norma infinito de r |
| --- | ---: |
| Sin pivoteo | 1.77x10⁻⁷ |
| Pivoteo parcial escalado | 2.29x10⁻¹⁰ |
| Después de refinar | 1.38x10⁻⁴⁸ |

Refinamiento iterativo (usando L y U de la corrida (ii), sin repetir la eliminación):

| Pasada | Error relativo |
| ---: | ---: |
| 0 | 2.36x10⁻¹³ |
| 1 | 6.17x10⁻²⁶ |
| 2 | 1.61x10⁻³⁸ |
| 3 | 4.22x10⁻⁵¹ |

Cada pasada gana unos 12 dígitos, así que el refinamiento mejora mucho el resultado. Como control, `numpy.linalg.solve` da error 5.2x10⁻¹³, parecido al nuestro (2.4x10⁻¹³). Numpy se usó solo para comparar.

## 9. Conclusiones

- El costo de la eliminación es 1354 operaciones. Agregar pivoteo escalado cuesta unas 280 operaciones más (comparaciones, divisiones e intercambios) y a cambio el error baja unas 880 veces respecto de no pivotear.
- El pivoteo escalado mejora algo al pivoteo parcial simple (error 2.4x10⁻¹³ contra 5.5x10⁻¹³).
- El refinamiento cuesta 276 operaciones por pasada y con 3 pasadas se llega a la precisión máxima.
- Con n = 1000 la eliminación costaría del orden de 6.7x10⁸ operaciones y una pasada de refinamiento solo unos 2x10⁶, así que el refinamiento seguiría siendo barato. El residuo con fracciones ya no serviría (los números crecen demasiado) y habría que usar mayor precisión solo para el residuo.

## 10. Reproducibilidad

- Python 3.12.3 y numpy 2.5.4 (`requirements.txt`).
- Ejecutar desde la carpeta principal del repositorio: `python src/main.py`
- Genera en `resultados/`: `solucion.csv`, `traza_eliminacion.txt`, `conteo_flops.md` y `residuo.txt`.