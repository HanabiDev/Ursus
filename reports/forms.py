#encoding: utf-8
from django import forms
from reports.models import ReportFile
import django.forms.widgets as widgets
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from reports.models import Candidate

REPORT_TYPES = (
	#('HV','Visita Domiciliaria'),
	('LS','Situación Jurídica'),
	('SS','Estudio de Seguridad'),
)

REPORT_TYPES_B = (
	('HV','Visita Domiciliaria'),
	('LS','Situación Jurídica'),
	('SS','Estudio de Seguridad'),
)

class ReportRouterForm(forms.Form):
	report_type = forms.ChoiceField(choices=REPORT_TYPES, label=u'Tipo de reporte')


class ReportFileForm(forms.Form):
	dni = forms.CharField(
    	max_length=30, 
    	label='Número de Documento', 
    	validators=[
            RegexValidator(
                r'^[0-9]*$',
                'Sólo dígitos',
                'Número no válido'
            ),
            MinLengthValidator(5),
            MaxLengthValidator(30),
        ]
    )
	report_file = forms.FileField(label="Archivo de reporte")
	report_type = forms.ChoiceField(label="Tipo de reporte", choices=REPORT_TYPES_B)


