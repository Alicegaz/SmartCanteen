from django.core import serializers
from django.http import JsonResponse,HttpResponse
import json as json_module


def json(request):
    try:
        get_dict = request.GET
        json = get_dict.get('json')
        if json:
            return True
        else:
            return False
    except:
        return False


def json_response(request, data):
    json_data = []
    try:
        for instance in data:
            json_data.append(instance.get_json_object())
    except TypeError:
        json_data = {'data': serializers.serialize('json', data)}
        return JsonResponse(json_data)
    return HttpResponse(json_module.dumps(json_data).__str__())


