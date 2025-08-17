from django.contrib import messages
from django.http import HttpResponse
from django.template import loader

from apps.remuneracion.forms.consulta import ConsultaForm
from apps.remuneracion.models.remuneracion import Remuneracion
from apps.remuneracion.models.trabajador import Trabajador
from apps.util.update_menu import update_menu


def consulta_quinta_categoria(request):
    print(" Consulta quinta categoria ")
    print(" -->>>>>>>   ")
    update_menu(request)

    template = loader.get_template('consulta_quinta_categoria.html')

    if request.POST:

        form = ConsultaForm(request.POST)
        #
        # if not request.session['anonymous']:
        #     msg = "Tiempo expirado, intente de nuevo."
        #     messages.add_message(request, messages.WARNING, msg, extra_tags='danger')
        #     return redirect(reverse('index:index'))

        # Validate the form: the captcha field will automatically
        # check the input
        if form.is_valid():

            # request.session['anonymous'] = False

            dni = form['dni'].data
            try:
                trabajador = Trabajador.objects.get(dni=dni)
                msg = "Trabajador: " + trabajador.apellidos_nombres
                messages.add_message(request, messages.SUCCESS, msg)
                remuneraciones = Remuneracion.objects.filter(trabajador=trabajador)
                human = True

                request.session['trabajador_id'] = trabajador.id

                return HttpResponse(template.render(
                    {'form': form, 'human': human, 'trabajador': trabajador, 'remuneraciones': remuneraciones},
                    request))
            except Trabajador.DoesNotExist:
                msg = "Error. Trabajador no encontrado"
                messages.add_message(request, messages.WARNING, msg, extra_tags='danger')


        else:
            msg = "Error. Datos incorrectos"
            messages.add_message(request, messages.WARNING, msg, extra_tags='danger')
            print("Error")
    else:
        form = ConsultaForm()

    return HttpResponse(template.render({'form': form}, request))


def CambiarSessionTrue(request):
    request.session['anonymous'] = True
    return HttpResponse('OK')


def CambiarSessionFalse(request):
    request.session['anonymous'] = False
    return HttpResponse('OK')
