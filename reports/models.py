#encoding: utf-8
from django.db import models
from studies.models import Assignment

# Create your models here.

REPORT_CHOICES = (
	('HV','Visita Domiciliaria'),
	('LS','Situación Legal'),
	('CV','Estudio de Seguridad'),
)

class ReportForm(models.Model):
	assignment = models.ForeignKey(Assignment)
	json_data = models.TextField()
	report_type = models.CharField(max_length=2, choices=REPORT_CHOICES)
	verified = models.BooleanField(default=False)

