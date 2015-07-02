#encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
from redactor.fields import RedactorField
from users.models import Role

class Requisition(models.Model):
	open_date = models.DateTimeField(auto_now=True)
	client = models.ForeignKey(User, verbose_name=u'Cliente', on_delete=models.PROTECT)
	description = RedactorField(verbose_name=u'Descripción')

	def __unicode__(self):
		return u'Requisición #'+str(self.id)

class Service(models.Model):
	name = models.CharField(max_length=60, verbose_name=u'Nombre', unique=True)
	description = RedactorField(verbose_name=u'Descripción')
	roles = models.ManyToManyField(Role, verbose_name='Cargos involucrados')

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = u'Servicio'


def get_path(instance,file):
	dir = '/'
	if instance.file_type == 'CV':
		dir = '/curriculums/'
	elif instance.file_type == 'BO':
		dir = '/orders/'
	return 'uploads/requisitions/'+str(instance.requisition.id)+dir+file

import os
class Atachment(models.Model):
	TYPES = (
		('CV','Hoja de vida'),
		('BO','Orden de Compra'),
		('RE','Resumen'),
	)
	requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
	file_type = models.CharField(max_length=2, verbose_name=u'Tipo de adjunto', choices=TYPES)
	file_resource = models.FileField(upload_to=get_path)

	def get_size(self):
		return self.file_resource.file.size

	def __unicode__(self):
		return u''+os.path.basename(self.file_resource.file.name)