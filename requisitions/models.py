#encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
from redactor.fields import RedactorField
from users.models import Role

class Requisition(models.Model):
	open_date = models.DateTimeField(auto_now=True)
	client = models.ForeignKey(User, verbose_name=u'Cliente', on_delete=models.PROTECT)
	description = RedactorField(redactor_options={'lang':'es', 'focus':'false', 'minHeight':150, 'maxHeight':150, 'plugins': ['fullscreen']}, verbose_name=u'Descripción')
	
	def __unicode__(self):
		return u'Requisición #'+str(self.id)

class Service(models.Model):
	name = models.CharField(max_length=60, verbose_name=u'Nombre', unique=True)
	description = RedactorField(redactor_options={'lang':'es', 'focus':'false', 'minHeight':150, 'maxHeight':150}, verbose_name=u'Descripción')
	roles = models.ManyToManyField(Role, verbose_name='Cargos involucrados')

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = u'Servicio'

class Atachment(models.Model):
	requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE)
	file_resource = models.FileField(upload_to='uploads/attachments')

