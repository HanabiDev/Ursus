#encoding: utf-8
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.models import User
from requisitions.models import Atachment

from users.models import Notification
from models import Requisition
from forms import AddRequisitionForm
from django.core.urlresolvers import reverse_lazy

def home(request):
	reqs = ''
	if request.user.is_superuser or request.user.is_staff:
		reqs = Requisition.objects.all()
	else:
		reqs = Requisition.objects.filter(client=request.user)

	reqs = reqs.order_by('-open_date')
	return render_to_response('index_reqs.html', {'reqs':reqs}, context_instance=RequestContext(request))

def create_req(request):

	if request.method == 'GET':
		if request.user.type == 'C':
			form = AddRequisitionForm(initial={'client': request.user})
		else:
			form = AddRequisitionForm()
		return render_to_response('requisition.html', {'form':form}, context_instance=RequestContext(request))

	if request.method == 'POST':
		form = AddRequisitionForm(request.POST)
		if form.is_valid():
			new_req = form.save()

			if request.FILES:
				files = request.FILES
				if hasattr(files, 'getlist'):
					cv_files = files.getlist('curriculums')
					save_attachements(new_req, 'CV', cv_files)

					orders = files.getlist('orders')
					save_attachements(new_req, 'BO', orders)

					resume = files.get('resume')
					new_atachment = Atachment(requisition=new_req, file_type='RE', file_resource=resume)
					new_atachment.save()

			notificate_requisition(request.user, new_req.id)
			return redirect(reverse_lazy('reqs:home'))

		return render_to_response('requisition.html', {'form':form}, context_instance=RequestContext(request))

def view_req(request, req_id):
	req = Requisition.objects.get(id=req_id)

	if request.GET.get('notif'):
		not_id = request.GET.get('notif')
		notif = Notification.objects.get(id=not_id)
		notif.status=True
		notif.save()
		print notif

	return render_to_response('req_detail.html', {'req':req}, context_instance=RequestContext(request))

def edit_req(request, req_id):

	if request.method == 'GET':
		req = Requisition.objects.get(id=req_id)
		form = AddRequisitionForm(instance=req)
		return render_to_response('requisition.html', {'form':form, 'editing':True, 'id': req_id}, context_instance=RequestContext(request))
	
	if request.method == 'POST':
		req = Requisition.objects.get(id=req_id)
		form = AddRequisitionForm(request.POST, instance=req)
		if form.is_valid():
			new_req = form.save()

			return redirect(reverse_lazy('reqs:view_req', kwargs={'req_id':str(new_req.id)}))

		return render_to_response('requisition.html', {'form':form, 'editing':True, 'id': req_id}, context_instance=RequestContext(request))

from django.core.mail import send_mail

def notificate_requisition(site_user, element_id):
	users = User.objects.filter(is_superuser=True)

	mails = []
	for user in users:
		mails.append(user.email)

		notification = Notification(
				a_tag='',
				user=user,
				message='El cliente '+site_user.first_name+' '+site_user.last_name+' ha registrado una nueva requisición.</a>'.decode('utf-8'),
				short=u"Nueva requisición",
				icon="fa fa-book"
			)
		notification.save()
		notification.a_tag='<a href="/requisiciones/ver/'+str(element_id)+'?notif='+str(notification.id)+'">'
		notification.save()

	send_mail(
		subject=u'Nueva requisición registrada', 
		message='El cliente '+site_user.first_name+' '+site_user.last_name+' ha registrado una nueva requisicion.',
		html_message='<p>El cliente '+site_user.first_name+' '+site_user.last_name+' ha registrado una nueva requisicion. <a href="ursus.cosegem.com/requisiciones/ver/'+str(element_id)+'?notif='+str(notification.id)+'">Ver requisicion</a></p>'.decode('utf-8'),
		from_email='notificaciones.ursus@cosegem.com',
		recipient_list=mails,
		fail_silently=False 
	)



def save_attachements(requisition, type, files):
	for file in files:
		new_attachement = Atachment(requisition=requisition, file_type=type, file_resource=file)
		new_attachement.save()

from shutil import make_archive
from django.core.servers.basehttp import FileWrapper
from django.conf import settings
from django.http import HttpResponse

def download(request, req_id):
    file_path = settings.MEDIA_ROOT+'/uploads/requisitions/'+req_id+'/'
    print file_path

    path_to_zip = make_archive(file_path,"zip",file_path)
    response = HttpResponse(FileWrapper(file(path_to_zip,'rb')), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=requisicion_'+req_id+'.zip'
    return response