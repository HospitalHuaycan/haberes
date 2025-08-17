import os
from datetime import datetime

import pandas as pd

# from apps.entidad.models.dependencia import Dependencia
from apps.entidad.models.dependencia import Dependencia
from apps.trabajador.models.trabajador import Trabajador


def import_trabajador():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_excel(BASE_DIR + '/index/DATOSPLH.xlsx', engine='openpyxl', dtype={'LIBELE': 'string'})

    # print(df[['PLAZA', 'NOMBRE', 'CODCAR']])
    #
    # for i in df[['PLAZA', 'NOMBRE', 'CODCAR']]:
    #     print(type(i))
    #

    # data = df["PLAZA"]

    list_zip = zip(df["PLAZA"], df["NOMBRE"], df["CODCAR"], df["TIPOPLA"], df["CODEST"], df["LIBELE"],
                   df["FECNAC"])

    temp = 0
    for plaza, nombre, codcar, tipopla, codest, libele, fecnac in list_zip:


        depedencia = Dependencia.objects.get(codigo=codest.split("-")[0].strip())

        temp += 1

        try:
            Trabajador.objects.get(dni=libele.strip())
        except Trabajador.DoesNotExist:
            trabajador = Trabajador(dni=libele.strip(), apellidos_nombres=nombre,
                                    fecha_nacimiento=fecnac,
                                    depedencia_id=depedencia.id, plaza=plaza, cargo=codcar, tipo=tipopla)

            trabajador.save()


#
# dni = models.CharField(_('DNI'), max_length=8, unique=True)
# apellidos_nombres = models.CharField(_('Apellidos y nombres'), max_length=130)
# fecha_nacimiento = models.DateField(_('Fecha de nacimiento'))
# depedencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE)
# plaza = models.CharField(_('Plaza'), max_length=10, unique=True)
# cargo = models.CharField(_('Cargo'), max_length=100)
# tipo = models.PositiveIntegerField(choices=TIPOS_TRABAJADOR, default=1)
#
# print(plaza)
# print(nombre)
# print(codcar)
# print(tipopla)
# print(progsub)
# print(libele)
# print(fecnac)

# print(BD)
# print("--->>>")
# print(BD.head(3))
# print(BD.tail(3))
# import_trabajador()
