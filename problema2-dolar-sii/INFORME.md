@Nicolás Aburto Inzulza.
@Francisco Cartes Vallejos.

# Informe — La ganancia que se evapora

## Resumen
Se analizó el dólar observado del SII (2022-2025) para ver cuándo convenía comprar y vender, incorporando el error de representación por redondeo a cifras significativas y su propagación en las operaciones.

## Resultados

### Errores de representación y propagación (A1-A2)
**A1: ¿Qué mes quedó con el mayor error relativo al redondear?**

Se redondearon los precios del dólar a 2 cifras significativas y se calculó el error absoluto y relativo de cada mes. El mayor error relativo  se obtuvo en abril de 2022, donde el precio real de $815,12 se aproximó a $820, generando un error relativo de 0,5987%.

Es decir, abril de 2022 fue el mes en que el redondeo produjo la mayor diferencia proporcional respecto al precio real.

**A2: Entrega la ganancia como valor +/- error y su error porcentual.**

Se tomó como ejemplo una compra en enero de 2022 y una venta en julio de 2022, usando un monto inicial de $1.000.000 CLP.

El precio de compra fue de $822.05, mientras que el de venta fue de $953.71. 

Con estos valores se calculó la cantidad de dólares comprados, los pesos obtenidos al venderlos y finalmente la ganancia.

Se calcularon los errores de los precios y se propagaron los errores relativos en la división y multiplicación, para obtener el error de la  ganancia y se utilizó la suma de los errores absolutos.

El resultado fue una ganancia aproximada de $160.583,94 CLP, con un error propagado de +/- $423,50 CLP y un error relativo de aproximadamente 0,2637%.

Por lo tanto:

Ganancia = $160.583,94 +/- $423,50 CLP

### Cancelación y confiabilidad anual (A3-A5)
**A3: ¿puedes afirmar con seguridad si el dólar subió o bajó entre esos dos diciembres?**

Calculando la diferencia del precio del dólar de diciembre de 2022 y diciembre de 2023 con 3 cifras significativas.

- Variación: -$1,00CLP
- Error absoluto: +/- $0,67CLP
- Error relativo: 67,00%

Entonces:

Delta_P = -$1,00 +/- $0,67 CLP

Aunque el resultado muestra que el dólar bajó $1,00, el error es grande en comparación a la variación obtenida. Por esto no podemos estar seguros de que haya  bajado, ya que la diferencia está en el margen de error.

Esto muestra el efecto de cancelación: al restar dos valores muy parecidos, una pequeña diferencia entre ellos puede terminar teniendo un error relativo bastante grande.


**A4: ¿Qué tienen en común los años poco confiables?**

Calculamos la variación entre enero y diciembre de cada año, tomando también el error al restar los precios.

Al comparar los resultados, 2024 fue el año más confiable, con un error relativo de 0,42 %, mientras que 2023 fue el menos confiable, con un error relativo de 1,37%.

Los años menos confiables tienen en común que el precio de diciembre es muy parecido al de enero. Como la diferencia entre ambos valores es pequeña, el error tiene un  mayor peso sobre el resultado final. Esto produce un error relativo más alto debido al  efecto de cancelación.


**A5: ¿La conclusión sobrevive al error (la diferencia es mucho mayor que la incertidumbre) o queda en duda?**

La conclusión se mantiene considerando el error de representación. La diferencia entre el precio de compra y venta hace que el error propagado tenga poca influencia en la rentabilidad final.

La mejor estrategia es comprar en febrero de 2023, cuando el dólar tenía un valor de $798.26 CLP, y vender en enero de 2025, cuando alcanzó $1.000,76 CLP.

Con estos valores obtuvimos una rentabilidad de 25,00% +/- 0,07% que corresponde a un error relativo de 0,29%. Esto significa que, considerando el error de representación, la rentabilidad se mantiene prácticamente igual al valor calculado.

Gráficos:

