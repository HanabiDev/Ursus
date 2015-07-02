from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^(?P<assignment_id>\d+)/reporte-antecedentes/$', 'reports.views.create_legal_report', name='new_legal_report'),
    url(r'^nueva/$', 'requisitions.views.create_req', name='new_req'),
)