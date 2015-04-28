from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^$', 'settings.views.home', name='home'),
    url(r'^servicios/$', 'settings.views.index_services', name='services'),
    url(r'^servicios/nuevo/$', 'settings.views.create_service', name='new_service'),
    url(r'^servicios/editar/(?P<service_id>\d+)/$', 'settings.views.edit_service', name='edit_service'),
    url(r'^servicios/eliminar/(?P<service_id>\d+)/$', 'settings.views.delete_service', name='delete_service'),
    url(r'^cargos/$', 'settings.views.index_roles', name='roles'),
    url(r'^cargos/nuevo/$', 'settings.views.create_role', name='new_role'),
    url(r'^cargos/editar/(?P<role_id>\d+)/$', 'settings.views.edit_role', name='edit_role'),
    url(r'^cargos/eliminar/(?P<role_id>\d+)/$', 'settings.views.delete_role', name='delete_role'),
)