import os

import pandas as pd

from apps.cargo.models.cargo import Cargo
from apps.constancia.models.anio import Anio
from apps.load_data.insert_general import get_anio


def load_cargos(ANIO):
    if ANIO == 2020:
        db_name = 'default'
    else:
        db_name = 'haberes_' + str(ANIO)

    try:
        anio = get_anio(ANIO)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        BD = BASE_DIR + '/load_data/' + str(ANIO) + '/01/PLTABCAR.xlsx'
        df = pd.read_excel(BD, dtype={'CODANT': 'string', 'CODCAR': 'string'})

        list_zip = zip(df["CODANT"], df["CODCAR"], df["DESCAR"])

        for c1, c2, c3 in list_zip:
            print(c3)
            if c2 and c3:

                try:
                    Cargo.objects.using(db_name).get(codant=str(c1).strip(), codcar=c2, descar=c3, anio=anio)
                    print("No Insert")
                except Cargo.DoesNotExist:
                    if not pd.isnull(c1):
                        Cargo.objects.using(db_name).create(codant=str(c1).strip(), codcar=c2, descar=c3, anio=anio)
                    else:
                        Cargo.objects.using(db_name).create(codcar=c2, descar=c3, anio=anio)
                    print("Insert")

    except Anio.DoesNotExist:
        print(" Anio no existe en la BD")
