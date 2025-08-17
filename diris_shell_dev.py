# import os
#
# os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings.dev'
#
# from django.core.wsgi import get_wsgi_application
#
# application = get_wsgi_application()

from apps.load_data.load_establecimientos import load_establecimiento
from apps.load_data.load_cargos import load_cargos
from apps.load_data.load_concepto import load_concepto
from apps.load_data.load_constancia import load_constancia
from apps.load_data import load_plaza
from apps.load_data import load_trabajador


# load_establecimiento(2021)
# load_cargos(2021)
# load_concepto(7, 2021)
# load_constancia(7, 2021)
