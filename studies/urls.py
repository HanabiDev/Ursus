from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^$', 'studies.views.home', name='home'),
    url(r'^nuevo/$', 'studies.views.add_study', name='new_study'),
    url(r'^nuevo/agregar-candidato/$', 'studies.views.add_candidate', name='new_candidate'),
    url(r'^editar-candidato/(?P<candidate_id>\d+)/$', 'studies.views.edit_candidate', name='edit_candidate'),
    url(r'^ver/(?P<study_id>\d+)/$', 'studies.views.view_study', name='view_study'),
    url(r'^editar/(?P<study_id>\d+)/$', 'studies.views.edit_study', name='edit_study'),

    url(r'^(?P<study_id>\d+)/asignar-empleados/$', 'studies.views.assign_employees', name='assign_employees'),
    url(r'^crear-estudios/$', 'studies.views.create_studies', name='create_studies'),
)