from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project_controlefrota.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^cadastra_servidor/$', 
      'appfrota.views.servidor.cadastra_servidor', 
      name='cadastra_servidor'),

    url(r'^admin/', include(admin.site.urls)),
)
