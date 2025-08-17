from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User, Permission
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse
from django.views.generic import TemplateView

from apps.concepto.models.concepto import Concepto
from apps.constancia.models.anio import Anio
from apps.constancia.models.constancia import Constancia
from apps.constancia.models.constancia_detalle import MESES, ConstanciaDetalle
from apps.index.forms.consulta import ConsultaForm
from apps.trabajador.models.trabajador import Trabajador
from setup.models.menu import Menu, GroupMenu

ERROR_404_TEMPLATE_NAME = '404.html'
ERROR_403_TEMPLATE_NAME = '403.html'
ERROR_400_TEMPLATE_NAME = '400.html'
ERROR_500_TEMPLATE_NAME = '500.html'


class MenuItem(object):
    def __init__(self, id, name, url, icon):
        self.id = id
        self.name = name
        self.url = url
        self.icon = icon

    def serialize(self):
        return self.__dict__


def get_menu(user):
    group_list = list(col["id"] for col in Group.objects.values("id")
                      .filter(Q(user__id=user.id)).distinct())
    permission_list = list(col["id"] for col in Permission.objects
                           .values("id")
                           .filter(Q(group__in=group_list) | Q(user__id=user.id)).distinct())

    if user.is_superuser:
        menu_childrens_t = list(
            col["id"] for col in
            Menu.objects.values("id").all().order_by("id"))
    else:
        menu_childrens_t = list(
            col["menus"] for col in
            GroupMenu.objects.values("menus").filter(Q(group__in=group_list)).order_by("id"))

    menu_parents_parent = Menu.objects.filter(id__in=menu_childrens_t). \
        annotate(childrenss_num=Count('childrens')).filter(childrenss_num=0)

    menu_parents = Menu.objects.filter(childrens__in=menu_childrens_t).order_by("id").distinct()

    # list_menu = []
    menu_json = []
    menus_only_childrens = []

    for i in menu_parents:
        # childrens = []
        childrens_json = []

        for j in i.childrens.all():
            if j.id in menu_childrens_t:
                # childrens.append(j)
                childrens_json.append(MenuItem(j.id, j.name, j.url, j.icon).serialize())
                menus_only_childrens.append(j.id)
                menus_only_childrens.append(i.id)
        # list_menu.append({'menu': i, 'childrens': childrens})
        menu_json.append({'menu': MenuItem(i.id, i.name, i.url, i.icon).serialize(), 'childrens': childrens_json})

    menu_parents_final = menu_parents_parent.exclude(id__in=menus_only_childrens)

    for i in menu_parents_final:
        menu_json.append({'menu': MenuItem(i.id, i.name, i.url, i.icon).serialize(), 'childrens': []})

    return menu_json


def consulta_contancia(request):
    template = loader.get_template('consulta_contancia.html')
    human = False
    if request.POST:
        form = ConsultaForm(request.POST)

        if form.is_valid():

            dni = form['dni'].data

            try:
                trabajador = Trabajador.objects.get(dni=dni)
                msg = "Trabajador: " + trabajador.get_full_name()
                messages.add_message(request, messages.SUCCESS, msg)
                constancia = Constancia.objects.filter(trabajador=trabajador).last()

                print(" Constancia -->> ")
                print(constancia)

                constancia_ = Constancia.objects.get(trabajador=trabajador)

                # list_constancia_detalle = constancia_.constanciadetalle_set.all()
                conceptos = constancia_.constanciadetalle_set.values_list('concepto').order_by('concepto').distinct()
                concepto_ingresos_list = conceptos.filter(concepto__startswith='1')
                concepto_descuentos_list = conceptos.filter(concepto__startswith='2')
                concepto_aportes_list = conceptos.filter(concepto__startswith='3')

                print(concepto_ingresos_list)
                print(concepto_descuentos_list)
                print(concepto_aportes_list)

                monto_ingreso_list = []
                monto_ingreso_list_total = ["TOTAL", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                                            0.00, 0.00]

                for i in concepto_ingresos_list:
                    monto_ingreso_mes = [i[0]]
                    monto_count = Decimal(0.00)
                    for j in MESES:
                        try:
                            detalle = ConstanciaDetalle.objects.get(constancia=constancia, mes=j[0], concepto=i[0])
                            # if j[0] == 1:
                            concepto = Concepto.objects.filter(codcon=detalle.concepto, mes=j[0], anio=2020).order_by(
                                'tiparch').last()
                            # monto_ingreso_mes[0] = concepto.abrcon + " - " + concepto.codcon
                            monto_ingreso_mes[0] = concepto.abrcon
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
                            detalle = ConstanciaDetalle.objects.get(constancia=constancia, mes=j[0], concepto=i[0])
                            # if j[0] == 1:
                            concepto = Concepto.objects.filter(codcon=detalle.concepto, mes=j[0], anio=2020).order_by(
                                'tiparch').last()
                            monto_ingreso_mes[0] = concepto.abrcon
                            monto_ingreso_mes.append(detalle)
                            monto_count += detalle.monto
                            monto_descuento_list_total[j[0]] = Decimal(monto_descuento_list_total[j[0]]) + detalle.monto
                        except ConstanciaDetalle.DoesNotExist:
                            monto_ingreso_mes.append(" ")
                    monto_ingreso_mes.append(monto_count)
                    monto_descuento_list_total[13] = Decimal(monto_descuento_list_total[13]) + monto_count
                    monto_descuento_list.append(monto_ingreso_mes)

                monto_liquido_list_total = ["TOTAL", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                                            0.00, 0.00]
                for i in range(1, 14):
                    monto_liquido_list_total[i] = monto_ingreso_list_total[i] - monto_descuento_list_total[i]

                monto_aportaciones_list = []
                monto_aportaciones_list_total = ["TOTAL", 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00,
                                                 0.00,
                                                 0.00, 0.00]
                for i in concepto_aportes_list:
                    monto_ingreso_mes = [i[0]]
                    monto_count = Decimal(0.00)
                    for j in MESES:
                        try:
                            detalle = ConstanciaDetalle.objects.get(constancia=constancia, mes=j[0], concepto=i[0])
                            # if j[0] == 1:
                            concepto = Concepto.objects.filter(codcon=detalle.concepto, mes=j[0], anio=2020).order_by(
                                'tiparch').last()
                            monto_ingreso_mes[0] = concepto.abrcon
                            monto_ingreso_mes.append(detalle)
                            monto_count += detalle.monto
                            monto_aportaciones_list_total[j[0]] = Decimal(
                                monto_aportaciones_list_total[j[0]]) + detalle.monto
                        except ConstanciaDetalle.DoesNotExist:
                            monto_ingreso_mes.append(" ")
                    monto_ingreso_mes.append(monto_count)
                    monto_aportaciones_list_total[13] = Decimal(monto_aportaciones_list_total[13]) + monto_count
                    monto_aportaciones_list.append(monto_ingreso_mes)

                human = True

                request.session['trabajador_id'] = trabajador.id

                return HttpResponse(template.render(
                    {
                        'form': form,
                        'human': human,
                        'trabajador': trabajador,
                        'monto_ingreso_list': monto_ingreso_list,
                        'monto_descuento_list': monto_descuento_list,
                        'monto_ingreso_list_total': monto_ingreso_list_total,
                        'monto_descuento_list_total': monto_descuento_list_total,
                        'monto_liquido_list_total': monto_liquido_list_total,
                        'monto_aportaciones_list': monto_aportaciones_list,
                        'monto_aportaciones_list_total': monto_aportaciones_list_total,
                    }, request))

            except Trabajador.DoesNotExist:
                msg = "Error. Trabajador no encontrado"
                messages.add_message(request, messages.WARNING, msg, extra_tags='danger')

        else:
            msg = "Error. Datos incorrectos"
            messages.add_message(request, messages.WARNING, msg, extra_tags='danger')
            print("Error")
    else:
        form = ConsultaForm()

    return HttpResponse(template.render({'form': form, 'human': human}, request))