Brecha de precios ("1_serie_mensual.png"): El gráfico muestra que febrero de 2023 tiene el precio más bajo de toda la serie, con $798,26 CLP, mientras que enero de 2025 tiene el valor más alto de $1.000,76 CLP. La diferencia entre ambos precios es de $202,50 CLP, entonces el error producido tiene un efecto pequeño versus la variación observada.

Máxima rentabilidad ("4_rentabilidad_desde_minimo.png"): Con la rentabilidad acumulada, enero de 2025 alcanza el valor máximo de la curva, llegando aproximadamente al 25%. Esto confirma gráficamente que la combinación de estos dos meses corresponde a la mejor estrategia del período analizado.

Error de representación ("3_error_representacion.png"): El gráfico muestra que los errores relativos producidos por el redondeo son pequeños en comparación con la variación de precios . Aunque el mayor error relativo de la serie alcanza 0,5987%, el error propagado al calcular esta rentabilidad es de solo +/- 0,07%. Por lo tanto, el efecto del redondeo no cambia de mucho el resultado obtenido.

A diferencia de lo observado en A3 y A4, donde la resta entre valores muy similares provoca el efecto de cancelación y aumenta el error relativo, en este caso los precios de compra y venta están suficientemente separados. Por esto, el intervalo de rentabilidad, [24,93%, 25,07%], se mantiene positivo y lejos de cero. Por esto, el error de represetación no afecta la conclusión: comprar en febrero de 2023 y vender en enero de 2025 corresponde a la estrategia más rentable y el resultado es confiable dentro del error calculado.


### Punto flotante (B1-B4)
**B1: muestra el error de representación al dejar 3 cifras.**

Las cifras significativas muestran cuánta precisión se conserva al representar un número. Esto se relaciona con la mantisa usada en la representación de números en punto flotante, ya que la mantisa contiene las cifras significativas del valor.

Cuando se utiliza una mantisa con menor precisión, se conserva menos información del número original y es necesario aproximarlo. Esto genera un error de representación que puede afectar los resultados de operaciones posteriores, especialmente cuando se realizan cálculos entre valores muy cercanos.

Demostración del error de representación con $1000.76 CLP a 3 cifras significativas:

- Valor real (SII): $1000.76 CLP.
- Valor aproximado: $1000.0 CLP.
- Error absoluto: $0.76 CLP.
- Error relativo: 0.0759%.

El valor aproximado puede expresarse como:

$1000.0 +/- 0.76 CLP, con un error relativo de 0.0759%.

Aunque el error absoluto es de $0.76 CLP, su efecto sobre el valor original es pequeño, porque representa un 0.0759% del precio real. Esto muestra que la importancia de un error no depende solo del valor absoluto, sino también del tamaño del número de compara.

Un error que parece pequeño puede adquirir mayor importancia cuando hay operaciones entre valores similares. En esos casos, la diferencia obtenida puede ser pequeña porque el error puede ser considerable sobre el resultado, produciendo el efecto de cancelación.


**B2. La ida y vuelta que no vuelve (Deriva en punto flotante)** (ver gráfico 5,)

Al realizar una conversión de CLP a USD y luego de USD a CLP, usando el mismo precio mensual del dólar y trabajando con precisión simple (float32), se debería recuperar el monto inicial de $1.000.000 CLP.

Sin embargo, el resultado final presenta pequeñas diferencias respecto al monto original. Estas diferencias se producen durante las operaciones de conversión y se mantienen en el resultado final.

Resultado observado:

- Monto inicial: $1.000.000 CLP.
- Formato utilizado: float32 (precisión simple).
- Deriva máxima observada: +/- $0.06 CLP aprox.

Como se observa en la figura 5_deriva_ida_y_vuelta.png, las diferencias se mantienen en valores pequeños, cercanos a +/- $0.06 CLP. Esto se debe a la precisión limitada con la que float32 representa los números.

Además, la deriva observada no sigue la tendencia del precio del dólar mostrada en 1_serie_mensual.png. Esto indica que estas pequeñas variaciones no dependen de que el dólar suba o baje, sino de como los números son almacenados y procesados por el computador.


