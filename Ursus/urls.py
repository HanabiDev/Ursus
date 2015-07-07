from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import static
from django.conf import settings
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = patterns('',
	url(r'', include('authy.urls', 'authy')),
	url(r'^$', include('dashboard.urls', 'dashboard')),
	url(r'^registro/$', 'users.views.registry_client', name='registry'),
	url(r'^registro/continuar/$', 'users.views.new_profile', name='new_profile'),
	url(r'^admin/', include('admin.urls', 'admin')),
	url(r'^requisiciones/', include('requisitions.urls', 'reqs')),
	url(r'^estudios/', include('studies.urls', 'studies')),
	url(r'^reportes/', include('reports.urls', 'reports')),
	url(r'^configuracion/', include('settings.urls', 'settings')),

	url(r'^redactor/', include('redactor.urls')),
	
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),

    url(r'', include(tf_urls, 'two_factor')),
    url(r'', include('user_sessions.urls', 'user_sessions')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
