from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project_controlefrota.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    url(r'^cadastra_servidor/$', 'app_frota.views.servidor.cadastra_servidor', name='cadastra_servidor'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^/', 'appfrota.views.autenticacao.login'),
    url(r'^login/$', 'django.contrib.auth.views.login', {"template_name": "login.html"}),
)
