from django.http import HttpResponse
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


def generate_json(data):
    if type(data) == dict:
        result = {}
        item_list_of_data = data.items()
        for item in item_list_of_data:
            name, data = item
            result[name] = generate_json(data)
        return result
    elif hasattr(data, '__iter__'):
        result = []
        for item in data:
            result.append(generate_json(item))
        return result
    elif hasattr(data, 'get_json_object'):
        return data.get_json_object()
    elif isinstance(data, str):
        return str(data)
    else:
        raise TypeError


def json_response(data):
    json_data = generate_json(data)
    return HttpResponse(json_module.dumps(json_data).__str__())


