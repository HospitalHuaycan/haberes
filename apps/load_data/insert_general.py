from apps.constancia.models.anio import Anio

anios = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021,2022,2023,2024,2025]


def get_anio(ANIO):
    if ANIO == 2020:
        db_name = 'default'
    else:
        db_name = 'haberes_' + str(ANIO)

    for i in anios:
        try:
            Anio.objects.using(db_name).get(anio=int(i))
        except Anio.DoesNotExist:
            Anio.objects.using(db_name).create(anio=i)

    try:
        anio_current = Anio.objects.using(db_name).get(anio=int(ANIO))
    except Anio.DoesNotExist:
        anio_current = Anio.objects.using(db_name).create(anio=ANIO)

    return anio_current
