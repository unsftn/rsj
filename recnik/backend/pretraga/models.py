from django.db import models
from django.db.models import IntegerField, CharField
from elasticsearch_dsl import Document, analyzer, Keyword, SearchAsYouType, Text


class OdrednicaDocument(Document):
    pk = Keyword()
    rec = Keyword()
    varijante = SearchAsYouType(analyzer=analyzer('serbian'))
    vrsta = Keyword()


class OdrednicaResponse(models.Model):
    rec = CharField(max_length=50)
    vrsta = IntegerField()


class KorpusDocument(Document):
    pk = Keyword()
    osnovniOblik = Keyword()
    oblici = Text(analyzer=analyzer('serbian'))


class KorpusResponse(models.Model):
    osnovniOblik = CharField(max_length=50)
