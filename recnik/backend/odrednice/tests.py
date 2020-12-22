import json
from django.test import TestCase, Client
from rest_framework import status
from .models import (Kvalifikator, KvalifikatorOdrednice, Podznacenje,
                     OperacijaIzmene, IzmenaOdrednice, IzrazFraza, Odrednica,
                     Antonim, Sinonim, Kolokacija, RecUKolokaciji, Znacenje)
from django.urls import reverse

KVALIFIKATOR_LIST = reverse('odrednice:kvalifikator-list')
OPERACIJA_IZMENE_LIST = reverse('odrednice:operacija-izmene-list')
IZMENA_ODREDNICE_LIST = reverse('odrednice:izmena-odrednice-list')
KVALIFIKATOR_ODREDNICE_LIST = reverse('odrednice:kvalifikator-odrednice-list')
IZRAZFRAZA_LIST = reverse('odrednice:izrazfraza-list')
ANTONIM_LIST = reverse('odrednice:antonim-list')
SINONIM_LIST = reverse('odrednice:sinonim-list')
KOLOKACIJA_LIST = reverse('odrednice:kolokacija-list')
REC_U_KOLOKACIJI_LIST = reverse('odrednice:rec-u-kolokaciji-list')
ZNACENJE_LIST = reverse('odrednice:znacenje-list')
PODZNACENJE_LIST = reverse('odrednice:podznacenje-list')
ODREDNICA_LIST = reverse('odrednice:odrednica-list')


def get_jwt_token():
    c = Client()
    response = c.post('/api/token/', {'username': 'admin@rsj.rs',
                      'password': 'admin'})
    return json.loads(response.content.decode('UTF-8'))['access']


JSON = 'application/json'


