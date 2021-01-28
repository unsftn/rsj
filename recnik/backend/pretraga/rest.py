from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def odrednica(request):
    if request.method == 'GET':
        return _search_odrednica(request)
    elif request.method == 'POST':
        return _add_odrednica(request)
    elif request.method == 'PUT':
        return _update_odrednica(request)
    elif request.method == 'DELETE':
        return _delete_odrednica(request)


def _search_odrednica(request):
    pass


def _add_odrednica(request):
    pass


def _update_odrednica(request):
    pass


def _delete_odrednica(request):
    pass


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def korpus(request):
    if request.method == 'GET':
        return _search_korpus(request)
    elif request.method == 'POST':
        return _add_korpus(request)
    elif request.method == 'PUT':
        return _update_korpus(request)
    elif request.method == 'DELETE':
        return _delete_korpus(request)


def _search_korpus(request):
    pass


def _add_korpus(request):
    pass


def _update_korpus(request):
    pass


def _delete_korpus(request):
    pass
