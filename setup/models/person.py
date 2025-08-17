# from datetime import date
#
# from django.contrib.auth.models import AbstractUser
# from django.core.validators import RegexValidator
# from django.db import models
# from django.utils.translation import gettext_lazy as _
#
# from apps.project.models.project import Project
#
# TYPES = (
#     ('DNI', 'DNI'),
#     ('PASSPORD', 'PASAPORTE'),
# )
#
# DEGRESS = (
#     (0, 'SIN ESTUDIOS'),
#     (1, 'PRIMARIA COMPLETA'),
#     (2, 'PRIMARIA INCOMPLETA '),
#     (3, 'SECUNDARIA COMPLETA'),
#     (04, 'SECUNDARIA INCOMPLETA'),
#     (5, 'ESTUDIOS SUPERIORES'),
# )
#
# CIVIL_STATUS = (
#     (0, 'SOLTERO'),
#     (1, 'CASADO'),
#     (2, 'DIVORCIADO'),
#     (3, 'VIUDO'),
# )
#
# SEXS = (
#     (0, 'FEMENINO'),
#     (1, 'MASCULINO'),
# )
#
#
# def calculate_age(born):
#     today = date.today()
#     return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
#
#
# class Person(AbstractUser):
#     document = models.CharField(_('número de DNI'), max_length=12, unique=True, validators=[
#         RegexValidator(regex='^.{8}$', message=_('Tiene que ingresa 8 dígitos'), code='nomatch')])
#     name = models.CharField(_('nombres'), max_length=30)
#     first_name = models.CharField(_('apellido paterno'), max_length=50)
#     last_name = models.CharField(_('apellidos materno'), max_length=50)
#     phone = models.IntegerField(_('número de celular'), null=True, blank=True, validators=[
#         RegexValidator(regex='^.{9}$', message=_('tiene que ingresa 9 dígitos.'), code='nomatch')])
#     address = models.CharField(_('dirección'), max_length=150, null=True, blank=True)
#     project = models.ManyToManyField(Project, verbose_name='Proyectos', blank=True)
#
#     def get_full_name(self):
#         return self.name + " " + self.first_name + " " + self.last_name
#
#     def __str__(self):
#         return " %s  %s " % (
#             self.first_name, self.last_name)
#
#     class Meta:
#         verbose_name = _('Persona')
#         verbose_name_plural = _('Personas')
