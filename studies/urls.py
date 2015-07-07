from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^$', 'studies.views.home', name='home'),
    url(r'^nuevo/$', 'studies.views.create_study', name='new_study'),
    url(r'^ver/(?P<study_id>\d+)/$', 'studies.views.view_study', name='view_study'),
    url(r'^editar/(?P<study_id>\d+)/$', 'studies.views.edit_study', name='edit_study'),
)