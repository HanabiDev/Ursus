from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^$', 'dashboard.views.home', name='home'),
    url(r'^usuarios/', include('users.urls', 'users')),
)