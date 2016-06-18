from django.core import serializers
from django.http import JsonResponse,HttpResponse

def json(request):
    try:
        get = request.GET
        json = get.get('json')
        if json:
            return True
        else:
            return False
    except:
        return False


def json_response(request, data):
    json_data = serializers.serialize('json', data)
    return JsonResponse(json_data, safe=False)


