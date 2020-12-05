import json
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client
from .admin import *


class TestPublikacijaAdmin(TestCase):
    fixtures = [
        'vrste_publikacija',
        'publikacije',
    ]

    def setUp(self) -> None:
        self.publikacija_admin = PublikacijaAdmin(model=Publikacija, admin_site=AdminSite())

    def test_find_by_id(self):
        result = PublikacijaAdmin.get_search_results(self.publikacija_admin, None, Publikacija.objects.all(), "1")
        self.assertGreaterEqual(result[0].distinct().count(), 1)

    def test_find_by_naslov_izdanja(self):
        result = PublikacijaAdmin.get_search_results(self.publikacija_admin, None, Publikacija.objects.all(), "Hag")
        self.assertEquals(result[0].distinct().count(), 1)
        result = PublikacijaAdmin.get_search_results(self.publikacija_admin, None, Publikacija.objects.all(), "Zavisi")
        self.assertEquals(result[0].distinct().count(), 1)


def get_jwt_token():
    c = Client()
    response = c.post('/api/token/', {'username': 'admin@rsj.rs', 'password': 'admin'})
    return json.loads(response.content.decode('UTF-8'))['access']


class TestPublikacijaApi(TestCase):
    fixtures = [
        'vrste_publikacija',
        'publikacije',
        'users',
    ]

    def test_find_by_id(self):
        c = Client()
        response = c.get('/api/publikacije/publikacija/1/', HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type='application/json')
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(res_obj['naslov'], 'Zavisi od inflacije')

    def test_find_by_naslov_izdanja(self):
        c = Client()
        response = c.get('/api/publikacije/publikacija/?naslov_izdanja=Vreme',
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type='application/json')
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(res_obj), 2)

    def test_create_publikacija(self):
        c = Client()
        req_obj = {
            'naslov': 'Druga glasnost',
            'naslov_izdanja': 'Vreme',
            'issn': '03538028',
            'izdavac': 'Vreme, Beograd',
            'godina': '2012',
            'broj': '1144',
            'url': 'https://www.vreme.com/cms/view.php?id=1086777',
            'vrsta_id': 3,
            'autori': [{
                'ime': 'Dragan',
                'prezime': 'Kremer'
            }],
            # izostavi polja koja nemaju vrednost
            # 'isbn': '',
            # 'volumen': '',
        }
        response = c.post('/api/publikacije/create-publikacija/', data=req_obj,
                          HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type='application/json')
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        try:
            pub = Publikacija.objects.get(naslov='Druga glasnost')
            self.assertEquals('https://www.vreme.com/cms/view.php?id=1086777', pub.url)
        except Publikacija.DoesNotExist:
            self.fail('Publikacija not saved')
