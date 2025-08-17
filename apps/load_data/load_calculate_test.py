import os
from decimal import Decimal

import pandas as pd

from apps.constancia.models.concepto import Concepto
from apps.constancia.models.constancia import Constancia
from apps.constancia.models.constancia_detalle import ConstanciaDetalle
from apps.trabajador.models.trabajador import Trabajador
from apps.util.get_trabajador_api import get_trabajador_api_by_plaza

MES = 1


def run_file_load_data_test():
    trabajador_no_encontrado = 0
    # df = pd.read_excel(BASE_DIR + '/index/DATOSPLH.xlsx', engine='openpyxl', dtype={'LIBELE': 'string'})
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BD = BASE_DIR + '/load_data/2020/01/PLMOVMAE.xlsx'
    # df = pd.read_excel(BD, dtype={'LIBELE': 'string'}).query('PLAZA == 113643')
    # df = pd.read_excel(BD, header=1, usecols='L:N').query('PLAZA == 113643')
    # df = pd.read_excel(BD).query('PLAZA == 113643')
    df = pd.read_excel(BD)

    list_zip = zip(df["PLAZA"], df["C1"], df["C2"], df["C3"], df["C4"])

    for plaza, c1, c2, c3, c4 in list_zip:
        print("************************************************")
        print(plaza)
        fila = str(c1) + str(c2) + str(c3) + str(c4)
        print(fila)

        try:
            trabajador = Trabajador.objects.get(plaza=plaza)
            print(trabajador)

        except Trabajador.DoesNotExist:
            print("Trabajador no existe jojojo sssssssssssssssssssssss ")
            print(" PLAZA ->> " + str(plaza))
            response_json = get_trabajador_api_by_plaza(str(plaza))

            if response_json['results']:
                trabajador_json = response_json['results'][0]

                print(trabajador_json)
                print("-------------->>")

                trabajador = Trabajador(dni=trabajador_json['dni'].strip(),
                                        apellidos_nombres=trabajador_json['apellidos_nombres'].strip(),
                                        fecha_nacimiento=trabajador_json['fecha_nacimiento'],
                                        depedencia_id=trabajador_json['depedencia']['id'], plaza=plaza,
                                        cargo=trabajador_json['cargo'], tipo=trabajador_json['tipo'])
                trabajador.save()

        try:
            trabajador = Trabajador.objects.get(plaza=plaza)
            if trabajador:
                try:
                    constancia = Constancia.objects.get(trabajador=trabajador, anio_id=1)
                    print(" CONSTANCIA ")
                    print(constancia)
                except Constancia.DoesNotExist:
                    print(" Constancia NO  Existe ")
                    constancia = Constancia(trabajador=trabajador, anio_id=1)
                    constancia.save()

                fila_split = fila.split()

                for i in list(filter((lambda x: x % 2 == 0), range(-1, len(fila_split) - 2))):
                    codigo = fila_split[i][-4:]
                    if i == (len(fila_split) - 3):

                        monto = fila_split[i + 2][:-6]
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

                    print("------------------------------------------------")

                    try:
                        concepto = Concepto.objects.get(codigo=codigo)
                    except Concepto.DoesNotExist:
                        concepto = Concepto(codigo=codigo, nombre=codigo)
                        concepto.save()

                    try:
                        constancia_detalle = ConstanciaDetalle.objects.get(constancia=constancia, mes=MES,
                                                                           concepto=concepto)
                        print(constancia_detalle)
                    except ConstanciaDetalle.DoesNotExist:
                        print(" Constancia Detalle  no Existe ")
                        constancia_detalle = ConstanciaDetalle(trabajador=trabajador, anio_id=1, constancia=constancia,
                                                               mes=MES,
                                                               concepto=concepto, monto=Decimal(monto_final))
                        constancia_detalle.save()



        except Trabajador.DoesNotExist:
            print("NO valueee  ")
            trabajador_no_encontrado += 1

    print("Trabajadores no encontrados")
    print(trabajador_no_encontrado)
