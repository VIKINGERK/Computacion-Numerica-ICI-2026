# La ganancia que se evapora

Análisis de error y propagación de error usando el dólar observado del SII (2022-2025) lab Inv. de operacionees.

## Estructura

- 'src/cargar_datos.py' — carga el CSV con numpy
- 'src/errores.py' — error absoluto, relativo y propagado (preguntas A1-A2)
- 'src/anualidad.py' — cancelación, variación anual y rentabilidad (A3-A5) + gráficos
- 'src/punto_flotante.py' — float32/float64, ida y vuelta, cancelación (B1-B4)

## Cómo correrlo

bash
pip install -r requirements.txt
python src/cargar_datos.py
python src/errores.py
python src/anualidad.py
python src/punto_flotante.py


Los gráficos quedan en '/graficos' y las tablas de error en '/data'.

## Resultados

- A1: mes con mayor error relativo fue Abril 2022 (0.5987%)
- A2: ejemplo compra-venta: ganancia ($160,583.94 +/- $423.50) comprando en enero 2022 y vendiendo en julio 2022
- A3: cancelación dic-2022 vs dic-2023: DeltaP = -1.00 +/- 0.67 (Err = 67%)
- A4: año más / menos confiable: 2024/2023
- A5: rentabilidad mínimo-máximo: 25% +/- 0,07%
- B1: error al redondear 1000.76 a 3 cifras: 0.0759%
- B4: diferencia float32 vs float64: 0.00000977

Ver 'INFORME.md' para el análisis y conclusión.