from django import forms
from models import Requisition, Service
from django.contrib.auth.models import User

class AddRequisitionForm(forms.ModelForm):
	class Meta:
		model = Requisition
		fields = '__all__'
		exclude = ['status']
		
	def __init__(self, *args, **kwargs):
		super(AddRequisitionForm, self).__init__(*args, **kwargs)
		
		if kwargs.get('initial'):
			client = kwargs.get('initial').get('client')
			self.fields['client'].choices = [(client.id, client.first_name+' '+client.last_name)]
		else:	
			excluded = User.objects.filter(type='C')
			self.fields['client'].choices = [(p.id, p.first_name+' '+p.last_name,) for p in excluded]
			self.fields['client'].choices = [('', '---------')]+self.fields['client'].choices

class ServiceForm(forms.ModelForm):
	class Meta:
		model = Service
		
		fields = '__all__'
 
