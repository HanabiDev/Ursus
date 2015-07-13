#encoding: utf-8
from django.shortcuts import render_to_response, redirect, HttpResponse
from django.template import RequestContext
from models import ReportForm
from users.models import SiteUser
from requisitions.models import Requisition
from studies.models import Study
import json
from django.core.urlresolvers import reverse_lazy
import os
from users.models import Notification
from reports.models import Candidate, ReportFile
from reports.forms import ReportRouterForm, ReportFileForm

# Create your views here.

def report_router(request, study_id):
	if request.method == 'GET':
		form = ReportRouterForm()
		return render_to_response('report_router.html', {'form':form}, context_instance=RequestContext(request))
	if request.method == 'POST':
		 form = ReportRouterForm(request.POST)
		 if form.is_valid():
		 	report_type = request.POST.get('report_type')

		 	if report_type == 'HV':
		 		return None
	 		elif report_type == 'LS':
	 			return redirect(reverse_lazy('reports:new_legal_report', args=(study_id,)))
 			elif report_type == 'SE':
 				return redirect(reverse_lazy('reports:new_verif_report', args=(study_id,)))

def create_legal_report(request, study_id):
	if request.method == 'GET':
		return render_to_response('legal_report.html', context_instance=RequestContext(request))
	
	if request.method == 'POST':
		fields = {}
		for field in request.POST:
			fields[field] = request.POST.get(field)

		candidate = Candidate.objects.get_or_create(dni_number=fields['dni_number'])[0]
		
		report = ReportForm.objects.update_or_create(
			study=Study.objects.get(id=study_id),
			candidate=candidate,
			report_type='LS'
		)[0]

		report.json_data = json.dumps(fields)
		

		report.save()

		return redirect(reverse_lazy('studies:view_study', kwargs={'study_id':str(study_id)}))

def create_verification_report(request, study_id):
	if request.method == 'GET':
		return render_to_response('verification_report.html', context_instance=RequestContext(request))
	
	if request.method == 'POST':
		fields = {}
		for field in request.POST:
			fields[field] = request.POST.get(field)
		
		report = ReportForm(
			study=Study.objects.get(id=study_id),
			json_data=json.dumps(fields),
			report_type='CV'
		)
		report.save()

		return redirect(reverse_lazy('studies:view_study', kwargs={'study_id':str(study_id)}))

from easy_pdf.rendering import render_to_pdf_response
def view_report(request, report_id):
	report = ReportForm.objects.get(id=report_id)
	
	if request.method == 'GET':
		data = json.loads(report.json_data)
		res_path = os.path.abspath(os.path.dirname(__file__)+"../../static/")
		return render_to_pdf_response(request, 'report.html', {'report':report, 'data':data, 'res_path':res_path})
		#return render_to_response('report.html', {'report':report, 'data':data, 'res_path':res_path})

def edit_report(request, report_id):

	report = ReportForm.objects.get(id=report_id)
	data = json.loads(report.json_data)

	if request.method == 'GET':
		if report.report_type == 'HV':
			return None
		elif report.report_type == 'LS':
			return render_to_response('legal_report.html', {'data':data}, context_instance=RequestContext(request))
		elif report.report_type == 'SE':
			return None

	if request.method == 'POST':
		fields = {}
		for field in request.POST:
			fields[field] = request.POST.get(field)
		
		report.json_data=json.dumps(fields)
		report.save()

		return redirect(reverse_lazy('studies:view_study', kwargs={'study_id':str(report.study_id)}))

def lock_report(request, report_id):
	report = ReportForm.objects.get(id=report_id)
	study_id = report.study.id
	report.locked = True
	report.save()
	notificate_report(request.user, study_id)

	return redirect(reverse_lazy('studies:view_study', args=(study_id,)))

def unlock_report(request, report_id):
	report = ReportForm.objects.get(id=report_id)
	study_id = report.study.id
	report.locked = False
	report.save()
	return redirect(reverse_lazy('studies:view_study', args=(study_id,)))

