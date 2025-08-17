# fila = "1001    138255    1382551002     74445     744451006       571       5711047     50562     505621054     30000     300002006      7500      75002023      1500      15002092         0     526002181       350       3502182       100       1002272      5000      50002372      5440      54402501        50        502640         0     138263004         0     124433005         0       8433007         0       871"

fila_core = "1001    138255    1382551002     74445     744451006       571       5711047     39237     392371056     40000     400002006       800       8002023      1500      15002092         0     526002109         0      47002181       350       3502182       100       1002272      5000      50002372      6145      61452501        50        502640         0     138262641         0      18663004         0     124433005         0       5253007         0       871"


def procesar_fila(fila):
    fila_split = fila.split()
    for i in list(filter((lambda x: x % 2 == 0), range(-1, len(fila_split) - 2))):
        codigo = fila_split[i][-4:]
        if i == (len(fila_split) - 3):
            monto = fila_split[i + 2]
        else:
            monto = fila_split[i + 2][:-4]

        if monto[:-2]:
            monto_final = monto[:-2] + "." + monto[-2:]
        else:
            monto_final = "0." + monto[-2:]

        TIPOS_CONCEPTO = {
            'CODIGO': codigo,
            'MONTO': monto_final
        }

        print(TIPOS_CONCEPTO)

    return "TIPOS_CONCEPTO"


# procesar_fila(fila_core)
