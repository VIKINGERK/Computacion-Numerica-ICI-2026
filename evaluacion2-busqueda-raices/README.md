# Evaluación 2 — La raíz que se esconde

Comparación de seis métodos de búsqueda de raíces (bisección, falsa posición, punto fijo,
secante, Newton-Raphson y Newton-Raphson mejorado) sobre seis funciones de distinta naturaleza,
con tolerancia `1e-6` y tope de 100 iteraciones.

**Integrantes:** _(Nicolás Aburto I. & Francisco Cartes V.)_ · Universidad Católica del Maule

## Estructura

```
evaluacion2-busqueda-raices/
├── README.md
├── requirements.txt          numpy, matplotlib
├── informe.md                respuestas a las preguntas de convergencia y conclusión
└── src/
    ├── assets/               gráficos PNG generados
    ├── data/                 CSV generados
    └── scripts/              scripts de Python
```

## Entorno (venv)

Requiere Python 3.9 o superior.

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Cómo ejecutar

Siempre desde la raíz del repositorio:

```bash
python src/scripts/generar_todo.py     # CSV + gráficos principales + tabla en consola
python src/scripts/sensibilidad.py     # estudio de intervalo inicial y estimación inicial
```

Los scripts son deterministas (no usan azar): al ejecutarlos se obtienen exactamente los
mismos CSV y gráficos que aparecen en `informe.md`.

## Qué hace cada script

| Script | Qué hace |
|---|---|
| `src/scripts/metodos.py` | Implementa con numpy los seis métodos (`biseccion`, `falsa_posicion`, `punto_fijo`, `secante`, `newton`, `newton_mejorado`) y `estimar_orden`, que estima el orden de convergencia empírico a partir de los errores. |
| `src/scripts/funciones.py` | Define las seis funciones de prueba con sus derivadas, la función `g(x)` de punto fijo y el ambiente controlado (intervalo `[a, b]`, `x0`, `x1`, tolerancia y tope). |
| `src/scripts/generar_todo.py` | Corre los seis métodos en cada función, demuestra la raíz (cambio de signo o tangencia) y genera todos los CSV de `src/data/` y los gráficos de función, convergencia y resumen. |
| `src/scripts/sensibilidad.py` | Repite los métodos variando el intervalo inicial (cerrados) y la estimación inicial (abiertos) y genera `sensibilidad.csv` y sus gráficos. |

## Archivos generados

**`src/data/`**
- `<funcion>.csv`: columnas `(x, f(x))`, 400 puntos por función.
- `ambiente_controlado.csv`: intervalo, estimaciones iniciales, `f(a)`, `f(b)`, `f(a)·f(b)`, tolerancia, tope y demostración de la raíz.
- `historial_convergencia.csv`: una fila por iteración de cada método (x, f(x), paso, error real).
- `resumen_convergencia.csv`: estado, iteraciones, raíz, error real y orden estimado por método y función.
- `sensibilidad.csv`: resultados al variar intervalo y estimación inicial.

**`src/assets/`**
- `funcion_<funcion>.png`: cada función con su raíz marcada (en la raíz doble, la tangencia al eje).
- `convergencia_<funcion>.png`: |error| vs iteración en escala log, comparando métodos.
- `resumen_iteraciones.png`: iteraciones por método y función.
- `sensibilidad_intervalo.png`, `sensibilidad_x0.png`: efecto del intervalo y de `x0`.

## Criterios usados

- Parada: `|f(x)| < 1e-6` **o** `|x − x_anterior| < 1e-6` (en bisección, la semiamplitud del intervalo).
- Error: `|x − raíz|`, con raíz de referencia obtenida por bisección a precisión de máquina (en la raíz doble, la raíz exacta 2).
- Tope: 100 iteraciones.
