#encoding: utf-8
from django import forms

class ReportRouterForm(forms.Form):
	
	REPORT_TYPES = (
		('HV','Visita Domiciliaria'),
		('LS','Situación Legal'),
		('SE','Estudio de Seguridad'),
	)

	report_type = forms.ChoiceField(choices=REPORT_TYPES, label=u'Tipo de reporte')
