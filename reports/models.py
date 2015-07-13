#encoding: utf-8
from django.db import models
from studies.models import Study

# Create your models here.

REPORT_CHOICES = (
	('HV','Visita Domiciliaria'),
	('LS','Situación Jurídica'),
	('SS','Estudio de Seguridad'),
)

def get_path(instance,file):
	return 'uploads/reports/'+str(instance.candidate.dni_number)+"/"+file


class Candidate(models.Model):
	dni_number = models.CharField(max_length=20)
	class Meta:
		def __unicode__():
			return dni_number

class ReportForm(models.Model):
	study = models.ForeignKey(Study)
	candidate = models.ForeignKey(Candidate)
	json_data = models.TextField()
	report_type = models.CharField(max_length=2, choices=REPORT_CHOICES)
	locked = models.BooleanField(default=False)
	verified = models.BooleanField(default=False)

class ReportFile(models.Model):
	study = models.ForeignKey(Study)
	candidate = models.ForeignKey(Candidate, verbose_name=u'Cédula candidato')
	report_file = models.FileField(upload_to=get_path, verbose_name=u'Archivo')
	report_type = models.CharField(max_length=2, choices=REPORT_CHOICES, verbose_name=u'Tipo de reporte')
	locked = models.BooleanField(default=False)
	verified = models.BooleanField(default=False)

