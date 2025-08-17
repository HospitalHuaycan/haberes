from django.http import HttpResponseRedirect
from django.urls import reverse


def is_manager_or_admin(user):
    if user.is_superuser:
        return True
    else:
        return user.groups.filter(name='Administrador').exists()


# Custom Decorator
def teacher_required(function):
    def _function(request, *args, **kwargs):
        # if request.user.groups.filter(name='Administrador').exists():
        return HttpResponseRedirect(reverse('lot.internal:list'))
        # return function(request, *args, **kwargs)

    return _function
