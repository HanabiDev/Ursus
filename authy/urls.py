from django.conf.urls import patterns, include, url

from two_factor.urls import urlpatterns as tf_urls
#from two_factor.gateways.twilio.urls import urlpatterns as tf_twilio_urls
from views import (OwnDisableView, OwnSetupView, OwnLoginView)

urlpatterns = patterns(
    '',
    url(r'^cuenta/$', 'users.views.account', name='account'),
    url(r'^login/$', OwnLoginView.as_view(), name='authy_login'),
    url(r'^desactivar-otp/$', OwnDisableView.as_view(), name='disable_otp'),
    url(r'^activar-otp/$', OwnSetupView.as_view(), name='enable_otp'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),    
)