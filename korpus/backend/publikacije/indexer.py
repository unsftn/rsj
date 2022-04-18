# import logging
# from elasticsearch_dsl import analyzer, Index, Document, Keyword, SearchAsYouType, Search  # , Text
#
# log = logging.getLogger(__name__)
#
# SERBIAN_ANALYZER = analyzer('serbian')
# PUB_INDEX = 'publikacije'
# ALL_INDEXES = [
#     {'index': PUB_INDEX, 'document': PublikacijaDocument},
# ]
#
# def check_elasticsearch():
#     try:
#         r = requests.get(f'http://{settings.ELASTICSEARCH_HOST}:9200/')
#         if r.status_code != 200:
#             return False
#         json = r.json()
#         if not json['version']['number']:
#             return False
#         if int(json['version']['number'].split('.')[0]) < 7:
#             return False
#         return True
#     except requests.exceptions.ConnectionError:
#         return False
#
#
# def create_index_if_needed():
#     try:
#         for es_idx in ALL_INDEXES:
#             if not connections.get_connection().indices.exists(es_idx['index']):
#                 idx = Index(es_idx['index'])
#                 idx.analyzer(SERBIAN_ANALYZER)
#                 idx.document(es_idx['document'])
#                 idx.create()
#     except Exception as ex:
#         log.fatal(ex)
#
#
# def recreate_index():
#     try:
#         for es_idx in ALL_INDEXES:
#             if connections.get_connection().indices.exists(es_idx['index']):
#                 connections.get_connection().indices.delete(es_idx['index'])
#         create_index_if_needed()
#     except Exception as ex:
#         log.fatal(ex)
