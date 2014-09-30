from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project_controlefrota.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^estado/cidades/$', 'app_frota.views.cidade.cidades', name='cidades'),
    url(r'^adicionar-servidor/$', 'app_frota.views.servidor.adicionar', name='adicionar-servidor'),
    url(r'^editar-servidor/(?P<user_id>\d+)/$', 'app_frota.views.servidor.editar', name='editar-servidor'),
    url(r'^consultar-servidores/$', 'app_frota.views.servidor.consultar', name='consultar-servidores'),

    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login/login.html'}),
    url(r'^logout/$', 'app_frota.views.controle.logout_user', name='logout_user'),
    url(r'^perfil/$', 'app_frota.views.servidor.salvar_perfil', name='perfil'),
    url(r'^$', 'app_frota.views.controle.index', name='index'),

    url(r'^visualizar-autorizacao/(?P<id>\d+)/$', 'app_frota.views.autorizacao.visualizar', name='visualizar-autorizacao'),
    url(r'^consultar-autorizacoes/$', 'app_frota.views.autorizacao.consultar', name='consultar-autorizacoes'),

    url(r'^solicitar-emprestimo/$', 'app_frota.views.emprestimo.solicitar', name='solicitar-emprestimo'),
    url(r'^emprestimo/veiculos/$', 'app_frota.views.emprestimo.veiculos_disponiveis', name='emprestimo-veiculos'),

    url(r'^cargainicial/$', 'app_frota.views.carga_inicial.carga', name='carga'),

    url(r'^cadastrar-marca/$', 'app_frota.views.marca.cadastrar_marca', name='cadastrar_marca'),
)
