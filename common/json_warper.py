from django.core import serializers
from django.http import JsonResponse,HttpResponse
import json as json_module


def json(request):
    try:
        get_dict = request.GET
        json_str = get_dict.get('json')
        json_str = str(json_str)
        if json_str == '1' or json_str.lower() == 'true':
            return True
        else:
            return False
    except Exception:
        return False


def is_iterable(obj):
    try:
        if obj.__iter__:
            return True
        else:
            return False
    except AttributeError:
        return False


def json_response(data):
    json_data = {}
    item_list_of_data = data.items()
    for item in item_list_of_data:
        name, data = item
        try:
            if is_iterable(data):
                data_list = []
                for instance in data:
                    data_list.append(instance.get_json_object())
                json_data[name] = data_list
            else:
                json_data[name] = data.get_json_object()
        except AttributeError:
            json_data[name] = str(data)
    return HttpResponse(json_module.dumps(json_data).__str__())


