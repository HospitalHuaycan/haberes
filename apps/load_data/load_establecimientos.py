import os

import pandas as pd

from apps.constancia.models.anio import Anio
from apps.establecimiento.models.establecimiento import Establecimiento
from apps.load_data.insert_general import get_anio
from apps.load_data.load_constancia import EXCLUDE_LIBELE


def load_establecimiento(ANIO):
    # if ANIO == 2020:
    #     db_name = 'default'
    # else:
    db_name = 'haberes_' + str(ANIO)

    try:
        anio = get_anio(ANIO)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        BD = BASE_DIR + '/load_data/' + str(ANIO) + '/01/PLTABEST.xlsx'
        df = pd.read_excel(BD, dtype={'PROGSUB': 'string', 'CODEST': 'string'})
        list_zip = zip(df["PROGSUB"], df["CODEST"], df["DESEST"])

        for progsub, codest, desest in list_zip:
            print(desest)
            if codest not in EXCLUDE_LIBELE:
                try:
                    # Establecimiento.objects.using(db_name).get(progsub=progsub, codest=codest, desest=desest, anio=anio)
                    Establecimiento.objects.using(db_name).get(
                        progsub=progsub, codest=codest, anio=anio)
                    print("No Insert")
                except Establecimiento.DoesNotExist:
                    Establecimiento.objects.using(db_name).create(progsub=progsub, codest=codest, desest=desest,
                                                                  anio=anio)
                    print("Insert")

    except Anio.DoesNotExist:
        print(" Anio no existe en la BD")
