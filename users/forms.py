#encoding:utf-8
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm
from django.contrib.auth.models import User, Group
from django import forms
from models import *
from django.forms.extras.widgets import Select
from django.forms.widgets import TextInput

class UserAddForm(UserCreationForm):

	def __init__(self, *args, **kwargs):
		super(UserCreationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Usuario"
		self.fields['password1'].label = "Contraseña"
		self.fields['password2'].label = "Confirmar contraseña"


class UserEditForm(UserChangeForm):
	def __init__(self, *args, **kwargs):
		super(UserChangeForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Usuario"
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['email'].required = True

		if kwargs.get('initial'):
			self.fields['company'].value = 'HANABI S.A.S.'
			self.fields['company'].widget = TextInput(attrs={'readonly':'readonly'})
			CHOICES = Role.objects.all()
			choices = [(x.name, x.name) for x in CHOICES ]
			self.fields['role'].widget = Select(choices=[('---------','---------')]+choices)

	class Meta:
		model = SiteUser
		fields = [
			'first_name', 'last_name', 'username', 'email', 'avatar', 
			'genre', 'dni_type', 'dni_number', 'address', 'phone', 
			'mobile', 'type', 'role', 'company', 'is_active', 'is_superuser',
			'is_staff', 'password'
		]

		labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
            'is_superuser': 'Superusuario',
            'is_active': 'Activo',
            'user_permissions': 'Permisos',
            'groups': 'Grupos',
            'password': '',
            'avatar': 'Imágen de perfil',
            'is_staff': 'Administrador'
        }


class NewProfileForm(UserChangeForm):
	def __init__(self, *args, **kwargs):
		super(UserChangeForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = "Usuario"
		self.fields['first_name'].required = True
		self.fields['last_name'].required = True
		self.fields['email'].required = True


	class Meta:
		
		model = SiteUser
		fields = [
			'first_name', 'last_name', 'username', 'email',
			'genre', 'dni_type', 'dni_number', 'address', 'phone', 
			'mobile', 'role', 'company', 'password'
		]

		labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
            'is_superuser': 'Superusuario',
            'is_active': 'Activo',
            'user_permissions': 'Permisos',
            'groups': 'Grupos',
            'password': '',
            'avatar': 'Imágen de perfil',
            'is_staff': 'Administrador'
        }

class RoleForm(forms.ModelForm):
	class Meta:
		model = Role
		fields = '__all__'
	