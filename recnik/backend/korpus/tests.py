# -*- coding: utf-8 -*-
import json
from django.test import TestCase, Client


def get_jwt_token():
    c = Client()
    response = c.post('/api/token/', {'username': 'admin@rsj.rs', 'password': 'admin'})
    return json.loads(response.content.decode('UTF-8'))['access']


class TestImenicaApi(TestCase):
    fixtures = [
        'users',
        'imenice',
    ]

    def test_find_imenica_by_id(self):
        c = Client()
        response = c.get('/api/korpus/imenica/1/', HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type='application/json')
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(res_obj['nomjed'], 'акценат')

    def test_find_imenica_by_nomjed(self):
        c = Client()
        response = c.get('/api/korpus/imenica/?nomjed=дама', HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type='application/json')
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(res_obj[0]['genjed'], 'даме')

    def test_find_imenica_by_vrsta_id(self):
        c = Client()
        response = c.get('/api/korpus/imenica/?vrsta_id=2', HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type='application/json')
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertGreaterEqual(len(res_obj), 2)

    def test_create_imenica_bez_varijanti(self):
        req_obj = {
            'vrsta_id': 2,
            'nomjed': 'столица',
            'genjed': 'столице',
            'datjed': 'столици',
            'akujed': 'столицу',
            'vokjed': 'столице',
            'insjed': 'столицом',
            'lokjed': 'столици',
            'nommno': 'столице',
            'genmno': 'столица',
            'datmno': 'столицама',
            'akumno': 'столице',
            'vokmno': 'столице',
            'insmno': 'столицама',
            'lokmno': 'столицама',
        }
        c = Client()
        response = c.post('/api/korpus/save-imenica/', data=req_obj,
                          HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type='application/json')
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 201)
        self.assertEquals(res_obj['nomjed'], 'столица')

    def test_create_imenica_sa_varijantama(self):
        req_obj = {
            'vrsta_id': 2,
            'nomjed': 'отац',
            'genjed': 'оца',
            'datjed': 'оцу',
            'akujed': 'оца',
            'vokjed': 'оче',
            'insjed': 'оцем',
            'lokjed': 'оцу',
            'nommno': 'очеви',
            'genmno': 'очева',
            'datmno': 'очевима',
            'akumno': 'oчева',
            'vokmno': 'очеви',
            'insmno': 'очевима',
            'lokmno': 'очевима',
            'varijante': [{
                'nomjed': '',
                'genjed': '',
                'datjed': '',
                'akujed': '',
                'vokjed': '',
                'insjed': '',
                'lokjed': '',
                'nommno': 'оци',
                'genmno': 'отаца',
                'datmno': 'оцима',
                'akumno': 'оце',
                'vokmno': 'оци',
                'insmno': 'оцима',
                'lokmno': 'оцима',
            }]
        }
        c = Client()
        response = c.post('/api/korpus/save-imenica/', data=req_obj,
                          HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type='application/json')
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 201)
        self.assertEquals(res_obj['nomjed'], 'отац')
        self.assertEquals(res_obj['varijantaimenice_set'][0]['nommno'], 'оци')

    def test_update_imenica(self):
        # TODO
        pass

    def test_concurrent_update_imenica(self):
        # TODO
        pass
