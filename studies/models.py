#encoding: utf-8
from django.db import models
from django_resized import ResizedImageField
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from requisitions.models import Requisition, Service
from django.contrib.auth.models import User
from redactor.fields import RedactorField

def get_path(instance,file):
	return 'uploads/studies/'+str(instance.id)+file

class Study(models.Model):
	creation_date = models.DateTimeField(auto_now=True)
	requisition = models.ForeignKey(Requisition, verbose_name=u'Requisición', on_delete=models.CASCADE)
	service = models.ForeignKey(Service, verbose_name=u'Servicio')
	employee = models.ForeignKey(User, verbose_name=u'Empleado')
	limit_date = models.DateTimeField(verbose_name=u'Fecha de Entrega')
	description = RedactorField(verbose_name=u'Descripción')
	attachment = models.FileField(upload_to=get_path, verbose_name=u'Archivos adjuntos')


