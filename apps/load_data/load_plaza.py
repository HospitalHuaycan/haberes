import os

import pandas as pd

from apps.constancia.models.constancia import Constancia

MES = 1
ANIO = 1

EXCLUDE_LIBELE = [11111111, 22222222, 33333333, 44444444, 55555555, 66666666, 77777777, 88888888, 99999999]


def run_load_plaza():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BD = BASE_DIR + '/load_data/2020/0' + str(MES) + '/PLMOVMAE.xlsx'
    df_source = pd.read_excel(BD, dtype={'LIBELE': 'string', })

    df_source_1 = df_source.loc[df_source["RESCES"].isnull()]  # Limite de edad o cese
    df_other = df_source_1.loc[df_source_1["EC1"].notnull()]  # Conceptos y montos
    df = df_other.loc[df_other["INDICA"].notnull()]  # W

    list_zip = zip(df["PLAZA"], df["LIBELE"], df["NOM"], df["PAT"], df["MAT"], df["FECNAC"], df["SEXO"], df["NHIJOS"],
                   df["C1"], df["C2"], df["C3"], df["C4"], df["CODEJE"], df["CODFUN"], df["CODPRO"], df["CODSUB"],
                   df["TIPOPLA"], df["PROGSUB"], df["CODEST"], df["CODCOM"], df["SERV"], df["CODCAR"], df["CODNIV"],
                   df["EC1"])

    contador = 0
    for count, data in enumerate(list_zip):

        if (data[18] != 999999999) and (data[1] not in EXCLUDE_LIBELE):

            fila = ""
            print(" CONTADOR --> " + str(contador))
            contador += 1

            if str(data[1]) != "nan" and data[23][1] == '1':
                print(data[0])
                try:
                    constancia = Constancia.objects.get(trabajador__dni=str(data[1]), anio_id=1)
                    constancia.plaza = data[0]
                    constancia.nivel = data[22]
                    constancia.codcar = data[21]
                    constancia.codest = data[18]
                    constancia.save()
                    print("Constancia actualizada -->> " + constancia.trabajador.nombre_completo)
                except Constancia.DoesNotExist:
                    print("constancia no encontrada")