class TestOdredniceApi(TestCase):

    fixtures = ['users', 'odrednice']

    def test_get_kvalikator_by_id(self):
        c = Client()
        prviKvalifikator = Kvalifikator.objects.get(pk=1)
        response = c.get(prviKvalifikator.get_absolute_url(),
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['naziv'], 'prvi kvalifikator')

    def test_get_kvalifikator_list(self):
        c = Client()
        response = c.get(KVALIFIKATOR_LIST,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 2)

    def test_get_kvalikator_odrednice_by_id(self):
        c = Client()
        prviKvalifikatorOdrednice = KvalifikatorOdrednice.objects.get(pk=1)
        response = c.get(prviKvalifikatorOdrednice.get_absolute_url(),
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['redni_broj'], 1)

    def test_get_kvalifikatori_odrednica_list(self):
        c = Client()
        response = c.get(KVALIFIKATOR_ODREDNICE_LIST,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 1)

    def test_get_operacija_izmene_by_id(self):
        c = Client()
        prvaOperacijaIzmene = OperacijaIzmene.objects.get(pk=2)
        response = c.get(prvaOperacijaIzmene.get_absolute_url(),
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['naziv'], 'druga operacija izmene')

    def test_get_operacije_izmena_list(self):
        c = Client()
        response = c.get(OPERACIJA_IZMENE_LIST,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 3)

    def test_get_izmena_odrednice_by_id(self):
        c = Client()
        prvaIzmena = IzmenaOdrednice.objects.get(pk=1)
        response = c.get(prvaIzmena.get_absolute_url(),
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['user_id'], 1)
        self.assertEquals(result['odrednica_id'], 1)
        self.assertEquals(result['operacija_izmene_id'], 2)

    def test_get_izemene_odrednica_list(self):
        c = Client()
        response = c.get(IZMENA_ODREDNICE_LIST,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 2)

    def test_get_izrazfraza_by_id(self):
        c = Client()
        prvaIzrazFraza = IzrazFraza.objects.get(pk=1)
        response = c.get(prvaIzrazFraza.get_absolute_url(),
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['opis'], 'prva izrazFraza')
        self.assertEquals(result['u_vezi_sa_id'], 1)
        self.assertEquals(result['pripada_odrednici_id'], 2)

    def test_get_izrazfraza_list(self):
        c = Client()
        response = c.get(IZRAZFRAZA_LIST,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 2)

    def test_get_antonim_by_id(self):
        c = Client()
        prviAntonim = Antonim.objects.get(pk=1)
        response = c.get(prviAntonim.get_absolute_url(),
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['redni_broj'], 1)
        self.assertEquals(result['ima_antonim_id'], 1)
        self.assertEquals(result['u_vezi_sa_id'], 2)

    def test_get_antonim_list(self):
        c = Client()
        response = c.get(ANTONIM_LIST,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 1)

    def test_get_sinonim_by_id(self):
        c = Client()
        sinonim = Sinonim.objects.get(pk=1)
        response = c.get(sinonim.get_absolute_url(),
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['redni_broj'], 1)
        self.assertEquals(result['ima_sinonim_id'], 2)
        self.assertEquals(result['u_vezi_sa_id'], 1)

    def test_get_sinonim_list(self):
        c = Client()
        response = c.get(ANTONIM_LIST,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 1)

    def test_get_kolokacija_by_id(self):
        c = Client()
        kolokacija = Kolokacija.objects.get(pk=1)
        response = c.get(kolokacija.get_absolute_url(),
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['napomena'], 'test napomena kolokacija')
        self.assertEquals(result['odrednica_id'], 2)

    def test_get_kolacija_list(self):
        c = Client()
        response = c.get(KOLOKACIJA_LIST,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 1)

    def test_get_rec_u_kolokaciji_by_id(self):
        c = Client()
        rec_u_kolokaciji = RecUKolokaciji.objects.get(pk=1)
        response = c.get(rec_u_kolokaciji.get_absolute_url(),
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['redni_broj'], 1)
        self.assertEquals(result['odrednica_id'], 1)
        self.assertEquals(result['kolokacija_id'], 1)

    def test_get_rec_u_kolokaciji_list(self):
        c = Client()
        response = c.get(REC_U_KOLOKACIJI_LIST,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 1)

    def test_get_znacenje_by_id(self):
        c = Client()
        znacenje = Znacenje.objects.get(pk=1)
        response = c.get(znacenje.get_absolute_url(),
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['tekst'], 'tekst znacenja')
        self.assertEquals(result['odrednica_id'], 1)

    def test_get_znacenje_list(self):
        c = Client()
        response = c.get(ZNACENJE_LIST,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 1)

    def test_get_podznacenje_by_id(self):
        c = Client()
        podznacenje = Podznacenje.objects.get(pk=1)
        response = c.get(podznacenje.get_absolute_url(),
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['tekst'], 'tekst podznacenja')
        self.assertEquals(result['znacenje_id'], 1)

    def test_get_podznacenje_list(self):
        c = Client()
        response = c.get(PODZNACENJE_LIST,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 1)

    def test_get_odrednica_by_id(self):
        c = Client()
        odrednica = Odrednica.objects.get(pk=1)
        response = c.get(odrednica.get_absolute_url(),
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['rec'], 'test rec')
        self.assertEquals(result['vrsta'], 0)

    def test_get_odrednica_by_rec(self):
        c = Client()
        response = c.get('/api/odrednice/odrednica/?rec=odrednica',
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result[0]['nastavak'], 'nastavak odrednice')
        self.assertEquals(result[0]['vrsta'], 0)

    def test_get_odrednica_by_rod(self):
        c = Client()
        response = c.get('/api/odrednice/odrednica/?rod=1',
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(result), 2)

    def test_get_odrednica_list(self):
        c = Client()
        response = c.get(ODREDNICA_LIST,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 2)

    def test_create_odrednica(self):
        request_object = {
            'id': 3,
            'rec': 'request object',
            'vrsta': 1,
            'rod': 1,
            'nastavak': 'object nastavak',
            'info': 'ovo je test info za request object',
            'glagolski_vid': 1,
            'glagolski_rod': 1,
            'prezent': 'test prezent',
            'broj_pregleda': 10,
            'stanje': 3,
            'version': 1
        }
        br_izmena = IzmenaOdrednice.objects.filter(odrednica_id=3).count()
        c = Client()
        response = c.post('/api/odrednice/save-odrednica/',
                          data=request_object,
                          HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                          content_type=JSON)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        odrednica = Odrednica.objects.get(id=3)
        self.assertEquals(odrednica.rec, 'request object')
        br_izmena_new = IzmenaOdrednice.objects.filter(odrednica_id=3).count()
        self.assertEquals(br_izmena + 1, br_izmena_new)

    def test_update_odrednica(self):

        request_object = {
            'id': 1,
            'rec': 'реч реч реч',
            'vrsta': 0,
            'rod': 1,
            'nastavak': 'реч',
            'info': 'тест',
            'glagolski_vid': 0,
            'glagolski_rod': 0,
            'prezent': 'реч',
            'broj_pregleda': 1,
            'stanje': 2,
            'version': 1,
            'kolokacija_set': [],
            'recukolokaciji_set': [],
            'znacenje_set': [],
            'kvalifikatorodrednice_set': [],
            'izmenaodrednice_set': []
        }

        br_izmena = IzmenaOdrednice.objects.filter(odrednica_id=1).count()
        c = Client()
        response = c.put('/api/odrednice/save-odrednica/',
                         data=request_object,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        odrednica_updated = Odrednica.objects.get(id=1)
        self.assertEquals(odrednica_updated.rec, 'реч реч реч')
        br_izmena_new = IzmenaOdrednice.objects.filter(odrednica_id=1).count()
        self.assertEquals(br_izmena + 1, br_izmena_new)

    def test_update_odrednica_bez_setova(self):

        request_object = {
            'id': 1,
            'rec': 'test bez',
            'vrsta': 0,
            'rod': 1,
            'nastavak': 'реч',
            'info': 'тест',
            'glagolski_vid': 0,
            'glagolski_rod': 0,
            'prezent': 'реч',
            'broj_pregleda': 1,
            'stanje': 2,
            'version': 1
        }

        br_izmena = IzmenaOdrednice.objects.filter(odrednica_id=1).count()
        c = Client()
        response = c.put('/api/odrednice/save-odrednica/',
                         data=request_object,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        odrednica_updated = Odrednica.objects.get(id=1)
        self.assertEquals(odrednica_updated.rec, 'test bez')
        br_izmena_new = IzmenaOdrednice.objects.filter(odrednica_id=1).count()
        self.assertEquals(br_izmena + 1, br_izmena_new)

    def test_concurrent_update_odrednice(self):
        data_obj1 = {
            'id': 1,
            'rec': 'update 1',
            'vrsta': 0,
            'rod': 1,
            'version': 1
        }
        data_obj2 = {
            'id': 1,
            'rec': 'update 2',
            'vrsta': 0,
            'rod': 1,
            'version': 1
        }
        c1 = Client()
        r1 = c1.put('/api/odrednice/save-odrednica/', data=data_obj1,
                    HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                    content_type=JSON)
        self.assertEquals(r1.status_code, status.HTTP_204_NO_CONTENT)
        c2 = Client()
        r2 = c2.put('/api/odrednice/save-odrednica/', data=data_obj2,
                    HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                    content_type=JSON)
        self.assertEquals(r2.status_code, status.HTTP_409_CONFLICT)
