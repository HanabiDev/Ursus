#encoding: utf-8
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
# Create your views here.

from django.contrib.auth.models import User
from models import Notification, Role
from forms import UserAddForm, UserEditForm, NewProfileForm
from two_factor.utils import default_device, backup_phones

@login_required(login_url=reverse_lazy('authy:authy_login'))
@permission_required('auth.view_user', login_url='/permisos-insuficientes/')
def home(request):
	users = User.objects.all()
	return render_to_response('users_index.html', {'users':users}, context_instance=RequestContext(request))

@login_required(login_url=reverse_lazy('authy:authy_login'))
@permission_required('auth.view_user', login_url='/permisos-insuficientes/')
def index_employees(request):
	employees = User.objects.filter(type='E')
	return render_to_response('users_index.html', {'users':employees, 'employees':True}, context_instance=RequestContext(request))

@login_required(login_url=reverse_lazy('authy:authy_login'))
@permission_required('auth.view_user', login_url='/permisos-insuficientes/')
def index_clients(request):
	clients = User.objects.filter(type='C')
	return render_to_response('users_index.html', {'users':clients, 'employees':False}, context_instance=RequestContext(request))

def account(request):
	try:
		backup_tokens = request.user.staticdevice_set.all()[0].token_set.count()
	except Exception:
		backup_tokens = 0

	status = {
		'default_device': default_device(request.user),
		'default_device_type': default_device(request.user).__class__.__name__,
		'backup_phones': backup_phones(request.user),
		'backup_tokens': backup_tokens,
		'site_user': request.user
	}

	return render_to_response('account.html', status, context_instance=RequestContext(request))

def profile(request, user_id):
	user = User.objects.get(id=user_id)
	return render_to_response('account.html', {'site_user':user}, context_instance=RequestContext(request))


@login_required(login_url='authy:authy_login')
@permission_required('auth.add_user', login_url='/permisos-insuficientes/')
def new_employee(request):

	if request.method == 'GET':
		form = UserAddForm()
		return render_to_response('add_user.html', {'form':form, 'employees': True}, context_instance=RequestContext(request))
	
	elif request.method == 'POST':
		form = UserAddForm(request.POST)
        if form.is_valid():
        	new_user = form.save()
        	new_user.avatar = 'uploads/avatars/avatar.png'
        	new_user.type = 'E'
        	new_user.company = 'COSEGEM S.A.S.'
        	new_user.save()

        	return redirect(reverse_lazy('admin:users:edit',kwargs={'user_id':str(new_user.id)}))
        else:
        	return render_to_response('add_user.html',
							  {'form':form, 'employees':True}, context_instance=RequestContext(request))

@login_required(login_url='authy:authy_login')
@permission_required('auth.add_user', login_url='/permisos-insuficientes/')
def new_client(request):

	if request.method == 'GET':
		form = UserAddForm()
		return render_to_response('add_user.html', {'form':form}, context_instance=RequestContext(request))
	
	elif request.method == 'POST':
		form = UserAddForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            if new_user.genre == 'M':
            	new_user.avatar = 'uploads/avatars/avatar.png'
            else:
            	new_user.avatar = 'uploads/avatars/f_avatar.png'
            new_user.type = 'C'
            new_user.save()

            return redirect(reverse_lazy('admin:users:edit',kwargs={'user_id':str(new_user.id)}))
        else:
        	return render_to_response('add_user.html',
							  {'form':form}, context_instance=RequestContext(request))

@login_required(login_url='authy:authy_login')
@permission_required('auth.change_user', login_url='/permisos-insuficientes/')
def edit_user(request, user_id):

	user = User.objects.get(id=user_id)

	if request.method == 'GET':
		
		form = UserEditForm(instance=user)
		if user.type == 'E':
			form = UserEditForm(initial={'role': user.role}, instance=user)

		return render_to_response('edit_user.html', {'form':form, 'site_user':user}, 
						context_instance=RequestContext(request))

	if request.method == 'POST':
		form = UserEditForm(request.POST, instance=user)

		if form.is_valid():

			user = form.save()

			if request.FILES:
				user.avatar = request.FILES.get('avatar')
			
			user.save()

			if user.type == 'C':
				return redirect(reverse_lazy('admin:users:clients'))
			
			return redirect(reverse_lazy('admin:users:employees'))


    	return render_to_response('edit_user.html', {'form':form, 'site_user':user}, 
						context_instance=RequestContext(request))

@login_required(login_url='authy:authy_login')
@permission_required('auth.change_user', login_url='/permisos-insuficientes/')
def toggle_lock(request, user_id):
	user = User.objects.get(id=user_id)
	user.is_active = not user.is_active
	user.save()

	if user.type == 'C':
		return redirect(reverse_lazy('admin:users:clients'))
	
	return redirect(reverse_lazy('admin:users:employees'))

def registry_client(request):
	message = 'Elige un nombre de usuario y contraseña, estos serán tus datos de inicio de sesión.'
	if request.method == 'GET':
		form = UserAddForm()
		return render_to_response('registry.html', {'form':form, 'message':message}, context_instance=RequestContext(request))
		
	elif request.method == 'POST':
		form = UserAddForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            new_user.type = 'C'
            new_user.is_active = False
            new_user.save()

            request.session['new_profile'] = new_user.id

            return redirect(reverse_lazy('new_profile'))
        else:
        	return render_to_response('registry.html',
							  {'form':form, 'message':message}, context_instance=RequestContext(request))

def new_profile(request):
	if not request.session.get('new_profile'):
		return redirect(reverse_lazy('dashboard:home'))
	
	user = User.objects.get(id=request.session['new_profile'])
	message = 'Para fines de contacto te pedimos por favor suministres algunos datos adicionales, luego de esto podrás iniciar sesión con tus credenciales.'
	
	form = NewProfileForm(initial={'type': 'C'}, instance=user)
	if request.method == 'GET':
		form = NewProfileForm(instance=user)
		
		return render_to_response('registry.html', {'form':form, 'editing':True, 'message':message}, 
						context_instance=RequestContext(request))

	elif request.method == 'POST':
		form = NewProfileForm(request.POST, instance=user)

		if form.is_valid():

			user = form.save()

			if user.genre == 'M':
				user.avatar = 'uploads/avatars/avatar.png'
			else:
				user.avatar = 'uploads/avatars/f_avatar.png'
			user.is_active = True
			user.save()
			notificate_registry(user)

			return redirect(reverse_lazy('authy:authy_login'))
			
    	return render_to_response('registry.html', {'form':form, 'editing':True, 'message':message}, 
						context_instance=RequestContext(request))

def notificate_registry(new_user):
	users = User.objects.filter(is_superuser=True)

	for user in users:
		notification = Notification(
				user=user,
				message="El cliente "+new_user.first_name+" "+new_user.last_name+" se ha registrado en la plataforma.",
				short="Nuevo registro",
				icon="fa fa-user"
			)
		notification.save()
