from django import template

from apps.cargo.models.cargo import Cargo
from apps.constancia.models.constancia_detalle import ConstanciaDetalle
from apps.constancia.views.constancia import EXCLUDE_LIBELE
from apps.establecimiento.models.establecimiento import Establecimiento

register = template.Library()


@register.simple_tag
def get_establecimiento(anio_bd, trabajador, anio):
    detalles = ConstanciaDetalle.objects.using(anio_bd).filter(trabajador=trabajador, anio=int(anio))
    establecimiento_descripcion = " -- "

    if len(detalles) > 0:
        detalle_codest = detalles.last().codest

        try:
            if detalle_codest not in EXCLUDE_LIBELE:
                establecimiento = Establecimiento.objects.using(anio_bd).filter(codest=detalle_codest).last()
                if establecimiento:
                    establecimiento_descripcion = establecimiento.desest
        except Establecimiento.DoesNotExist:
            print(" No encontrado")

    return establecimiento_descripcion


@register.simple_tag
def get_cargo(anio_bd, trabajador, anio):
    detalles = ConstanciaDetalle.objects.using(anio_bd).filter(trabajador=trabajador, anio=int(anio))

    cargo_descripcion = ""

    if len(detalles) > 0:
        detalle_codcar = detalles.last().codcar if len(detalles.last().codcar) == 4 else "0" + detalles.last().codcar
        try:
            cargo = Cargo.objects.filter(codcar=detalle_codcar).last()
            if cargo:
                cargo_descripcion = cargo.descar
            else:
                cargo_descripcion = '--'
        except Cargo.DoesNotExist:
            print(" No encontrado")

    return cargo_descripcion
