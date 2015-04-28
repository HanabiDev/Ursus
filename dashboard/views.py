from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
# Create your views here.

@login_required(login_url=reverse_lazy('authy:authy_login'))

def home(request):

	section = 'Inicio'
	return render_to_response('dash_home.html', {'section':section}, context_instance=RequestContext(request))
