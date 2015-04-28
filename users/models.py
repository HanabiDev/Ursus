#encoding: utf-8

from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django_resized import ResizedImageField
from redactor.fields import RedactorField

GENRES = (
	('M', 'Masculino'),
	('F', 'Femenino')
)

DNI_TYPES = (
	('C', 'Cédula de Ciudadanía'),
	('E', 'Cédula de Extranjería'),
	('N', 'NIT')
)

USER_ROLES = (
    ('C', 'Cliente'),
    ('E', 'Empleado')
)

class Role(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    description = RedactorField(redactor_options={'lang':'es', 'focus':'false', 'minHeight':150, 'maxHeight':150}, verbose_name=u'Descripción')

    def __unicode__(self):
        return self.name

#Modelo para los usuarios del sitio, este modelo extiende el modelo de usuarios de Django
class SiteUser(User):
    ResizedImageField(size=[150, 150], crop=['middle', 'center'], upload_to='uploads/avatars', null=True, blank=True).contribute_to_class(User,'avatar')
    models.CharField(max_length=1, verbose_name=u'Género', choices=GENRES).contribute_to_class(User,'genre')
    models.CharField(max_length=200, verbose_name='Dirección').contribute_to_class(User,'address')
    models.CharField(max_length=9, verbose_name='Teléfono').contribute_to_class(User,'phone')
    models.CharField(max_length=12, verbose_name='Móvil').contribute_to_class(User,'mobile')
    models.CharField(max_length=200, verbose_name='Empresa').contribute_to_class(User,'company')
    models.CharField(max_length=200, verbose_name='Cargo').contribute_to_class(User,'role')
    models.CharField(max_length=1, verbose_name='Tipo de Usuario', choices=USER_ROLES).contribute_to_class(User,'type')

    models.CharField(
    	max_length=1, verbose_name='Tipo de Documento',
    	choices = DNI_TYPES
    ).contribute_to_class(User,'dni_type')

    models.CharField(
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
    ).contribute_to_class(User,'dni_number')

    def __unicode__(self):
        return self.fisrt_name + ' '+ self.last_name
    
    class Meta:
        proxy = True

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    icon = models.CharField(max_length=100)
    short = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
