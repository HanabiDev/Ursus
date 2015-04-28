from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render_to_response, HttpResponse
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, FormView

from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


from two_factor.views import OTPRequiredMixin
from two_factor.views.utils import class_view_decorator
from two_factor.utils import default_device, backup_phones
from two_factor.views import (LoginView, DisableView,SetupCompleteView, SetupView,
                              ProfileView, QRGeneratorView)

# Create your views here.

@login_required
def home(request):

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


class OwnDisableView(DisableView):
    template_name = 'disable_otp.html'
    redirect_url = reverse_lazy('authy:account')

class OwnSetupView(SetupView):
    template_name = 'setup.html'
    redirect_url = reverse_lazy('authy:account')

class OwnLoginView(LoginView):
    template_name = 'login.html'