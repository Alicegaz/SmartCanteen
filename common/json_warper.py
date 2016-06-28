from django.core import serializers
from django.http import JsonResponse,HttpResponse
import json as json_module


def json(request):
    try:
        get_dict = request.GET
        json = get_dict.get('json')
        json = str(json)
        if json == '1' or json.lower() == 'true':
            return True
        else:
            return False
    except:
        return False


def json_response(data):
    json_data = {}
    item_list_of_data = data.items()
    for item in item_list_of_data:
        print(item)
        print(1)
        name, data = item
        try:
            if data.__iter__:
                print(data.__iter__)
                data_list = []
                for instance in data:
                    print(instance)
                    data_list.append(instance.get_json_object())
                    print(data_list)
                json_data[name] = data_list
            else:
                json_data[name] = data.get_json_object
        except AttributeError:
            print(4)
            json_data[name] = str(data)
    return HttpResponse(json_module.dumps(json_data).__str__())


