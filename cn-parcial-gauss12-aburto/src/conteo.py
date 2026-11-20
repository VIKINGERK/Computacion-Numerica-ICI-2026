def tabla_por_paso(contador):
    n = contador.n
    f = ["| Paso k | Divisiones (multiplicadores) | Multiplicaciones | Mult/Div | "
         "Restas | Sumas | Sumas/Restas | Flops del paso |",
         "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    tot = {"div": 0, "mul": 0, "res": 0, "sum": 0}
    for k, d in enumerate(contador.pasos, start=1):
        for t in tot:
            tot[t] += d[t]
        f.append(f"| {k} | {d['div']} | {d['mul']} | {contador.muldiv(d)} | {d['res']} | "
                 f"{d['sum']} | {contador.sumres(d)} | {contador.flops(d)} |")
    f.append(f"| *Eliminacion (1 a {n - 1})* | *{tot['div']}* | *{tot['mul']}* | "
             f"*{tot['div'] + tot['mul']}* | *{tot['res']}* | *{tot['sum']}* | "
             f"*{tot['res'] + tot['sum']}* | *{contador.flops_eliminacion()}* |")
    s = contador.sust
    f.append(f"| Sustitucion regresiva | {s['div']} | {s['mul']} | {contador.muldiv(s)} | "
             f"{s['res']} | {s['sum']} | {contador.sumres(s)} | {contador.flops(s)} |")
    muldiv = tot['div'] + tot['mul'] + contador.muldiv(s)
    sumres = tot['res'] + tot['sum'] + contador.sumres(s)
    f.append(f"| *TOTAL* | *{tot['div'] + s['div']}* | *{tot['mul'] + s['mul']}* | "
             f"*{muldiv}* | *{tot['res'] + s['res']}* | *{tot['sum'] + s['sum']}* | "
             f"*{sumres}* | *{contador.flops_total()}* |")
    return f


def tabla_sobrecosto(contador):
    f = ["| Paso k | Comparaciones | Divisiones de escalado | Intercambios de filas |",
         "| --- | --- | --- | --- |"]
    if contador.pre["cmp"]:
        f.append(f"| Escalas de fila (previo) | {contador.pre['cmp']} | {contador.pre['div_piv']} | 0 |")
    for k, d in enumerate(contador.pasos, start=1):
        f.append(f"| {k} | {d['cmp']} | {d['div_piv']} | {d['swap']} |")
    f.append(f"| *TOTAL* | *{contador.comparaciones()}* | *{contador.divisiones_pivoteo()}* | "
             f"*{contador.intercambios()}* |")
    return f


def reporte_markdown(corridas):
    contador = corridas["escalado"].contador

    L = [
        "# Tabla de operaciones por paso\n",
        "Conteo de operaciones elementales por paso (1 flop = suma, resta, multiplicacion o division).\n"
    ]
    L.extend(tabla_por_paso(contador))
    L.append("")
    L.append("## Sobrecosto de estabilidad (pivoteo parcial escalado)\n")
    L.extend(tabla_sobrecosto(contador))
    return "\n".join(L) + "\n"