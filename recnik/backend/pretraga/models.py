# from django.db import models
# from django.db.models import IntegerField, CharField
# from elasticsearch_dsl import Document, analyzer, Keyword, SearchAsYouType, Text


# class OdrednicaDocument(Document):
#     pk = Keyword()
#     rec = Keyword()
#     varijante = SearchAsYouType()  # analyzer=SERBIAN_ANALYZER
#     vrsta = Keyword()
#     rbr_homo = Keyword()
#     status = Keyword()


# class OdrednicaResponse(models.Model):
#     rec = CharField(max_length=50)
#     vrsta = IntegerField()
#     rbr_homo = IntegerField(null=True)


# class KorpusDocument(Document):
#     pk = Keyword()
#     osnovniOblik = Keyword()
#     oblici = Text()  # analyzer=SERBIAN_ANALYZER


# class KorpusResponse(models.Model):
#     osnovniOblik = CharField(max_length=50)


# class PublikacijaDocument(Document):
#     pk = Keyword()
#     skracenica = Keyword()
#     naslov = Keyword()
#     tekst = SearchAsYouType()