def index(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render({}, request))


class AnioItem(object):
    def __init__(self, id, anio):
        self.id = id
        self.anio = anio

    def serialize(self):
        return self.__dict__


class Dashboard(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        self.request.session["anio_list"] = [AnioItem(j.id, j.anio).serialize() for j in Anio.objects.all()]

        self.request.session['menu_parent'] = 1
        # self.request.session['menu_children'] = 2

        try:
            anio = Anio.objects.get(anio=2020)
        except Anio.DoesNotExist:
            anio = Anio.objects.all().last()

        self.request.session["anio"] = 0
        if anio.anio == 2020:
            self.request.session["anio_bd"] = 'default'
        else:
            self.request.session["anio_bd"] = 'haberes_' + str(anio.anio)

        return dict(super(Dashboard, self).get_context_data(**kwargs))


def login_view(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        try:
            user_active = User.objects.get(username=username)
            if not user_active.is_active:
                msg = "Cuenta suspendida, contacte con el administrador"
                messages.add_message(request, messages.WARNING, msg, extra_tags='danger')
                return redirect(reverse('index:index'))

        except User.DoesNotExist:
            msg = "Datos de acceso incorrectos"
            messages.add_message(request, messages.WARNING, msg)
            return redirect(reverse('index:index'))

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)

                msg = "Bienvenido: "
                messages.add_message(request, messages.SUCCESS, msg)

                request.session["menu"] = get_menu(request.user)
                request.session["menu_manager"] = 'active'
                request.session["menu_patient"] = ''

                request.session['menu_parent'] = 0
                request.session["project"] = 0
                return redirect(reverse('index:dashboard'))

            else:
                msg = "Cuenta suspendida, contacte con el administrador"
                messages.add_message(request, messages.WARNING, msg)
                return redirect(reverse('index:index'))
        else:
            msg = "Datos de acceso incorrectos"
            messages.add_message(request, messages.WARNING, msg)
            return redirect(reverse('index:index'))
    else:
        msg = "Operación no soportada"
        messages.add_message(request, messages.WARNING, msg)
        return redirect(reverse('index:index'))


def logout_view(request):
    if request.user.is_authenticated:
        request.session['menu_children'] = 0
        request.session['menu_parent'] = 0
        logout(request)
    return redirect(reverse('index:index'))


def change_anio(request):
    if request.user.is_authenticated:
        anio_id = request.GET.get('anio_id', '0')

        try:
            anio = Anio.objects.get(pk=int(anio_id))
            msg = "Cambiando al año: " + str(anio.anio)
            messages.add_message(request, messages.INFO, msg)
            if anio.anio == 2020:
                request.session["anio_bd"] = 'default'
            else:
                request.session["anio_bd"] = 'haberes_' + str(anio.anio)
        except Anio.DoesNotExist:
            print("Error")

        # if request.user.is_superuser:
        if anio_id != '0':
            request.session["anio"] = int(anio_id)

        else:
            print(" No es super usuario ->> ")
        # return redirect(reverse('constancia:list')+ "?anio_id=" + anio_id)
        return redirect(reverse('constancia:list'))
