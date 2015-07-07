from django import template
register = template.Library()
from django.core.urlresolvers import reverse_lazy
from users.models import Notification
from django.contrib.auth.models import User

def get_employees(role):
	employees = User.objects.filter(role=role)
	return employees

import json
def get_candidate(json_data):
	data = json.loads(json_data)
	candidate = data['full_name']
	print candidate
	return candidate

register.filter('get_employees', get_employees)
register.filter('get_candidate', get_candidate)