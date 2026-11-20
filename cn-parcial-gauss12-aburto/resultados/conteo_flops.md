# Tabla de operaciones por paso

Conteo de operaciones elementales por paso (1 flop = suma, resta, multiplicación o división).

| Paso k | Divisiones (multiplicadores) | Multiplicaciones | Mult/Div | Restas | Sumas | Sumas/Restas | Flops del paso |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 11 | 132 | 143 | 132 | 0 | 132 | 275 |
| 2 | 10 | 110 | 120 | 110 | 0 | 110 | 230 |
| 3 | 9 | 90 | 99 | 90 | 0 | 90 | 189 |
| 4 | 8 | 72 | 80 | 72 | 0 | 72 | 152 |
| 5 | 7 | 56 | 63 | 56 | 0 | 56 | 119 |
| 6 | 6 | 42 | 48 | 42 | 0 | 42 | 90 |
| 7 | 5 | 30 | 35 | 30 | 0 | 30 | 65 |
| 8 | 4 | 20 | 24 | 20 | 0 | 20 | 44 |
| 9 | 3 | 12 | 15 | 12 | 0 | 12 | 27 |
| 10 | 2 | 6 | 8 | 6 | 0 | 6 | 14 |
| 11 | 1 | 2 | 3 | 2 | 0 | 2 | 5 |
| *Eliminación (1 a 11)* | *66* | *572* | *638* | *572* | *0* | *572* | *1210* |
| Sustitución regresiva | 12 | 66 | 78 | 66 | 0 | 66 | 144 |
| *TOTAL* | *78* | *638* | *716* | *638* | *0* | *638* | *1354* |

## Sobrecosto de estabilidad (pivoteo parcial escalado)

| Paso k | Comparaciones | Divisiones de escalado | Intercambios de filas |
| --- | --- | --- | --- |
| Escalas de fila (previo) | 132 | 0 | 0 |
| 1 | 11 | 12 | 1 |
| 2 | 10 | 11 | 0 |
| 3 | 9 | 10 | 1 |
| 4 | 8 | 9 | 1 |
| 5 | 7 | 8 | 1 |
| 6 | 6 | 7 | 1 |
| 7 | 5 | 6 | 1 |
| 8 | 4 | 5 | 1 |
| 9 | 3 | 4 | 1 |
| 10 | 2 | 3 | 0 |
| 11 | 1 | 2 | 0 |
| *TOTAL* | *198* | *77* | *8* |
