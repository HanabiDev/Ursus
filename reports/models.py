#encoding: utf-8
from django.db import models
from studies.models import Study

# Create your models here.

REPORT_CHOICES = (
	('HV','Visita Domiciliaria'),
	('LS','Situación Jurídica'),
	('CV','Estudio de Seguridad'),
)

class Candidate(models.Model):
	dni_number = models.CharField(max_length=20)

class ReportForm(models.Model):
	study = models.ForeignKey(Study)
	#candidate = models.ForeignKey(Candidate)
	json_data = models.TextField()
	report_type = models.CharField(max_length=2, choices=REPORT_CHOICES)
	locked = models.BooleanField(default=False)
	verified = models.BooleanField(default=False)

