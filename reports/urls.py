from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^(?P<study_id>\d+)/nuevo/$', 'reports.views.report_router', name='new_report'),
    
    
    url(r'^(?P<study_id>\d+)/reporte-antecedentes/$', 'reports.views.create_legal_report', name='new_legal_report'),
    url(r'^(?P<study_id>\d+)/reporte-seguridad/$', 'reports.views.create_verification_report', name='new_verif_report'),
    
    url(r'^ver/(?P<report_id>\d+)/$', 'reports.views.view_report', name='view_report'),
    url(r'^editar/(?P<report_id>\d+)/$', 'reports.views.edit_report', name='edit_report'),
    url(r'^bloquear/(?P<report_id>\d+)/$', 'reports.views.lock_report', name='lock_report'),
    url(r'^desbloquear/(?P<report_id>\d+)/$', 'reports.views.unlock_report', name='unlock_report'),
    url(r'^eliminar/(?P<report_id>\d+)/$', 'reports.views.delete_report', name='remove_report'),
    url(r'^publicar/(?P<report_id>\d+)/$', 'reports.views.check_report', name='check_report'),



    url(r'^(?P<study_id>\d+)/subir/$', 'reports.views.upload_report', name='upload_report'),
    url(r'^editar-subido/(?P<ureport_id>\d+)/$', 'reports.views.edit_upload_report', name='edit_report_upload'),
    url(r'^bloquear-subido/(?P<report_id>\d+)/$', 'reports.views.lock_upload_report', name='lock_report_upload'),
    url(r'^desbloquear-subido/(?P<report_id>\d+)/$', 'reports.views.unlock_upload_report', name='unlock_report_upload'),
    url(r'^eliminar-subido/(?P<report_id>\d+)/$', 'reports.views.delete_upload_report', name='remove_report_upload'),
    url(r'^publicar-subido/(?P<report_id>\d+)/$', 'reports.views.check_upload_report', name='check_report_upload'),

    url(r'^buscar/$', 'reports.views.search', name='search'),
    url(r'^buscar/por-requisicion/(?P<req_id>\d+)/$', 'reports.views.search_by_req', name='search_req'),
    url(r'^reporte-completo/(?P<dni>\d+)/$', 'reports.views.join_reports', name='join_reports'),
    url(r'^comprimir/(?P<req_id>\d+)/$', 'reports.views.compress_reports', name='compress_reports'),
)
