from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from models import ReportForm
from studies.models import Assignment
import json
from django.core.urlresolvers import reverse_lazy

# Create your views here.

def create_legal_report(request, assignment_id):
	if request.method == 'GET':
		assignment = Assignment.objects.get(id=assignment_id)
		
		if assignment.reportform_set.filter(report_type='LS').count()==0:
			candidate = assignment.study.candidate
			return render_to_response('legal_report.html', {'cand':candidate}, context_instance=RequestContext(request))
				
		return redirect(reverse_lazy('assignments:view_assign', kwargs={'assign_id':str(assignment_id)}))	
	
	if request.method == 'POST':
		fields = {}
		for field in request.POST:
			fields[field] = request.POST.get(field)
		
		report = ReportForm(
			assignment=Assignment.objects.get(id=int(assignment_id)),
			json_data=json.dumps(fields),
			report_type='LS'
		)

		report.save()