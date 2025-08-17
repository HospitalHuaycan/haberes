activate_this = 'C:/Users/Administrador.WIN-6SDDSK51A35/Envs/remuneraciones/Scripts/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))
exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('C:/Users/Administrador.WIN-6SDDSK51A35/Envs/remuneraciones/Lib/site-packages')


# Add the app's directory to the PYTHONPATH
sys.path.append('C:/Users/Administrador.WIN-6SDDSK51A35/Documents/Apps/diris-remuneraciones')
sys.path.append('C:/Users/Administrador.WIN-6SDDSK51A35/Documents/Apps/diris-remuneraciones/main')

os.environ['DJANGO_SETTINGS_MODULE'] = 'main.settings.prod_windows'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings.prod_windows")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()