# import os
#
# import pandas as pd
#
# from apps.trabajador.models.trabajador import Trabajador
# from apps.util.get_trabajador_api import get_trabajador_api_by_plaza
#
# MES = 1
#
#
# def run_file_load_data():
#     # df = pd.read_excel(BASE_DIR + '/index/DATOSPLH.xlsx', engine='openpyxl', dtype={'LIBELE': 'string'})
#     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     BD = BASE_DIR + '/load_data/2020/01/PLMOVMAE.xlsx'
#     # df = pd.read_excel(BD, dtype={'LIBELE': 'string'}).query('PLAZA == 113643')
#     # df = pd.read_excel(BD, header=1, usecols='L:N').query('PLAZA == 113643')
#     # df = pd.read_excel(BD).query('PLAZA == 113643')
#     df = pd.read_excel(BD)
#
#     list_zip = zip(df["PLAZA"], df["C1"], df["C2"], df["C3"], df["C4"])
#
#     for count, data in enumerate(list_zip):
#
#         fila = ""
#         print("******************************************")
#         print(" data", data)
#         # if str(data[0]) != "nan":
#         #     fila = fila + str(data[0])
#
#         if str(data[1]) != "nan":
#             fila = fila + str(data[1])
#
#         if str(data[2]) != "nan":
#             fila = fila + str(data[2])
#
#         if str(data[3]) != "nan":
#             fila = fila + str(data[3])
#
#         if count == 20:
#             break
#
#         print(" FILA --->>> " + fila)
#         try:
#             trabajador = Trabajador.objects.get(plaza=data[0])
#             print(trabajador)
#         except Trabajador.DoesNotExist:
#             print("Trabajador no existe jojojo ")
#             response_json = get_trabajador_api_by_plaza(str(data[0]))
#
#             if response_json['results']:
#                 print(" JSON ENCONTRADO")
#                 trabajador_json = response_json['results'][0]
#
#                 print(trabajador_json)
#                 print("-------------->>")
#
#                 trabajador = Trabajador(dni=trabajador_json['dni'].strip(),
#                                         apellidos_nombres=trabajador_json['apellidos_nombres'].strip(),
#                                         fecha_nacimiento=trabajador_json['fecha_nacimiento'],
#                                         depedencia_id=trabajador_json['depedencia']['id'], plaza=data[0],
#                                         cargo=trabajador_json['cargo'], tipo=trabajador_json['tipo'])
#                 trabajador.save()
#
#         # try:
#         #     constancia = Constancia.objects.get(trabajador=trabajador, anio_id=1)
#         #     print(" CONSTANCIA ")
#         #     print(constancia)
#         # except Constancia.DoesNotExist:
#         #     constancia = Constancia(trabajador=trabajador, anio_id=1)
#         #     constancia.save()
#         #
#         # fila_split = fila.split()
#         #
#         # for i in list(filter((lambda x: x % 2 == 0), range(-1, len(fila_split) - 2))):
#         #     codigo = fila_split[i][-04:]
#         #     if i == (len(fila_split) - 3):
#         #
#         #         monto = fila_split[i + 2][:-6]
#         #     else:
#         #         monto = fila_split[i + 2][:-04]
#         #
#         #     if monto[:-2]:
#         #         monto_final = monto[:-2] + "." + monto[-2:]
#         #     else:
#         #         monto_final = "0." + monto[-2:]
#         #
#         #     TIPOS_CONCEPTO = {
#         #         'CODIGO': codigo,
#         #         'MONTO': monto_final
#         #     }
#         #
#         #     print("------------------------------------------------")
#         #
#         #     try:
#         #         concepto = Concepto.objects.get(codigo=codigo)
#         #     except Concepto.DoesNotExist:
#         #         concepto = Concepto(codigo=codigo, nombre=codigo)
#         #         concepto.save()
#         #
#         #     try:
#         #         constancia_detalle = ConstanciaDetalle.objects.get(constancia=constancia, mes=MES, concepto=concepto)
#         #         print(constancia_detalle)
#         #     except ConstanciaDetalle.DoesNotExist:
#         #         print(" Constancia no Existe ")
#         #         constancia_detalle = ConstanciaDetalle(trabajador=trabajador, anio_id=1, constancia=constancia, mes=MES,
#         #                                                concepto=concepto, monto=Decimal(monto_final))
#         #         constancia_detalle.save()
#
#     print("************************************************")