**B4: Compara e indica cuántas cifras significativas válidas quedan en cada caso.**

Para ver el efecto de precisión del computador, se calculó la variación del dólar entre diciembre de 2022 y diciembre de 2023. Los valores utilizados fueron $875,66 CLP y $874,67 CLP, respectivamente.

Resultados obtenidos:

- float64 (doble precisión): −$0,99000000 CLP.
- float32 (precisión simple): −$0,98999023 CLP.
- Diferencia entre resultados: $0,00000977 CLP.

La diferencia entre float32 y float64 permite observar cómo la precisión de la máquina afecta el resultado cuando se restan números de valores muy similares.

En este caso, los precios son cercanos entre sí, por lo que al restar se produce una cancelación de cifras significativas. Con float64, obtenemos un resultado similar al esperado, mientras que float32 presenta una diferencia pequeña en los últimos decimales.

Esto se relaciona con lo observado en A3. Allí, la variación entre diciembre de 2022 y diciembre de 2023 fue de −$1,00 CLP, pero el error de representación alcanzó +/- $0,67 CLP, con un error relativo del 67%. En cambio, en la máquina la diferencia entre float32 y float64 es de $0,00000977 CLP.

## Conclusión

## **9. Conclusión final**

A partir del análisis realizado, se puede concluir que el mejor momento para comprar dólares fue en febrero de 2023, cuando el precio alcanzó su mínimo de $798,26 CLP. Este valor se encuentra por debajo de sus meses vecinos, enero de 2023 con $826,34 CLP y marzo de 2023 con $809,50 CLP, con diferencias de $28,08 CLP y $11,24 CLP, respectivamente. Como se observa en "1_serie_mensual.png" y "2_variacion_mes_a_mes.png", estas diferencias son grandes en comparación con los errores de representación analizados, por lo que el mínimo de febrero de 2023 se puede considerar confiable.

Por otro lado, el mejor momento para vender fue enero de 2025, cuando el dólar alcanzó su valor máximo de $1.000,76 CLP. Al compararlo con diciembre de 2024, cuyo valor fue de $982,30 CLP, y febrero de 2025, con $956,62 CLP, se obtienen diferencias de $18,46 CLP y $44,14 CLP. Estas diferencias también son amplias frente a los errores de representación, permitiendo considerar enero de 2025 como el máximo de la serie con un alto grado de confianza, tal como se observa en "1_serie_mensual.png" y "3_error_representacion.png".

Considerando ambos extremos, la estrategia más rentable es comprar en febrero de 2023 y vender en enero de 2025, teniendo una rentabilidad de 25,00% +/- 0,07%, con un error relativo de 0,29%. La figura "4_rentabilidad_desde_minimo.png" confirma que esta combinación tiene el mayor rendimiento dentro del período analizado. Además, el intervalo obtenido, entre 24,93% y 25,07%, permanece positivo, por lo que el error de representación no cambia la conclusión.

Sin embargo, no todos los resultados del período presentan el mismo nivel de confiabilidad. Un ejemplo es la comparación entre diciembre de 2022 y diciembre de 2023, donde la variación fue de solo −$1,00 +/- $0,67 CLP, con un error relativo de 67%. En este caso, el error tiene un peso importante respecto de la variación calculada, por lo que no es posible afirmar con seguridad que el dólar haya subido o bajado. Esto demuestra el efecto de cancelación analizado anteriormente.

En conjunto, el análisis muestra que la precisión de los datos y la forma en que estos se utilizan en las operaciones son fundamentales para interpretar correctamente los resultados. Mientras que las diferencias grandes, como las observadas entre febrero de 2023 y enero de 2025, permiten obtener conclusiones confiables, las diferencias muy pequeñas pueden quedar ocultas por el error y generar resultados poco confiables. Por lo tanto, no basta con calcular una variación; también es necesario evaluar el error asociado para determinar si esa variación realmente permite tomar una decisión.
