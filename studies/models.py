#encoding: utf-8
from django.db import models
from django_resized import ResizedImageField
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from requisitions.models import Requisition, Service
from django.contrib.auth.models import User

# Create your models here.

class Candidate(models.Model):
	
	dni = models.CharField(
    	unique=True,
    	max_length=30, 
    	verbose_name='Número de Documento', 
    	validators=[
            RegexValidator(
                r'^[0-9]*$',
                'Sólo dígitos',
                'Número no válido'
            ),
            MinLengthValidator(5),
            MaxLengthValidator(30),
        ],
    )

	candidate_photo = ResizedImageField(
		size=[100, 120], crop=['middle', 'center'], 
		upload_to='uploads/avatars/candidates', 
		default='uploads/avatars/candidates/candidate.png', 
		null=False, blank=False, verbose_name=u'Foto')

	first_name = models.CharField(max_length=50, verbose_name='Nombres')
	last_name = models.CharField(max_length=50, verbose_name='Apellidos')
	phone = models.CharField(max_length=9, verbose_name='Teléfono')
	mobile = models.CharField(max_length=12, verbose_name='Móvil')
	email = models.EmailField(verbose_name='Email')
	aspired_role = models.CharField(max_length=200, verbose_name='Cargo al que aspira')
	address = models.CharField(max_length=200, verbose_name='Dirección')
	curriculum = models.FileField(upload_to='uploads/candidates/curriculums/', verbose_name='Hoja de vida')


	def __unicode__(self):
		return self.first_name + ' '+ self.last_name

class Study(models.Model):
	requisition = models.ForeignKey(Requisition, verbose_name=u'Requisición', on_delete=models.CASCADE)
	candidate = models.ForeignKey(Candidate, verbose_name=u'Candidato')
	creation_date = models.DateTimeField(auto_now=True)
	service = models.ForeignKey(Service, verbose_name=u'Servicio')

class Assignment(models.Model):
	study = models.ForeignKey(Study, verbose_name=u'Estudio')
	employee = models.ForeignKey(User, verbose_name=u'Empleado')
	asignment_date = models.DateTimeField(auto_now=True)

