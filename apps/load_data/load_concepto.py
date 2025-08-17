import os

import pandas as pd

from apps.concepto.models.concepto import Concepto
from apps.constancia.models.anio import Anio
from apps.load_data.insert_general import get_anio

anios = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]


def load_concepto(MES, ANIO):
    if ANIO == 2020:
        db_name = 'default'
    else:
        db_name = 'haberes_' + str(ANIO)

    try:
        anio = get_anio(ANIO)

        mes_string = str(MES) if MES >= 10 else '0' + str(MES)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        BD = BASE_DIR + '/load_data/' + str(ANIO) + '/' + mes_string + '/PLTABCON.xlsx'
        df = pd.read_excel(BD, dtype={'CODCON': 'string', })
        list_zip = zip(df["TIPARCH"], df["CODCON"], df["DESCON"], df["ABRCON"], df["MODIFI"], df["DESCON1"])

        for c1, c2, c3, c4, c5, c6 in list_zip:
            print(c3)
            try:
                Concepto.objects.using(db_name).get(tiparch=c1, codcon=c2, mes=MES, anio=anio)
                print(" No insert ")
            except Concepto.DoesNotExist:

                if not pd.isnull(c5):
                    Concepto.objects.using(db_name).create(tiparch=c1, codcon=c2, descon=c3, abrcon=c4, modifi=c5,
                                                           descon1=c6, mes=MES, anio=anio)
                else:
                    Concepto.objects.using(db_name).create(tiparch=c1, codcon=c2, descon=c3, abrcon=c4, descon1=c6,
                                                           mes=MES, anio=anio)
                print(" Insert ")

    except Anio.DoesNotExist:
        print(" Anio no existe en la BD")
