from apps.trabajador.models.trabajador import Trabajador


def run_update_trabajador():
    trabajadores = Trabajador.objects.all()

    for t in trabajadores:
        print(t)
        t.nombre_completo = t.apellido_paterno + " " + t.apellido_materno + " " + t.nombres
        t.save()
