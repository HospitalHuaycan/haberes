import os

import pandas as pd

MES = 1


def run_file_load_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BD = BASE_DIR + '/load_data/2020/01/PLMOVMAE.xlsx'
    df_source = pd.read_excel(BD).query('CODEST == 888888888 or CODEST == 999999999', inplace=True)
    df = df_source.loc[df_source["RESCES"].isnull()]

    list_zip = zip(df["PLAZA"], df["LIBELE"], df["NOM"], df["PAT"], df["MAT"], df["FECNAC"], df["SEXO"], df["NHIJOS"],
                   df["C1"], df["C2"], df["C3"], df["C4"], df["CODEJE"], df["CODFUN"], df["CODPRO"], df["CODSUB"],
                   df["TIPOPLA"], df["PROGSUB"], df["CODEST"], df["CODCOM"], df["SERV"], df["CODCAR"], df["CODNIV"],
                   df["EC1"])

    count = 0
    for a in list_zip:
        print(count)
        # if str(a[1]) != "nan" and a[23][1] == '1':
        #     # print(a[8])
        #     print(a[8])
        count += 1

    print(count)

    # for count, data in enumerate(list_zip):
    #
    #     fila = ""
    #     print("******************************************")
    #     print(" data", data)
    #     # if str(data[0]) != "nan":
    #     #     fila = fila + str(data[0])
    #
    #     if str(data[8]) != "nan":
    #         fila = fila + str(data[8])
    #
    #     if str(data[9]) != "nan":
    #         fila = fila + str(data[9])
    #
    #     if str(data[10]) != "nan":
    #         fila = fila + str(data[10])
    #
    #     if count == 500:
    #         break
    #
    #     print(" FILA --->>> " + fila)
    #
    #     fila_split = fila.split()
    #
    #     print(fila_split)
    #
    #     size_list = len(fila_split)
    #     print(size_list)
    #     print("DDD")
    #
    #     for i in list(filter((lambda x: x % 2 == 0), range(-1, len(fila_split) - 2))):
    #
    #         codigo = fila_split[i][-4:]
    #         if (size_list - 3) == i:
    #             monto = fila_split[i + 2]
    #         else:
    #             monto = fila_split[i + 2][:-4]
    #
    #         if monto[:-2]:
    #             monto_final = monto[:-2] + "." + monto[-2:]
    #         else:
    #             monto_final = "0." + monto[-2:]
    #
    #         TIPOS_CONCEPTO = {
    #             'CODIGO': codigo,
    #             'MONTO': monto_final
    #         }
    #
    #         print(TIPOS_CONCEPTO)
    #
    #         print("------------------------------------------------")
    #
    # print("************************************************")


# run_file_load_data()
