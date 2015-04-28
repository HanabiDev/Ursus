from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy

from csv_importer import import_data
from forms import CandidateForm, StudyForm
from models import Requisition
from models import Study, Candidate, Assignment
from django.contrib.auth.models import User

def home(request):
	if request.user.is_superuser or request.user.is_staff:
		studies = Study.objects.all()
	else:
		studies = Study.objects.filter(requisition__client=request.user)
	
	return render_to_response('studies_index.html', {'studies':studies}, context_instance=RequestContext(request))

def create_studies(request):
	if request.method == 'GET':
		return render_to_response('massive-load.html', request.session, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		if request.FILES:
			datafile = request.FILES.get('csv_file')
			import_data(datafile)
			
			return redirect(reverse_lazy('reqs:home'))

		return render_to_response('massive-load.html', {'errors':'Este campo es obligatorio'}, context_instance=RequestContext(request))		

def create_study(request, req_id):
	if request.method == 'GET':
		form = CandidateForm()
		return render_to_response('study.html', {'id':req_id,'form':form}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		form = CandidateForm(request.POST)
		if form.is_valid():
			
			requisition = Requisition.objects.get(id=req_id)
			candidate = form.save()
			
			if request.FILES:
				candidate.candidate_photo = request.FILES.get('avatar')
			
			candidate.save()

			study = Study(requisition=requisition, candidate=candidate)
			study.save()

			return redirect(reverse_lazy('reqs:view_req', kwargs={'req_id':str(req_id)}))

		return render_to_response('study.html', {'id':req_id,'form':form}, context_instance=RequestContext(request))

def view_study(request, study_id):
	study = Study.objects.get(id=study_id)
	return render_to_response('study_detail.html', {'study':study}, context_instance=RequestContext(request))

def edit_study(request, study_id):
	study = Study.objects.get(id=study_id)

	if request.method == 'GET':
		form = StudyForm(instance=study)
		return render_to_response('edit_study.html', {'r_id':study.requisition.id, 'id':study_id,'form':form, 'editing':True}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		form = StudyForm(request.POST, instance=study)
		if form.is_valid():
			study = form.save()
			return redirect(reverse_lazy('studies:view_study', kwargs={'study_id':str(study_id)}))

		return render_to_response('edit_study.html', {'r_id':study.requisition.id, 'id':study_id,'form':form, 'editing':True}, context_instance=RequestContext(request))

def assign_employees(request, study_id):
	study = Study.objects.get(id=study_id)
		
	if request.method == 'GET':
		roles = study.service.roles.all()
		return render_to_response('assign_employees.html', {'id':study_id, 'roles':roles}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		study.assignment_set.all().delete()

		roles = study.service.roles.all()

		for role in roles:
			employee_id = request.POST.get('role_'+str(role.id)+'_employees')
			employee = User.objects.get(id=employee_id)
			
			assignment = Assignment(
				study=study,
				employee=employee
			)

			assignment.save()

		return redirect(reverse_lazy('studies:view_study', kwargs={'study_id':str(study_id)}))

