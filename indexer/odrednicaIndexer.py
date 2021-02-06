from time import sleep

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index, Document, SearchAsYouType, analyzer, Search, Keyword
from elasticsearch_dsl.query import MultiMatch
import json


index = 'odrednica'
serbianAnalyzer = analyzer('serbian')
host = 'localhost'
data = []


class Odrednica(Document):
    pk = Keyword()
    rec = Keyword()
    varijante = SearchAsYouType(analyzer=serbianAnalyzer)
    vrsta = Keyword()


def createIndex():
    connections.create_connection(hosts=[host], timeout=20)
    if not connections.get_connection().indices.exists(index):
        odrednicaIdx = Index(index)
        odrednicaIdx.analyzer(serbianAnalyzer)
        odrednicaIdx.document(Odrednica)
        odrednicaIdx.create()


def saveOdrednica(item):
    varijante = ' '.join(item['varijante'])
    varijante += ' ' + item['rec']
    odrednica = Odrednica(
        pk=item['pk'],
        rec=item['rec'],
        varijante=varijante,
        vrsta=item['vrsta']
    )
    odrednica.save(id=odrednica.pk, index=index)


def deleteOdrednica(pk):
    odrednica = Odrednica()
    odrednica.delete(id=pk, index=index)


def searchOdrednica(term):
    s = Search(index=index)
    s = s.source(includes=['pk', 'rec', 'vrsta'])
    s.query = MultiMatch(
            type='bool_prefix',
            query=term,
            fields=['varijante'],
            analyzer=serbianAnalyzer
    )

    response = s.execute()
    return response.hits


def update():
    with open('odredniceV2.json') as json_data_file:
        data = json.load(json_data_file)

    print('Update data:')
    Odrednica.init(index=index)
    for item in data:
        print(item)
        saveOdrednica(item)


if __name__ == '__main__':
    createIndex()

    with open('odrednice.json') as json_data_file:
        data = json.load(json_data_file)

    print('Added data:')
    Odrednica.init(index=index)
    for item in data:
        print(item)
        saveOdrednica(item)

    print('term: a, result: ')
    print(searchOdrednica('a'))
    print('term: aб, result: ')
    print(searchOdrednica('aб'))
    print('term: aбо, result: ')
    print(searchOdrednica('aбо'))
    print('term: abo, result: ')
    print(searchOdrednica('abo'))
    print('term: abol, result: ')
    print(searchOdrednica('abol'))
    print('term: abd, result: ')
    print(searchOdrednica('abd'))
    print('term: bo, result: ')
    print(searchOdrednica('bo'))
    print('term: рад, result: ')
    print(searchOdrednica('рад'))
    update()
    sleep(5)
    print('term: abd, result: ')
    print(searchOdrednica('abd'))
    print('term: rad, pk:6, result: ')
    print(searchOdrednica('rad'))
    print('delete pk:2, rec: abdicirati')
    deleteOdrednica(2)
    sleep(5)
    print('term: abd, result: ')
    print(searchOdrednica('abd'))
