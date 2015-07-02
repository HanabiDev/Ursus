from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy

from studies.models import Assignment
from django.contrib.auth.models import User

def home(request):
	assignments = Assignment.objects.filter(employee=request.user)
	return render_to_response('assigns_index.html', {'assignments':assignments}, context_instance=RequestContext(request))

def view_assign(request, assign_id):
	assign = Assignment.objects.get(id=assign_id)
	return render_to_response('assign_detail.html', {'assign':assign}, context_instance=RequestContext(request))
