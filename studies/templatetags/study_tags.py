from django import template
register = template.Library()
from django.core.urlresolvers import reverse_lazy
from users.models import Notification
from django.contrib.auth.models import User
from requisitions.models import Requisition

def get_employees(role):
	employees = User.objects.filter(role=role)
	return employees

def get_progress(req_id):
	req = Requisition.objects.get(id=req_id)
	studies = req.study_set.all().count()
	ended_studies = req.study_set.filter(status='F').count()
	progress = int(ended_studies*100/studies)
	if(progress >= 100):
		progress = 100
		req.status = 'T'
		req.save()
	return progress
	
import json
def get_candidate(json_data):
	data = json.loads(json_data)
	candidate = data['dni_number']
	print candidate
	return candidate

register.filter('get_employees', get_employees)
register.filter('get_candidate', get_candidate)
register.filter('get_progress', get_progress)