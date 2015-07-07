#encoding: utf-8
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from users.models import Notification
from django.core.mail import send_mail
from forms import StudyForm
from models import Requisition
from models import Study
from django.contrib.auth.models import User

def home(request):
	if request.user.is_superuser or request.user.is_staff:
		studies = Study.objects.all()
	elif request.user.type == 'C':
		studies = Study.objects.filter(requisition__client=request.user)
	else:
		studies = Study.objects.filter(employee=request.user)
	
	studies = studies.order_by('-id')
	return render_to_response('studies_index.html', {'studies':studies}, context_instance=RequestContext(request))

def create_study(request, req_id=None):

	if request.method == 'GET':
		if req_id:
			form = StudyForm(initial={'requisition':req_id})
			return render_to_response('study.html', {'id':req_id, 'form':form}, context_instance=RequestContext(request))
		else:
			form = StudyForm()
			return render_to_response('study.html', {'form':form}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
	
		form = StudyForm(request.POST, request.FILES)

		if form.is_valid():
			study = form.save()
			
			if request.FILES:
				study.attachment = request.FILES.get('attachment')
			
			study.save()

			notificate_assignation(study.employee, study.id)

			return redirect(reverse_lazy('studies:home'))
		
		return render_to_response('study.html', {'id':req_id,'form':form}, context_instance=RequestContext(request))

def view_study(request, study_id):
	if request.GET.get('notif'):
		not_id = request.GET.get('notif')
		notif = Notification.objects.get(id=not_id)
		notif.status=True
		notif.save()

	study = Study.objects.get(id=study_id)
	return render_to_response('study_detail.html', {'study':study}, context_instance=RequestContext(request))

def edit_study(request, study_id):
	study = Study.objects.get(id=study_id)

	if request.method == 'GET':
		form = StudyForm(instance=study)
		return render_to_response('study.html', {'r_id':study.requisition.id, 'id':study_id,'form':form, 'editing':True}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		form = StudyForm(request.POST, instance=study)
		if form.is_valid():
			study = form.save()
			return redirect(reverse_lazy('studies:view_study', kwargs={'study_id':str(study_id)}))

		return render_to_response('study.html', {'r_id':study.requisition.id, 'id':study_id,'form':form, 'editing':True}, context_instance=RequestContext(request))

from django.core.mail import send_mail
def notificate_assignation(site_user, element_id):

	notification = Notification(
		a_tag='',
		user=site_user,
		message='Se le ha asignado un nuevo estudio.</a>'.decode('utf-8'),
		short=u"Nueva asignación",
		icon="fa fa-search"
	)

	notification.save()
	notification.a_tag='<a href="/estudios/ver/'+str(element_id)+'?notif='+str(notification.id)+'">'
	notification.save()

	send_mail(
		subject=u'Nueva asignación', 
		message='Se le ha asignado un nuevo estudio.',
		html_message='<p>Se le ha asignado un nuevo estudio. Para mayor detalle use <a href="ursus.cosegem.com/estudios/ver/'+str(element_id)+'?notif='+str(notification.id)+'">este enlace</a></p>'.decode('utf-8'),
		from_email='Ursus <notificaciones.ursus@cosegem.com>',
		recipient_list=[site_user.email],
		fail_silently=False 
	)
