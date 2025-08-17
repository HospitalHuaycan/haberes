# from django.contrib.auth.decorators import login_required
# from django.urls import path
#
# from setup.views.person import PersonList, PersonCreate, PersonUpdate, PersonDelete, PersonSearch, person_all_json, \
#     UserPasswordUpdate
#
# app_name = 'person'
#
# urlpatterns = [
#     path('list', login_required(PersonList.as_view()), name='list'),
#     path('new', login_required(PersonCreate.as_view()), name='new'),
#     path('edit/<pk>', login_required(PersonUpdate.as_view()), name='edit'),
#     path('delete/<pk>', login_required(PersonDelete.as_view()), name='delete'),
#     path('search', login_required(PersonSearch), name='search'),
#     path('all-json', login_required(person_all_json), name='all-json'),
#     path('password/<pk>', login_required(UserPasswordUpdate.as_view()), name='password'),
# ]
