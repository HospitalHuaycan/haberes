from decimal import Decimal

from django.views.generic import TemplateView

from apps.cargo.models.cargo import Cargo
from apps.concepto.models.concepto import Concepto
from apps.constancia.forms.constancia import ConstanciaListFilter
from apps.constancia.models.anio import Anio
from apps.constancia.models.constancia import Constancia
from apps.constancia.models.constancia_detalle import MESES, ConstanciaDetalle
from apps.establecimiento.models.establecimiento import Establecimiento
from apps.trabajador.models.trabajador import Trabajador
from apps.util.generic_filters.views import FilteredListViewConstancia

EXCLUDE_LIBELE = [11111111, 22222222, 33333333, 44444444, 55555555, 66666666, 77777777, 88888888, 99999999]


class ConstanciaList(FilteredListViewConstancia):
    model = Constancia
    paginate_by = 30
    form_class = ConstanciaListFilter
    filter_fields = []
    search_fields = ['trabajador__nombre_completo', 'trabajador__dni', 'plaza']
    default_order = 'id'

    def get_context_data(self, **kwargs):
        title = "Todas las constancias"
        return dict(
            super(ConstanciaList, self).get_context_data(**kwargs), title=title)

    def get_queryset(self):

        anio_id = self.request.session["anio"]

        try:
            anio = Anio.objects.get(pk=anio_id)

            if anio.anio == 2020:
                db_name = 'default'
            else:
                db_name = 'haberes_' + str(anio.anio)
            #
            # queryset = Constancia.objects.using(db_name).all()
            # return queryset

            queryset = super().get_queryset()
            return queryset.using(db_name).all().order_by('-plaza')
            # return queryset

        except Anio.DoesNotExist:
            queryset = super().get_queryset()
            # return queryset.filter(trabajador__nombre_completo__icontains="CASTRO LIZARRAGA").order_by('-id')
            return queryset

        # return queryset


# def generar_constancia(trabajador_id, anio_id, pk):
def generar_constancia(request, pk):
    try:

        # anio = Anio.objects.get(pk=anio_id)
        # trabajador = Trabajador.objects.get(id=trabajador_id)

        constancia = Constancia.objects.using(request.session["anio_bd"]).get(pk=int(pk))

        conceptos = constancia.constanciadetalle_set.values_list('concepto').order_by('concepto').distinct()

        concepto_ingresos_list = conceptos.filter(concepto__startswith='1')
        concepto_descuentos_list = conceptos.filter(concepto__startswith='2')
        concepto_aportes_list = conceptos.filter(concepto__startswith='3')

        monto_ingreso_list = []
        monto_ingreso_list_total = ["TOTAL", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                                    0.00, 0.00]

        for i in concepto_ingresos_list:
            monto_ingreso_mes = [i[0]]
            monto_count = Decimal(0.00)
            for j in MESES:
                try:
                    detalle = ConstanciaDetalle.objects.using(request.session["anio_bd"]).get(constancia=constancia,
                                                                                              mes=j[0], concepto=i[0])
                    # if j[0] == 1:
                    # TODO - VALIDAR, OJO
                    # concepto = Concepto.objects.filter(codcon=detalle.concepto, mes=j[0], anio=anio.anio).order_by(
                    #     'tiparch').last()

                    concepto = Concepto.objects.using(request.session["anio_bd"]).filter(codcon=detalle.concepto,
                                                                                         mes=j[0]).order_by(
                        'tiparch').last()

                    if concepto:
                        monto_ingreso_mes[0] = concepto.abrcon
                    else:
                        monto_ingreso_mes[0] = "-"
                    monto_ingreso_mes.append(detalle)
                    monto_count += detalle.monto
                    monto_ingreso_list_total[j[0]] = Decimal(monto_ingreso_list_total[j[0]]) + detalle.monto
                except ConstanciaDetalle.DoesNotExist:
                    monto_ingreso_mes.append(" ")
            monto_ingreso_mes.append(monto_count)
            monto_ingreso_list_total[13] = Decimal(monto_ingreso_list_total[13]) + monto_count
            monto_ingreso_list.append(monto_ingreso_mes)

        monto_descuento_list = []
        monto_descuento_list_total = ["TOTAL", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                                      0.00, 0.00]
        for i in concepto_descuentos_list:
            monto_ingreso_mes = [i[0]]
            monto_count = Decimal(0.00)
            for j in MESES:
                try:
                    detalle = ConstanciaDetalle.objects.using(request.session["anio_bd"]).get(constancia=constancia,
                                                                                              mes=j[0], concepto=i[0])
                    # if j[0] == 1:
                    concepto = Concepto.objects.using(request.session["anio_bd"]).filter(codcon=detalle.concepto,
                                                                                         mes=j[0]).order_by(
                        'tiparch').last()
                    if concepto:
                        monto_ingreso_mes[0] = concepto.abrcon
                    else:
                        monto_ingreso_mes[0] = "-"
                    monto_ingreso_mes.append(detalle)
                    monto_count += detalle.monto
                    monto_descuento_list_total[j[0]] = Decimal(monto_descuento_list_total[j[0]]) + detalle.monto
                except ConstanciaDetalle.DoesNotExist:
                    monto_ingreso_mes.append(" ")
            monto_ingreso_mes.append(monto_count)
            monto_descuento_list_total[13] = Decimal(monto_descuento_list_total[13]) + monto_count
            monto_descuento_list.append(monto_ingreso_mes)

        monto_liquido_list_total = ["TOTAL", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                                    0.00]

        for i in range(1, 14):
            monto_liquido_list_total[i] = Decimal(monto_ingreso_list_total[i]) - Decimal(monto_descuento_list_total[i])

        monto_aportaciones_list = []
        monto_aportaciones_list_total = ["TOTAL", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                                         0.00, 0.00, 0.00]
        for i in concepto_aportes_list:
            monto_ingreso_mes = [i[0]]
            monto_count = Decimal(0.00)
            for j in MESES:
                try:
                    detalle = ConstanciaDetalle.objects.using(request.session["anio_bd"]).get(constancia=constancia,
                                                                                              mes=j[0], concepto=i[0])
                    # if j[0] == 1:
                    concepto = Concepto.objects.using(request.session["anio_bd"]).filter(codcon=detalle.concepto,
                                                                                         mes=j[0]).order_by(
                        'tiparch').last()
                    if concepto:
                        monto_ingreso_mes[0] = concepto.abrcon
                    else:
                        monto_ingreso_mes[0] = "-"
                    monto_ingreso_mes.append(detalle)
                    monto_count += detalle.monto
                    monto_aportaciones_list_total[j[0]] = Decimal(
                        monto_aportaciones_list_total[j[0]]) + detalle.monto
                except ConstanciaDetalle.DoesNotExist:
                    monto_ingreso_mes.append(" ")
            monto_ingreso_mes.append(monto_count)
            monto_aportaciones_list_total[13] = Decimal(monto_aportaciones_list_total[13]) + monto_count
            monto_aportaciones_list.append(monto_ingreso_mes)

        return {
            'trabajador': constancia.trabajador,
            'monto_ingreso_list': monto_ingreso_list,
            'monto_descuento_list': monto_descuento_list,
            'monto_ingreso_list_total': monto_ingreso_list_total,
            'monto_descuento_list_total': monto_descuento_list_total,
            'monto_liquido_list_total': monto_liquido_list_total,
            'monto_aportaciones_list': monto_aportaciones_list,
            'monto_aportaciones_list_total': monto_aportaciones_list_total,
            'anio': constancia.anio,
            'constancia': constancia,
        }

    except Trabajador.DoesNotExist:
        return {
            'trabajador': '',
            'monto_ingreso_list': [],
            'monto_descuento_list': [],
            'monto_ingreso_list_total': [],
            'monto_descuento_list_total': [],
            'monto_liquido_list_total': [],
            'monto_aportaciones_list': [],
            'monto_aportaciones_list_total': [],
            'constancia': '',
        }


