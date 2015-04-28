from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^$', 'users.views.home', name='home'),
    url(r'^actualizar-cuenta/(?P<user_id>\d+)/$', 'users.views.edit_user', name='update_account'),
    url(r'^empleados/$', 'users.views.index_employees', name='employees'),
    url(r'^clientes/$', 'users.views.index_clients', name='clients'),
    url(r'^empleados/nuevo/$', 'users.views.new_employee', name='new_employee'),
    url(r'^clientes/nuevo/$', 'users.views.new_client', name='new_client'),
   	url(r'^ver/(?P<user_id>\d+)/$', 'users.views.profile', name='profile'),
    url(r'^editar/(?P<user_id>\d+)/$', 'users.views.edit_user', name='edit'),
    url(r'^bloquear/(?P<user_id>\d+)/$', 'users.views.toggle_lock', name='block'),
    url(r'^desbloquear/(?P<user_id>\d+)/$', 'users.views.toggle_lock', name='unblock'),
)