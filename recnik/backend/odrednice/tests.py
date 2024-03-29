import json
from django.urls import reverse
from django.test import TestCase, Client
from rest_framework import status
from .models import *

KVALIFIKATOR_LIST = reverse('odrednice:kvalifikator-list')
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
ODREDNICA_LATEST_LIST = reverse('odrednice:odrednica-latest-list')
ODREDNICA_CHANGED_LIST = reverse('odrednice:odrednica-changed-list')
ODREDNICA_POPULAR_LIST = reverse('odrednice:odrednica-popular-list')

JSON = 'application/json'


def get_jwt_token():
    c = Client()
    response = c.post('/api/token/', {'username': 'admin@rsj.rs', 'password': 'admin'})
    return json.loads(response.content.decode('UTF-8'))['access']


class TestOdredniceApi(TestCase):
    fixtures = ['users', 'kvalifikatori', 'operacije-izmene', 'odrednice']
    databases = ['default', 'memory']

    def setUp(self) -> None:
        self.token = f'Bearer {get_jwt_token()}'
        self.big_request_object = {
            'rec': 'а',
            'ijekavski': '',
            'vrsta': 8,
            'nastavak': '',
            'info': 'углавном супр. значења',
            'prezent': '',
            'stanje': 1,
            'varijante': [],
            'rbr_homonima': None,
            'znacenja': [{
                'redni_broj': 1,
                'tekst': '',
                'znacenje_se': False,
                'podznacenja': [{
                    'redni_broj': 1,
                    'tekst': 'повезује реченице или реченичке чланове, делове супротног значења',
                }, {
                    'redni_broj': 2,
                    'tekst': '(са везн. ”да” и негацијом) за искључивање онога што се логички очекује',
                }],
            }, {
                'redni_broj': 2,
                'tekst': '',
                'znacenje_se': False,
                'podznacenja': [{
                    'redni_broj': 1,
                    'tekst': 'за повезивање, прикључивање реченица или реченичких делова различитог садржаја',
                }, {
                    'redni_broj': 2,
                    'tekst': 'за исказивање нечег неочекиваног',
                }, {
                    'redni_broj': 3,
                    'tekst': 'за повезивање са претходно изложеним (у причању, дијалогу, у питањима, при преласку на нову мисао) или уз објашњење (у уметнутој реченици)',
                }],
            }, {
                'redni_broj': 3,
                'tekst': 'за појачавање, истицање',
                'znacenje_se': False,
                'podznacenja': [{
                    'redni_broj': 1,
                    'tekst': 'у погодбеним или допусним реченицама',
                }, {
                    'redni_broj': 2,
                    'tekst': 'у допусним, изјавним реченицама са негацијом',
                }],
            }, {
                'redni_broj': 4,
                'tekst': 'у спрегама: а камоли, а некмоли, а не при поређењу, за истицање',
                'znacenje_se': False,
                'podznacenja': [],
            }]
        }
        self.test_kvalifikator = {
            'redni_broj': 1,
            'kvalifikator_id': 4
        }
        self.test_izraz_fraza_1 = {
            'redni_broj': 1,
            'opis': 'бела кафа'
        }
        self.test_izraz_fraza_2 = {
            'redni_broj': 2,
            'opis': 'флагрантно кршење људских права'
        }
        self.konkordansa_1 = {
            'redni_broj': 1,
            'opis': 'текст конкордансе 1...',
            'publikacija_id': 1
        }
        self.konkordansa_2 = {
            'redni_broj': 2,
            'opis': 'текст конкордансе 2...',
            'publikacija_id': 2
        }
        self.sinonim_1 = {
            'redni_broj': 1,
            'sinonim_id': 2,
            'tekst': ''
        }
        self.sinonim_2 = {
            'redni_broj': 2,
            'sinonim_id': 1,
            'tekst': ''
        }
        self.antonim_1 = {
            'redni_broj': 1,
            'antonim_id': 2,
            'tekst': ''
        }
        self.antonim_2 = {
            'redni_broj': 2,
            'antonim_id': 1,
            'tekst': ''
        }

    def test_get_kvalikator_by_id(self):
        c = Client()
        prviKvalifikator = Kvalifikator.objects.get(pk=1)
        response = c.get(prviKvalifikator.get_absolute_url(), HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['naziv'], 'prvi kvalifikator')

    def test_get_kvalifikator_list(self):
        c = Client()
        response = c.get(KVALIFIKATOR_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 192)

    def test_get_kvalikator_odrednice_by_id(self):
        c = Client()
        prviKvalifikatorOdrednice = KvalifikatorOdrednice.objects.get(pk=1)
        response = c.get(prviKvalifikatorOdrednice.get_absolute_url(), HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['redni_broj'], 1)

    def test_get_kvalifikatori_odrednica_list(self):
        c = Client()
        response = c.get(KVALIFIKATOR_ODREDNICE_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 1)

    def test_get_izmena_odrednice_by_id(self):
        c = Client()
        prvaIzmena = IzmenaOdrednice.objects.get(pk=1)
        response = c.get(prvaIzmena.get_absolute_url(), HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['user']['id'], 1)
        self.assertEquals(result['odrednica_id'], 1)
        self.assertEquals(result['operacija_izmene']['id'], 1)

    def test_get_izemene_odrednica_list(self):
        c = Client()
        response = c.get(IZMENA_ODREDNICE_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 2)

    def test_get_izrazfraza_by_id(self):
        c = Client()
        prvaIzrazFraza = IzrazFraza.objects.get(pk=1)
        response = c.get(prvaIzrazFraza.get_absolute_url(), HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['opis'], 'prva izrazFraza')
        self.assertEquals(result['odrednica_id'], 1)
        self.assertEquals(result['redni_broj'], 1)

    def test_get_izrazfraza_list(self):
        c = Client()
        response = c.get(IZRAZFRAZA_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 2)

    # def test_get_antonim_by_id(self):
    #     c = Client()
    #     prviAntonim = Antonim.objects.get(pk=1)
    #     response = c.get(prviAntonim.get_absolute_url(), HTTP_AUTHORIZATION=self.token, content_type=JSON)
    #     result = json.loads(response.content.decode('UTF-8'))
    #     self.assertEquals(response.status_code, status.HTTP_200_OK)
    #     self.assertEquals(result['redni_broj'], 1)
    #     self.assertEquals(result['ima_antonim_id'], 1)
    #     self.assertEquals(result['u_vezi_sa_id'], 2)

    # def test_get_antonim_list(self):
    #     c = Client()
    #     response = c.get(ANTONIM_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
    #     result = json.loads(response.content.decode('UTF-8'))
    #     self.assertEquals(response.status_code, status.HTTP_200_OK)
    #     self.assertEquals(len(result), 1)

    # def test_get_sinonim_by_id(self):
    #     c = Client()
    #     sinonim = Sinonim.objects.get(pk=1)
    #     response = c.get(sinonim.get_absolute_url(), HTTP_AUTHORIZATION=self.token, content_type=JSON)
    #     result = json.loads(response.content.decode('UTF-8'))
    #     self.assertEquals(response.status_code, status.HTTP_200_OK)
    #     self.assertEquals(result['redni_broj'], 1)
    #     self.assertEquals(result['ima_sinonim_id'], 2)
    #     self.assertEquals(result['u_vezi_sa_id'], 1)

    # def test_get_sinonim_list(self):
    #     c = Client()
    #     response = c.get(ANTONIM_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
    #     result = json.loads(response.content.decode('UTF-8'))
    #     self.assertEquals(response.status_code, status.HTTP_200_OK)
    #     self.assertEquals(len(result), 1)

    def test_get_kolokacija_by_id(self):
        c = Client()
        kolokacija = Kolokacija.objects.get(pk=1)
        response = c.get(kolokacija.get_absolute_url(), HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['napomena'], 'test napomena kolokacija')
        self.assertEquals(result['odrednica_id'], 2)

    def test_get_kolacija_list(self):
        c = Client()
        response = c.get(KOLOKACIJA_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 1)

    def test_get_rec_u_kolokaciji_by_id(self):
        c = Client()
        rec_u_kolokaciji = RecUKolokaciji.objects.get(pk=1)
        response = c.get(rec_u_kolokaciji.get_absolute_url(), HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['redni_broj'], 1)
        self.assertEquals(result['odrednica_id'], 1)
        self.assertEquals(result['kolokacija_id'], 1)

    def test_get_rec_u_kolokaciji_list(self):
        c = Client()
        response = c.get(REC_U_KOLOKACIJI_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 1)

    def test_get_znacenje_by_id(self):
        c = Client()
        znacenje = Znacenje.objects.get(pk=1)
        response = c.get(znacenje.get_absolute_url(), HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['tekst'], 'tekst znacenja')
        self.assertEquals(result['odrednica_id'], 1)

    def test_get_znacenje_list(self):
        c = Client()
        response = c.get(ZNACENJE_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 1)

    def test_get_podznacenje_by_id(self):
        c = Client()
        podznacenje = Podznacenje.objects.get(pk=1)
        response = c.get(podznacenje.get_absolute_url(), HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['tekst'], 'tekst podznacenja')
        self.assertEquals(result['znacenje_id'], 1)

    def test_get_podznacenje_list(self):
        c = Client()
        response = c.get(PODZNACENJE_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 1)

    def test_get_odrednica_by_id(self):
        c = Client()
        odrednica = Odrednica.objects.get(pk=1)
        response = c.get(odrednica.get_absolute_url(), HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(result['rec'], 'test rec')
        self.assertEquals(result['vrsta'], 0)

    # def test_get_odrednica_by_rec(self):
    #     c = Client()
    #     response = c.get('/api/odrednice/odrednica/?rec=odrednica', HTTP_AUTHORIZATION=self.token, content_type=JSON)
    #     result = json.loads(response.content.decode('UTF-8'))
    #     self.assertEquals(response.status_code, status.HTTP_200_OK)
    #     self.assertEquals(result[0]['nastavak'], 'nastavak odrednice')
    #     self.assertEquals(result[0]['vrsta'], 0)

    def test_get_odrednica_by_rod(self):
        c = Client()
        response = c.get('/api/odrednice/odrednica/?rod=1', HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(result), 2)
        response = c.get('/api/odrednice/odrednica/?rod=2', HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(result), 0)

    def test_get_odrednica_list(self):
        c = Client()
        response = c.get(ODREDNICA_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 2)

    def test_get_odrednice_latest(self):
        c = Client()
        response = c.get(ODREDNICA_LATEST_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0]['rec'], 'odrednica')

    def test_get_odrednice_last_changed(self):
        c = Client()
        response = c.get(ODREDNICA_CHANGED_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0]['rec'], 'odrednica')

    def test_get_odrednice_popular(self):
        c = Client()
        response = c.get(ODREDNICA_POPULAR_LIST, HTTP_AUTHORIZATION=self.token, content_type=JSON)
        result = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0]['rec'], 'test rec')

    def test_create_odrednica_osnovni(self):
        request_object = {
            'rec': 'request object',
            'vrsta': 1,
            'rod': 1,
            'nastavak': 'object nastavak',
            'info': 'ovo je test info za request object',
            'glagolski_vid': 1,
            'glagolski_rod': 1,
            'prezent': 'test prezent',
            'stanje': 3,
            'version': 1,
            'varijante': [],
            'znacenja': []
        }
        br_izmena = IzmenaOdrednice.objects.filter(odrednica_id=3).count()
        c = Client()
        response = c.post('/api/odrednice/save/', data=request_object, HTTP_AUTHORIZATION=self.token,
                          content_type=JSON)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        odrednica = Odrednica.objects.get(rec='request object')
        self.assertEquals(odrednica.info, 'ovo je test info za request object')
        br_izmena_new = IzmenaOdrednice.objects.filter(odrednica_id=odrednica.id).count()
        self.assertEquals(br_izmena + 1, br_izmena_new)

    def save_big_odrednica(self):
        c = Client()
        response = c.post('/api/odrednice/save/', data=self.big_request_object, HTTP_AUTHORIZATION=self.token,
                          content_type=JSON)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        odrednica_id = json.loads(response.content.decode('utf-8'))['id']
        odrednica = Odrednica.objects.get(id=odrednica_id)
        self.assertEquals(odrednica.info, 'углавном супр. значења')
        br_izmena = IzmenaOdrednice.objects.filter(odrednica_id=odrednica.id).count()
        self.assertEquals(br_izmena, 1)
        return odrednica

    def test_create_odrednica_znacenja(self):
        self.save_big_odrednica()

    def test_create_odrednica_kvalifikatori_odrednice(self):
        self.big_request_object['kvalifikatori'] = [self.test_kvalifikator]
        odrednica = self.save_big_odrednica()
        self.assertEquals(odrednica.kvalifikatorodrednice_set.count(), 1)

    def test_create_odrednica_kvalifikatori_znacenja(self):
        self.big_request_object['znacenja'][0]['kvalifikatori'] = [self.test_kvalifikator]
        odrednica = self.save_big_odrednica()
        self.assertEquals(odrednica.znacenje_set.get(redni_broj=1).kvalifikatorznacenja_set.count(), 1)

    def test_create_odrednica_kvalifikatori_podznacenja(self):
        self.big_request_object['znacenja'][0]['podznacenja'][0]['kvalifikatori'] = [self.test_kvalifikator]
        odrednica = self.save_big_odrednica()
        self.assertEquals(odrednica.znacenje_set.get(redni_broj=1).podznacenje_set.get(redni_broj=1).kvalifikatorpodznacenja_set.count(), 1)

    def test_create_odrednica_izrazi_fraze(self):
        self.big_request_object['izrazi_fraze'] = [self.test_izraz_fraza_1, self.test_izraz_fraza_2]
        odrednica = self.save_big_odrednica()
        self.assertEquals(odrednica.izrazfraza_set.get(redni_broj=1).opis, 'бела кафа')

    def test_create_odrednica_znacenje_izrazi_fraze(self):
        self.big_request_object['znacenja'][0]['izrazi_fraze'] = [self.test_izraz_fraza_1, self.test_izraz_fraza_2]
        odrednica = self.save_big_odrednica()
        self.assertEquals(odrednica.znacenje_set.get(redni_broj=1).izrazfraza_set.get(redni_broj=1).opis, 'бела кафа')

    def test_create_odrednica_podznacenje_izrazi_fraze(self):
        self.big_request_object['znacenja'][0]['podznacenja'][0]['izrazi_fraze'] = [self.test_izraz_fraza_1, self.test_izraz_fraza_2]
        odrednica = self.save_big_odrednica()
        self.assertEquals(odrednica.znacenje_set.get(redni_broj=1).podznacenje_set.get(redni_broj=1).izrazfraza_set.get(redni_broj=1).opis, 'бела кафа')

    def test_create_odrednica_znacenje_konkordansa(self):
        self.big_request_object['znacenja'][0]['konkordanse'] = [self.konkordansa_1, self.konkordansa_2]
        odrednica = self.save_big_odrednica()
        self.assertEquals(odrednica.znacenje_set.get(redni_broj=1).konkordansa_set.get(redni_broj=1).opis, 'текст конкордансе 1...')

    def test_create_odrednica_podznacenje_konkordansa(self):
        self.big_request_object['znacenja'][0]['podznacenja'][0]['konkordanse'] = [self.konkordansa_1, self.konkordansa_2]
        odrednica = self.save_big_odrednica()
        self.assertEquals(odrednica.znacenje_set.get(redni_broj=1).podznacenje_set.get(redni_broj=1).konkordansa_set.get(redni_broj=1).opis, 'текст конкордансе 1...')

    # def test_create_odrednica_sinonim(self):
    #     self.big_request_object['sinonimi'] = [self.sinonim_1]
    #     odrednica = self.save_big_odrednica()
    #     self.assertEquals(odrednica.ima_sinonim.get(redni_broj=1).ima_sinonim.id, odrednica.id)
    #     self.assertEquals(odrednica.ima_sinonim.get(redni_broj=1).u_vezi_sa.id, 2)

    # def test_create_odrednica_antonim(self):
    #     self.big_request_object['antonimi'] = [self.antonim_1]
    #     odrednica = self.save_big_odrednica()
    #     self.assertEquals(odrednica.ima_antonim.get(redni_broj=1).ima_antonim.id, odrednica.id)
    #     self.assertEquals(odrednica.ima_antonim.get(redni_broj=1).u_vezi_sa.id, 2)

    def xtest_concurrent_update_odrednice(self):
        # TODO: treba da uzme u obzir prava pristupa odrednici
        odr1 = Odrednica.objects.get(pk=1)
        odr2 = Odrednica.objects.get(pk=1)

        data_obj1 = {
            'id': odr1.id,
            'rec': 'update 1',
            'vrsta': odr1.vrsta,
            'rod': odr1.rod,
            'version': odr1.version,
            'znacenja': [],
            'stanje': 1,
        }
        data_obj2 = {
            'id': odr2.id,
            'rec': 'update 2',
            'vrsta': odr2.vrsta,
            'rod': odr2.rod,
            'version': odr2.version,
            'znacenja': [],
            'stanje': 1,
        }
        c1 = Client()
        r1 = c1.put('/api/odrednice/save/', data=data_obj1, HTTP_AUTHORIZATION=self.token,
                    content_type=JSON)
        self.assertEquals(r1.status_code, status.HTTP_204_NO_CONTENT)
        c2 = Client()
        r2 = c2.put('/api/odrednice/save/', data=data_obj2, HTTP_AUTHORIZATION=self.token,
                    content_type=JSON)
        self.assertEquals(r2.status_code, status.HTTP_409_CONFLICT)

    def xtest_update_odrednica(self):
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
        response = c.put('/api/odrednice/save/', data=request_object, HTTP_AUTHORIZATION=self.token,
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
            'stanje': 2,
            'znacenja': []
        }

        br_izmena = IzmenaOdrednice.objects.filter(odrednica_id=1).count()
        c = Client()
        response = c.put('/api/odrednice/save/', data=request_object, HTTP_AUTHORIZATION=self.token,
                         content_type=JSON)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        odrednica_updated = Odrednica.objects.get(id=1)
        self.assertEquals(odrednica_updated.rec, 'test bez')
        br_izmena_new = IzmenaOdrednice.objects.filter(odrednica_id=1).count()
        self.assertEquals(br_izmena + 1, br_izmena_new)
