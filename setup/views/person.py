# import json
#
# from django.contrib import messages
# from django.contrib.auth.models import Group
# from django.db.models.query_utils import Q
# from django.http.response import HttpResponse
# from django.urls.base import reverse_lazy
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
#
# from apps.project.models.project import Project
# from apps.util.generic_filters.views import FilteredListView
# from setup.forms.person import PersonForm, PersonListFilter, PersonChangePasswordForm, PersonChangeForm
# from setup.models.person import Person
#
#
# class PersonList(FilteredListView):
#     model = Person
#     paginate_by = 15
#     form_class = PersonListFilter
#     search_fields = ['username', 'name', 'first_name', 'last_name', 'document']
#     default_order = 'id'
#
#     def get_context_data(self, **kwargs):
#         title = "Todos los usuarios"
#         return dict(
#             super(PersonList, self).get_context_data(**kwargs), title=title)
#
#     def get_queryset(self):
#         groups = [g.id for g in Group.objects.filter(name__in=['Administrador', 'Trabajador'])]
#
#         queryset = super().get_queryset()
#         # return queryset.filter(is_staff=False).exclude(groups__in=groups).order_by('-id')
#         return queryset.filter(is_staff=False).order_by('-id')
#
#
# class PersonCreate(CreateView):
#     form_class = PersonForm
#     model = Person
#     success_url = reverse_lazy('person:list')
#
#     def form_valid(self, form):
#         self.object = form.save()
#         groups = self.request.POST.getlist("groups")
#         project = self.request.POST.getlist("project")
#
#         persona = Person.objects.get(pk=self.object.id)
#
#         if project:
#             projects = Project.objects.filter(id__in=project)
#             for p in projects:
#                 persona.project.add(p)
#                 persona.save()
#
#         if groups:
#             grupos = Group.objects.filter(id__in=groups)
#             for g in grupos:
#                 persona.groups.add(g)
#                 persona.save()
#
#         msg = "El Usuario <strong>" + str(self.request.POST['username']) + "</strong>  fue agregado correctamente"
#         messages.add_message(self.request, messages.SUCCESS, msg)
#         return super().form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         title = "Agregar Usuario"
#         return dict(
#             super(PersonCreate, self).get_context_data(**kwargs), title=title)
#
#
# class PersonUpdate(UpdateView):
#     form_class = PersonChangeForm
#     model = Person
#     success_url = reverse_lazy('person:list')
#
#     def get_context_data(self, **kwargs):
#         person = Person.objects.get(pk=self.kwargs['pk'])
#         title = "Actualizar Usuario"
#         return dict(
#             super(PersonUpdate, self).get_context_data(**kwargs), person=person, title=title)
#
#     def form_valid(self, form):
#         msg = "El Usuario <strong>" + str(
#             self.request.POST['username'] + "</strong>  fue editado correctamente")
#         messages.add_message(self.request, messages.SUCCESS, msg)
#         return super().form_valid(form)
#
#
# class UserPasswordUpdate(UpdateView):
#     form_class = PersonChangePasswordForm
#     model = Person
#     template_name = "setup/change_password.html"
#
#     def get_success_url(self):
#         return reverse_lazy('person:edit',
#                             kwargs={'pk': self.object.id})
#
#     def get_context_data(self, **kwargs):
#         user_object = Person.objects.get(pk=self.kwargs['pk'])
#         title = "Actualizar contraseña"
#
#         return dict(
#             super(UserPasswordUpdate, self).get_context_data(**kwargs), user_object=user_object, title=title)
#
#     def form_valid(self, form):
#         msg = "Contraseña actualizada del usuario: <strong>" + str(
#             self.request.POST['username'] + "</strong>")
#         messages.add_message(self.request, messages.SUCCESS, msg)
#         return super().form_valid(form)
#
#
# def PersonSerializer(person):
#     return {'id': person.id, 'first_name': person.first_name, 'last_name': person.last_name}
#
#
# def PersonSearch(request):
#     q = request.GET.get('q')
#     print(q)
#
#     list_person = Person.objects.filter(
#         Q(first_name__startswith=q) | Q(last_name__startswith=q)
#         | Q(first_name__icontains=q) | Q(last_name__icontains=q)
#         | Q(document__startswith=q) | Q(document__icontains=q))
#     list_person_ = [PersonSerializer(p) for p in list_person]
#
#     return HttpResponse(json.dumps(list_person_), content_type='application/json')
#
#
# def PersonSerializerBasic(person):
#     return {'id': person.id, 'name': person.first_name + " " + person.last_name}
#
#
# def person_all_json(request):
#     list_person = Person.objects.all()
#     list_person_ = [PersonSerializerBasic(p) for p in list_person]
#     return HttpResponse(json.dumps(list_person_), content_type='application/json')
#
#
# class PersonDelete(DeleteView):
#     model = Person
#     success_url = reverse_lazy('person:list')
