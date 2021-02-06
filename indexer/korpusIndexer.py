from time import sleep

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index, Document, analyzer, Search, Keyword, Text
from elasticsearch_dsl.query import Match, Bool
import json


index = 'korpus'
serbianAnalyzer = analyzer('serbian')
host = 'localhost'
data = []


class AnotiranaRec(Document):
    pk = Keyword()
    osnovniOblik = Keyword()
    oblici = Text(analyzer=serbianAnalyzer)


def createIndex():
    connections.create_connection(hosts=[host], timeout=20)
    if not connections.get_connection().indices.exists(index):
        odrednicaIdx = Index(index)
        odrednicaIdx.analyzer(serbianAnalyzer)
        odrednicaIdx.document(AnotiranaRec)
        odrednicaIdx.create()


def saveAnotiranaRec(item):
    oblici = ' '.join(item['oblici'])
    oblici += ' ' + item['osnovniOblik']
    anotiranaRec = AnotiranaRec(
        pk=item['pk'],
        osnovniOblik=item['osnovniOblik'],
        oblici=oblici
    )
    anotiranaRec.save(id=anotiranaRec.pk, index=index)


def deleteAnotiranaRec(pk):
    anotiranaRec = AnotiranaRec()
    anotiranaRec.delete(id=pk, index=index)


def searchAnotiranaRec(term):
    s = Search(index=index)
    s = s.source(includes=['pk', 'osnovniOblik'])
    s.query = Bool(
        must=[Match(oblici=term)]
    )

    response = s.execute()
    return response.hits


def update():
    with open('korpusV2.json') as json_data_file:
        data = json.load(json_data_file)

    print('Update data:')
    AnotiranaRec.init(index=index)
    for item in data:
        print(item)
        saveAnotiranaRec(item)


if __name__ == '__main__':
    createIndex()

    with open('korpus.json') as json_data_file:
        data = json.load(json_data_file)

    print('Added data:')
    AnotiranaRec.init(index=index)
    for item in data:
        print(item)
        saveAnotiranaRec(item)

    print('term: abolicijski, result: ')
    print(searchAnotiranaRec('abolicijski'))
    print('term: aбolirati, result: ')
    print(searchAnotiranaRec('aбolirati'))
    print('term: аболи́цӣјској, result: ')
    print(searchAnotiranaRec('аболи́цӣјској'))
    print('term: bombona, result: ')
    print(searchAnotiranaRec('bombona'))
    print('term: abazuri, result: ')
    print(searchAnotiranaRec('abazuri'))
    print('term: радио, result: ')
    print(searchAnotiranaRec('радио'))
    print('term: радијом, result: ')
    print(searchAnotiranaRec('радијом'))
    print('term: abdicirati, pk:2, result: ')
    print(searchAnotiranaRec('abdicirati'))
    print('delete pk:2, oblik: abdicirati')
    deleteAnotiranaRec(2)
    sleep(5)
    print('term: abdicirati, pk:2, result: ')
    print(searchAnotiranaRec('abdicirati'))
    update()
    sleep(5)
    print('term: abazuri, version 2, result: ')
    print(searchAnotiranaRec('abazuri'))
    print('term: радијом, version 2, result: ')
    print(searchAnotiranaRec('радијом'))
