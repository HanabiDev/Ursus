#encoding: utf-8
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from models import ReportForm
from users.models import SiteUser
from studies.models import Study
import json
from django.core.urlresolvers import reverse_lazy
import os
from users.models import Notification

from reports.forms import ReportRouterForm

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
		
		report = ReportForm(
			study=Study.objects.get(id=study_id),
			json_data=json.dumps(fields),
			report_type='LS'
		)
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
