#encoding: utf-8
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy

from requisitions.models import Service
from requisitions.forms import ServiceForm
from users.models import Role
from users.forms import RoleForm

# Create your views here.
def home(request):
	return render_to_response('settings.html', request.session, context_instance=RequestContext(request))

def index_services(request):
	services = Service.objects.all()
	return render_to_response('services_index.html', {'services':services}, context_instance=RequestContext(request))

def create_service(request):
	if request.method == 'GET':
		form = ServiceForm()
		return render_to_response('service.html', {'form':form}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		form = ServiceForm(request.POST)
		if form.is_valid():
			service = form.save()
			return redirect(reverse_lazy('settings:services'))

	return render_to_response('service.html', {'form':form}, context_instance=RequestContext(request))

def edit_service(request, service_id):
	service = Service.objects.get(id=service_id)
	
	if request.method == 'GET':
		form = ServiceForm(instance=service)
		return render_to_response('service.html', {'form':form, 'editing':True, 'service_id':service_id}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		form = ServiceForm(request.POST, instance=service)
		if form.is_valid():
			service = form.save()
			return redirect(reverse_lazy('settings:services'))

	return render_to_response('service.html', {'form':form, 'editing':True}, context_instance=RequestContext(request))

def delete_service(request, service_id):
	service = Service.objects.get(id=service_id)
	service.delete()
	return redirect(reverse_lazy('settings:services'))

def index_roles(request):
	roles = Role.objects.all()
	return render_to_response('roles_index.html', {'roles':roles}, context_instance=RequestContext(request))

def create_role(request):
	if request.method == 'GET':
		form = RoleForm()
		return render_to_response('role.html', {'form':form}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		form = RoleForm(request.POST)
		if form.is_valid():
			role = form.save()
			return redirect(reverse_lazy('settings:roles'))

	return render_to_response('role.html', {'form':form}, context_instance=RequestContext(request))

def edit_role(request, role_id):
	role = Role.objects.get(id=role_id)
	
	if request.method == 'GET':
		form = RoleForm(instance=role)
		return render_to_response('role.html', {'form':form, 'editing':True}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		form = RoleForm(request.POST, instance=role)
		if form.is_valid():
			role = form.save()
			return redirect(reverse_lazy('settings:roles'))

	return render_to_response('role.html', {'form':form, 'editing':True}, context_instance=RequestContext(request))

def delete_role(request, role_id):
	role = Role.objects.get(id=role_id)
	role.delete()
	return redirect(reverse_lazy('settings:roles'))
