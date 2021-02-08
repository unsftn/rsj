import json

from elasticsearch.exceptions import ElasticsearchException, NotFoundError
from elasticsearch_dsl import Search, analyzer, Index
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.query import MultiMatch, Bool, Match
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND

from pretraga.models import OdrednicaDocument, KorpusDocument
from pretraga.serializers import CreateOdrednicaDocumentSerializer, CreateKorpusDocumentSerializer, \
    OdrednicaResponseSerializer, KorpusResponseSerializer

odrednicaIndex = 'odrednica'
korpusIndex = 'korpus'
serbianAnalyzer = analyzer('serbian')
host = 'localhost'
JSON = 'application/json'
connections.create_connection(hosts=[host], timeout=20)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def odrednica(request):
    if not connections.get_connection().indices.exists(odrednicaIndex):
        odrednicaIdx = Index(odrednicaIndex)
        odrednicaIdx.analyzer(serbianAnalyzer)
        odrednicaIdx.document(OdrednicaDocument)
        odrednicaIdx.create()

    if request.method == 'GET':
        return _search_odrednica(request)
    elif request.method == 'POST':
        return _add_odrednica(request)
    elif request.method == 'PUT':
        return _update_odrednica(request)
    elif request.method == 'DELETE':
        return _delete_odrednica(request)


def _search_odrednica(request):
    if not request.data or request.data['term'] is None:
        return BadRequest('no search term')

    term = request.data['term']
    hits = []
    s = Search(index=odrednicaIndex)
    s = s.source(includes=['pk', 'rec', 'vrsta'])
    s.query = MultiMatch(
        type='bool_prefix',
        query=term,
        fields=['varijante'],
        analyzer=serbianAnalyzer
    )
    try:
        response = s.execute()
        for hit in response.hits.hits:
            hits.append(hit['_source'])

        serializer = OdrednicaResponseSerializer(hits, many=True)
        data = serializer.data

        return Response(
            data,
            status=HTTP_200_OK,
            content_type=JSON
        )
    except ElasticsearchException as error:
        return ServerError(error.args)


def _add_odrednica(request):
    if not request.data or request.data['odrednica'] is None:
        return BadRequest('no data to index')
    odrednica = request.data['odrednica']

    return _save_odrednica(odrednica)


def _update_odrednica(request):
    if not request.data or request.data['odrednica'] is None:
        return BadRequest('no data to index')
    odrednica = request.data['odrednica']

    return _save_odrednica(odrednica)


def _delete_odrednica(request):
    if not request.data or request.data['pk'] is None:
        return BadRequest('no primary key')

    pk = request.data['pk']
    odrednica = OdrednicaDocument()
    try:
        odrednica.delete(id=pk, index=odrednicaIndex)
        return Response(status=HTTP_200_OK)
    except NotFoundError:
        return NotFound('requested object not found')
    except ElasticsearchException as error:
        return ServerError(error.args)


def _save_odrednica(item):
    serializer = CreateOdrednicaDocumentSerializer()
    try:
        odrednica = serializer.create(item)
    except KeyError as error:
        return BadRequest(error.args)

    try:
        result = odrednica.save(id=odrednica.pk, index=odrednicaIndex)
        return Response(
            result,
            status=HTTP_200_OK,
            content_type=JSON
        )
    except ElasticsearchException as error:
        return ServerError(error.args)


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def korpus(request):
    if not connections.get_connection().indices.exists(korpusIndex):
        korpusIdx = Index(korpusIndex)
        korpusIdx.analyzer(serbianAnalyzer)
        korpusIdx.document(KorpusDocument)
        korpusIdx.create()

    if request.method == 'GET':
        return _search_korpus(request)
    elif request.method == 'POST':
        return _add_korpus(request)
    elif request.method == 'PUT':
        return _update_korpus(request)
    elif request.method == 'DELETE':
        return _delete_korpus(request)


def _search_korpus(request):
    if not request.data or request.data['term'] is None:
        return BadRequest('no search term')

    term = request.data['term']
    hits = []
    s = Search(index=korpusIndex)
    s = s.source(includes=['pk', 'osnovniOblik'])
    s.query = Bool(
        must=[Match(oblici=term)]
    )
    try:
        response = s.execute()
        for hit in response.hits.hits:
            hits.append(hit['_source'])

        serializer = KorpusResponseSerializer(hits, many=True)
        data = serializer.data

        return Response(
            data,
            status=HTTP_200_OK,
            content_type=JSON
        )
    except ElasticsearchException as error:
        return ServerError(error.args)


def _add_korpus(request):
    if not request.data or request.data['anotiranaRec'] is None:
        return BadRequest('no data to index')
    anotiranaRec = request.data['anotiranaRec']

    return _save_korpus(anotiranaRec)


def _update_korpus(request):
    if not request.data or request.data['anotiranaRec'] is None:
        return BadRequest('no data to index')
    anotiranaRec = request.data['anotiranaRec']

    return _save_korpus(anotiranaRec)


def _delete_korpus(request):
    if not request.data or request.data['pk'] is None:
        return BadRequest('no primary key')

    pk = request.data['pk']
    anotiranaRec = KorpusDocument()
    try:
        anotiranaRec.delete(id=pk, index=korpusIndex)
        return Response(status=HTTP_200_OK)
    except NotFoundError:
        return NotFound('requested object not found')
    except ElasticsearchException as error:
        return ServerError(error.args)


def _save_korpus(item):
    serializer = CreateKorpusDocumentSerializer()
    try:
        anotiranaRec = serializer.create(item)
    except KeyError as error:
        return BadRequest(error.args)

    try:
        result = anotiranaRec.save(id=anotiranaRec.pk, index=korpusIndex)
        return Response(
            result,
            status=HTTP_200_OK,
            content_type=JSON
        )
    except ElasticsearchException as error:
        return ServerError(error.args)


def BadRequest(error):
    return Response(
        error,
        status=HTTP_400_BAD_REQUEST,
        content_type=JSON
    )


def NotFound(error):
    return Response(
        error,
        status=HTTP_404_NOT_FOUND,
        content_type=JSON
    )


def ServerError(error):
    return Response(
        error,
        status=HTTP_500_INTERNAL_SERVER_ERROR,
        content_type=JSON
    )