from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from app_frota.models import Cidade

@csrf_exempt
def cidades(request):
    cidades = Cidade.objects.filter(estado_id=request.POST['estado'])

    data_json = serializers.serialize('json', cidades)

    return HttpResponse(data_json, mimetype='application/json')