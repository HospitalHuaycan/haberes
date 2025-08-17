"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('', include('apps.index.url')),
                  # path('captcha/', include('captcha.urls')),

                  path('accounts/login/', include('apps.index.url')),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('manager/', admin.site.urls),
                  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                  path('constancia/', include('apps.constancia.url')),

                  # path('api/user/', include('apps.configuracion_login.url.user')),
                  # path('api/configuracion-login/', include(router_configuracion_login.urls)),
                  # path('localizations/country/', include('apps.localizations.urls.country')),
                  # path('localizations/department/', include('apps.localizations.urls.department')),
                  # path('localizations/province/', include('apps.localizations.urls.province')),
                  # path('localizations/district/', include('apps.localizations.urls.district')),

                  path('remuneracion/', include('apps.remuneracion.url')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