class GenerarConstanciaView(TemplateView):
    template_name = "constancia/generar_constancia.html"

    def get_context_data(self, **kwargs):
        # trabajador_id = self.request.GET.get('trabajador_id', 0)
        # anio_id = int(self.request.GET.get('anio_id', 1))
        pk = int(self.request.GET.get('pk', 1))

        constancia = generar_constancia(self.request, pk)
        context = super(GenerarConstanciaView, self).get_context_data(**kwargs)
        context['trabajador'] = constancia['trabajador']
        context['monto_ingreso_list'] = constancia['monto_ingreso_list']
        context['monto_descuento_list'] = constancia['monto_descuento_list']
        context['monto_ingreso_list_total'] = constancia['monto_ingreso_list_total']
        context['monto_descuento_list_total'] = constancia['monto_descuento_list_total']
        context['monto_liquido_list_total'] = constancia['monto_liquido_list_total']
        context['monto_aportaciones_list'] = constancia['monto_aportaciones_list']
        context['monto_aportaciones_list_total'] = constancia['monto_aportaciones_list_total']
        context['anio'] = constancia['anio']
        context['constancia'] = constancia['constancia']
        return context


def get_establecimiento(anio_bd, trabajador, anio):
    detalles = ConstanciaDetalle.objects.using(anio_bd).filter(trabajador=trabajador, anio=int(anio))
    establecimiento_descripcion = ""

    if len(detalles) > 0:
        detalle_codest = detalles.last().codest
        try:
            establecimiento = Establecimiento.objects.using(anio_bd).filter(codest=detalle_codest).last()
            establecimiento_descripcion = establecimiento.desest
        except Establecimiento.DoesNotExist:
            print(" No encontrado")

    return establecimiento_descripcion


def get_cargo(anio_bd, trabajador, anio):
    detalles = ConstanciaDetalle.objects.using(anio_bd).filter(trabajador=trabajador, anio=int(anio))

    cargo_descripcion = "** SIN CARGO **"

    if len(detalles) > 0:
        detalle_codcar = detalles.last().codcar if len(detalles.last().codcar) == 4 else "0" + detalles.last().codcar
        try:
            cargo = Cargo.objects.using(anio_bd).filter(codcar=detalle_codcar).last()
            if cargo:
                cargo_descripcion = cargo.descar
        except Cargo.DoesNotExist:
            print(" No encontrado")

    return cargo_descripcion
