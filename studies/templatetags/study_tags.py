from django import template
register = template.Library()
from django.core.urlresolvers import reverse_lazy
from users.models import Notification
from django.contrib.auth.models import User

def get_employees(role):
	employees = User.objects.filter(role=role)
	return employees

register.filter('get_employees', get_employees)