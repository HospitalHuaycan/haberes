import os
from decimal import Decimal

import pandas as pd

from apps.constancia.models.constancia import Constancia
from apps.constancia.models.constancia_detalle import ConstanciaDetalle
from apps.load_data.insert_general import get_anio
from apps.trabajador.models.trabajador import Trabajador

EXCLUDE_LIBELE = [11111111, 22222222, 33333333, 44444444, 55555555, 66666666, 77777777, 88888888, 99999999, '*********',
                  '********']

db_name = 'haberes_2018'

MES = 12


def load_test(ANIO):
    anio = get_anio(ANIO)

    print(" --->>> ANIO, -->>> ")
    print(anio)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BD = BASE_DIR + '/load_data/diciembre_falta.xlsx'
    df_source = pd.read_excel(BD, dtype={'LIBELE': 'string', })
    df_source_1 = df_source.loc[df_source["RESCES"].isnull()]  # Limite de edad o cese
    df_other = df_source_1.loc[df_source_1["C1"].notnull()]  # Conceptos y montos
    # df_other = df_source_1.loc[df_source_1["EC1"].notnull()]  # SOLO PARA EL 2020
    df = df_other.loc[df_other["INDICA"].notnull()]  # W

    list_zip = zip(df["PLAZA"], df["LIBELE"], df["NOM"], df["PAT"], df["MAT"], df["FECNAC"], df["SEXO"],
                   df["NHIJOS"],
                   df["C1"], df["C2"], df["C3"], df["C4"], df["CODEJE"], df["CODFUN"], df["CODPRO"], df["CODSUB"],
                   df["TIPOPLA"], df["PROGSUB"], df["CODEST"], df["CODCOM"], df["SERV"], df["CODCAR"], df["CODNIV"])

    contador = 1

    for count, data in enumerate(list_zip):
        print(" Primero  ")
        if (data[18] != 999999999) and (data[1] not in EXCLUDE_LIBELE):
            print(" Segundo  ")
            fila = ""
            contador += 1

            # if str(data[1]) != "nan" and data[23][1] == '1':
            if str(data[1]) != "nan":
                print(" DNI -->> " + str(data[1]))
                try:
                    trabajador = Trabajador.objects.using('haberes_2019').get(dni=str(data[1]))

                    print(" Trabajador encontrado ")
                    print(trabajador.pk)

                    if trabajador.apellido_paterno == str(data[3]):
                        print(" Trabajador existe !! ")

                        try:
                            constancia = Constancia.objects.using(db_name).get(trabajador_id=trabajador.pk,
                                                                               anio_id=anio.pk,
                                                                               plaza=data[0])
                        except Constancia.DoesNotExist:
                            constancia = Constancia.objects.using(db_name).create(trabajador_id=trabajador.pk,
                                                                                  anio_id=anio.pk,
                                                                                  plaza=data[0], nivel=data[22],
                                                                                  codcar=data[21], codest=data[18])

                        print(" Contancia ")
                        print(" --->>>>>  ")

                        if str(data[8]) != "nan":
                            fila = fila + str(data[8])

                        if str(data[9]) != "nan":
                            fila = fila + str(data[9])

                        if str(data[10]) != "nan":
                            fila = fila + str(data[10])

                        fila_split = fila.split()

                        size_list = len(fila_split)

                        for i in list(filter((lambda x: x % 2 == 0), range(-1, len(fila_split) - 2))):

                            codigo = fila_split[i][-4:]
                            if (size_list - 3) == i:
                                monto = fila_split[i + 2]
                            else:
                                monto = fila_split[i + 2][:-4]

                            print(" -------------------------->>>>> ")
                            print(monto)
                            if monto[:-2]:
                                monto_final = monto[:-2] + "." + monto[-2:]
                            else:
                                if len(monto) == 2:
                                    monto_final = "0." + monto[-2:]
                                else:
                                    monto_final = "0.0" + monto[-2:]

                            print(codigo)
                            print(" Monto final ")
                            print(monto_final)

                            try:
                                constancia_detalle = ConstanciaDetalle.objects.using(db_name).get(constancia_id=constancia.pk,
                                                                                                  anio_id=anio.pk, mes=MES,
                                                                                                  concepto=codigo)
                                constancia_detalle.monto = constancia_detalle.monto + Decimal(monto_final)
                                constancia_detalle.save(using=db_name)

                                print(" Constancia no existe-- jojo jo")

                            except ConstanciaDetalle.DoesNotExist:
                                ConstanciaDetalle.objects.using(db_name).create(constancia_id=constancia.pk,
                                                                                trabajador_id=trabajador.pk,
                                                                                anio_id=anio.pk, mes=MES, concepto=codigo,
                                                                                monto=monto_final, codeje=data[12],
                                                                                codfun=data[13],
                                                                                codpro=data[14], codsud=data[15],
                                                                                tipopla=data[16],
                                                                                progsub=data[17], codest=data[18],
                                                                                codcom=data[19],
                                                                                serv=data[20], codcar=data[21],
                                                                                codniv=data[22])

                                print(" Constancia guardada")


                except Trabajador.DoesNotExist:
                    print(" Trabajador no existe")