def check_report(request, report_id):
	report = ReportForm.objects.get(id=report_id)
	study_id = report.study.id
	report.verified = True
	report.save()
	return redirect(reverse_lazy('studies:view_study', args=(study_id,)))

def delete_report(request, report_id):
	report = ReportForm.objects.get(id=report_id)
	study_id = report.study.id
	report.delete()
	return redirect(reverse_lazy('studies:view_study', args=(study_id,)))







def upload_report(request, study_id):
	if request.method == 'GET':
		form = ReportFileForm()
		return render_to_response('upload_report.html', {'form':form, 'id':study_id}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		form = ReportFileForm(request.POST, request.FILES)
	
		if form.is_valid():
			dni = form.cleaned_data['dni']
			candidate = Candidate.objects.get_or_create(dni_number=dni)[0]
			study = Study.objects.get(id=study_id)
			rep_type = form.cleaned_data['report_type']
			rep_file = form.cleaned_data['report_file']


			new_report = ReportFile.objects.update_or_create(
				candidate=candidate,
				report_type=rep_type,
				study=study
			)[0]
			new_report.study = study
			new_report.report_file = rep_file
			new_report.save()

			update_study_status(study)

			return redirect(reverse_lazy('studies:view_study', kwargs={'study_id':str(study_id)}))
			
		return render_to_response('upload_report.html', {'form':form}, context_instance=RequestContext(request))

def edit_upload_report(request, ureport_id):
	report = ReportFile.objects.get(id=ureport_id)

	if request.method == 'GET':	
		form = ReportFileForm(initial={
			'report_type':report.report_type,
			'report_file':report.report_file,
			'dni':report.candidate.dni_number
		})
		return render_to_response('upload_report.html', {'form':form, 'editing':True, 'id':report.study.id}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		if request.FILES:
			form = ReportFileForm(request.POST, request.FILES)
		else:

			form = ReportFileForm(request.POST, {'report_file':report.report_file})
			
			print form.fields['report_file']


		if form.is_valid():
			dni = form.cleaned_data['dni']
			candidate = Candidate.objects.get_or_create(dni_number=dni)[0]
			study = Study.objects.get(id=report.study.id)
			rep_type = form.cleaned_data['report_type']
			rep_file = form.cleaned_data['report_file']

			report.candidate=candidate
			report.study = study
			report.report_type=rep_type
			report.report_file = rep_file
			
			report.save()
			update_study_status(study)
			join_reports(request, dni)

			return redirect(reverse_lazy('studies:view_study', kwargs={'study_id':str(report.study.id)}))
			
		return render_to_response('upload_report.html', {'form':form, 'editing':True, 'id':report.study.id}, context_instance=RequestContext(request))

def lock_upload_report(request, report_id):
	report = ReportFile.objects.get(id=report_id)
	study_id = report.study.id
	report.locked = True
	report.save()
	notificate_report(request.user, study_id)
	update_study_status(report.study)

	return redirect(reverse_lazy('studies:view_study', args=(study_id,)))

def unlock_upload_report(request, report_id):
	report = ReportFile.objects.get(id=report_id)
	study_id = report.study.id
	report.locked = False
	report.save()
	update_study_status(report.study)

	return redirect(reverse_lazy('studies:view_study', args=(study_id,)))

def check_upload_report(request, report_id):
	report = ReportFile.objects.get(id=report_id)
	study_id = report.study.id
	report.verified = True
	report.save()
	update_study_status(report.study)

	return redirect(reverse_lazy('studies:view_study', args=(study_id,)))

def delete_upload_report(request, report_id):
	report = ReportFile.objects.get(id=report_id)
	study_id = report.study.id
	report.delete()
	update_study_status(report.study)

	return redirect(reverse_lazy('studies:view_study', args=(study_id,)))


def search(request):
	if request.method == 'GET':
		reqs = []
		if request.user.is_superuser or request.user.is_staff:
			reqs = Requisition.objects.all()
		else:
			reqs = Requisition.objects.filter(client=request.user)
		
		return render_to_response('search.html', {'reqs':reqs}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		reports = []
		dni = request.POST.get('dni')
		join_reports(request, dni)
		
		try:
			reports = ReportFile.objects.filter(candidate__dni_number=dni, verified=True).order_by('report_type')
		except Exception, e:
			print e
		return render_to_response('search_results.html', {'reps':reports, 'dni':dni}, context_instance=RequestContext(request))

def search_by_req(request, req_id):
	
	reports = []
	if request.method == 'GET':
		reports = ReportFile.objects.filter(study__requisition_id=req_id, verified=True).values_list('candidate_id')
		candidates = Candidate.objects.filter(id__in=reports)

		return render_to_response('search_results.html', {'candidates':candidates, 'req_id':req_id}, context_instance=RequestContext(request))
		
	if request.method == 'POST':
		return None

from PyPDF2 import PdfFileMerger, PdfFileReader
from django.conf import settings
def join_reports(request, dni):
	path = os.path.join(settings.MEDIA_ROOT,"uploads/reports/",dni)
	filename = path+"/reporte-"+dni+".pdf"
	
	reports = ReportFile.objects.filter(candidate__dni_number=dni, verified=True).order_by('report_type')
	merger = PdfFileMerger()
	for report in reports:
		report_file = os.path.join(
			settings.MEDIA_ROOT,report.report_file.name
		)
		merger.append(PdfFileReader(file(report_file, 'rb')))
	
	merger.write(str(filename))
	return filename


import zipfile
def compress_reports(request, req_id):
	
	path = os.path.join(settings.MEDIA_ROOT, "uploads/reports/reqs/")
	name = os.path.join(path,"requisicion_"+req_id+".zip")

	reports = ReportFile.objects.filter(study__requisition_id=req_id, verified=True).values_list('candidate_id')
	candidates = Candidate.objects.filter(id__in=reports)
	
	zip_archive = zipfile.ZipFile(name, "w")

	for candidate in candidates:
		filename = join_reports(request, candidate.dni_number)
		zip_archive.write(
			filename, 
			arcname='reporte-'+candidate.dni_number+'.pdf',
			compress_type = zipfile.ZIP_DEFLATED
		)
	
	zip_archive.close()

	with open(name, 'r') as zipf:
		response = HttpResponse(zipf.read(), content_type='application/zip')
		response['Content-Disposition'] = 'inline;filename="requisicion_'+req_id+'.zip"'
		return response
	zipf.closed


def update_study_status(study):
	reportsA = study.reportfile_set.all().count()
	reportsB = study.reportform_set.all().count()
	
	createdA = study.reportfile_set.filter(verified=False, locked=False).count()
	createdB = study.reportform_set.filter(verified=False, locked=False).count()

	endedA = study.reportfile_set.filter(verified=True).count()
	endedB = study.reportform_set.filter(verified=True).count()
	
	if (createdA+createdB == reportsA+reportsB):
		study.status = 'A'
	elif(endedA+endedB == reportsA+reportsB):
		study.status = 'F'
	else:
		study.status = 'R'

	study.save()


from django.core.mail import send_mail
def notificate_report(site_user, element_id):

	users = SiteUser.objects.filter(is_superuser=True)
	mails = []
	for user in users:
		notification = Notification(
			a_tag='',
			user=user,
			message='El usuario '+site_user.first_name+' '+site_user.last_name+' ha enviado un reporte para revisar.</a>'.decode('utf-8'),
			short=u"Nuevo Reporte",
			icon="fa fa-text-file"
		)
		mails.append(user.email)

	notification.save()
	notification.a_tag='<a href="/estudios/ver/'+str(element_id)+'?notif='+str(notification.id)+'">'
	notification.save()

	send_mail(
		subject=u'Nuevo reporte', 
		message='Se ha enviado un reporte para revisar.',
		html_message='<p>El usuario '+site_user.first_name+' '+site_user.last_name+' ha enviado un reporte para revisar. <a href="ursus.cosegem.com/estudios/ver/'+str(element_id)+'?notif='+str(notification.id)+'">Ver reporte</a></p>'.decode('utf-8'),
		from_email='Ursus <notificaciones.ursus@cosegem.com>',
		recipient_list=mails,
		fail_silently=False 
	)
