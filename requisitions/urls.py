from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^$', 'requisitions.views.home', name='home'),
    url(r'^nueva/$', 'requisitions.views.create_req', name='new_req'),
    url(r'^ver/(?P<req_id>\d+)/$', 'requisitions.views.view_req', name='view_req'),
    url(r'^bajar-adjuntos/(?P<req_id>\d+)/$', 'requisitions.views.download', name='download'),
    url(r'^editar/(?P<req_id>\d+)/$', 'requisitions.views.edit_req', name='edit_req'),

    url(r'^(?P<req_id>\d+)/crear-estudio/$', 'studies.views.create_study', name='create_study'),

)