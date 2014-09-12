#coding: utf-8
from django.conf import settings
from django.template.loader import render_to_string


def get_menu(request):
    html = ''
    if request.user.is_authenticated():

        grupos_id = request.user.groups.values_list('id', flat=True).all()
        if settings.PERM_GRUPO_ADM in grupos_id:
            html += render_to_string('menu/menu_adm.html')

        if settings.PERM_GRUPO_SERVIDOR in grupos_id:
            html += render_to_string('menu/menu_servidor.html')

    return {'context_menu':html}