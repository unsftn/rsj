# -*- coding: utf-8 -*-
import json
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client
from .admin import *


def get_jwt_token():
    c = Client()
    response = c.post('/api/token/', {'username': 'admin@rsj.rs', 'password': 'admin'})
    return json.loads(response.content.decode('UTF-8'))['access']


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


class TestPublikacijaApi(TestCase):
    fixtures = [
        'users',
        'vrste_publikacija',
        'publikacije',
    ]

    def setUp(self) -> None:
        self.create_pub_obj = {
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
            'user_id': 1,
            # izostavi polja koja nemaju vrednost
            # 'isbn': '',
            # 'volumen': '',
        }

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
        response = c.post('/api/publikacije/create-publikacija/', data=self.create_pub_obj,
                          HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type='application/json')
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        try:
            pub = Publikacija.objects.get(naslov='Druga glasnost')
            self.assertEquals('https://www.vreme.com/cms/view.php?id=1086777', pub.url)
        except Publikacija.DoesNotExist:
            self.fail('Publikacija not saved')

    def test_create_tekst(self):
        c = Client()
        token = get_jwt_token()
        response = c.post('/api/publikacije/create-publikacija/', data=self.create_pub_obj,
                          HTTP_AUTHORIZATION=f'Bearer {token}', content_type='application/json')
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        pub_id = res_obj['id']
        req_obj = {
            'publikacija_id': pub_id,
            'tekst': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla vehicula tellus vel arcu imperdiet, auctor lacinia risus porttitor. In orci ex, consequat at convallis ac, blandit eget ante.'
        }
        response = c.post('/api/publikacije/create-text/', data=req_obj, HTTP_AUTHORIZATION=f'Bearer {token}',
                          content_type='application/json')
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(TekstPublikacije.objects.filter(id=res_obj['id']).count(), 1)
