from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^$', 'assignments.views.home', name='home'),
    url(r'^ver/(?P<assign_id>\d+)/$', 'assignments.views.view_assign', name='view_assign'),   
)