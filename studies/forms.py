#encoding: utf-8
from django import forms
from models import Study
from users.models import SiteUser
from django.forms.widgets import Select

class StudyForm(forms.ModelForm):
	
	class Meta:
		model = Study
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super(StudyForm, self).__init__(*args, **kwargs)
		employees = SiteUser.objects.filter(type='E')
		emps = [(employee.id, employee.first_name+' '+employee.last_name+' ('+employee.role+')') for employee in employees]
		self.fields['employee'].choices = emps
