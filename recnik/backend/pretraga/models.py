from django.db import models
from django.db.models import IntegerField, CharField
from elasticsearch_dsl import Document, analyzer, Keyword, SearchAsYouType, Text
from .config import *


class OdrednicaDocument(Document):
    pk = Keyword()
    rec = Keyword()
    varijante = SearchAsYouType()  # analyzer=SERBIAN_ANALYZER
    vrsta = Keyword()


class OdrednicaResponse(models.Model):
    rec = CharField(max_length=50)
    vrsta = IntegerField()


class KorpusDocument(Document):
    pk = Keyword()
    osnovniOblik = Keyword()
    oblici = Text()  # analyzer=SERBIAN_ANALYZER


class KorpusResponse(models.Model):
    osnovniOblik = CharField(max_length=50)
