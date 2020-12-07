# -*- coding: utf-8 -*-
import json
from django.test import TestCase, Client
from .models import Imenica, IzmenaImenice

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
        broj_izmena = IzmenaImenice.objects.filter(imenica_id=res_obj['id']).count()
        self.assertEquals(broj_izmena, 1)

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
        broj_izmena = IzmenaImenice.objects.filter(imenica_id=res_obj['id']).count()
        self.assertEquals(broj_izmena, 1)

    def test_update_imenica_bez_varijanti(self):
        req_obj = {
            'id': 1,
            'vrsta_id': 1,
            'nomjed': 'PROBA',
            'genjed': 'акцента',
            'datjed': 'акценту',
            'akujed': 'акценат',
            'vokjed': 'акценту',
            'insjed': 'акцентом',
            'lokjed': 'акценту',
            'nommno': 'акценти',
            'genmno': 'акцената',
            'datmno': 'акцентима',
            'akumno': 'акценте',
            'vokmno': 'акценти',
            'insmno': 'акцентима',
            'lokmno': 'акцентима',
            'version': 1
        }
        broj_izmena_pre = IzmenaImenice.objects.filter(imenica_id=1).count()
        c = Client()
        response = c.put('/api/korpus/save-imenica/', data=req_obj,
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type='application/json')
        self.assertEquals(response.status_code, 204)
        imenica = Imenica.objects.get(id=1)
        self.assertEquals(imenica.nomjed, 'PROBA')
        broj_izmena_posle = IzmenaImenice.objects.filter(imenica_id=1).count()
        self.assertEquals(broj_izmena_pre + 1, broj_izmena_posle)

    def test_update_imenica_sa_varijantama(self):
        req_obj = {
            'id': 1,
            'vrsta_id': 1,
            'nomjed': 'TEST',
            'genjed': 'акцента',
            'datjed': 'акценту',
            'akujed': 'акценат',
            'vokjed': 'акценту',
            'insjed': 'акцентом',
            'lokjed': 'акценту',
            'nommno': 'акценти',
            'genmno': 'акцената',
            'datmno': 'акцентима',
            'akumno': 'акценте',
            'vokmno': 'акценти',
            'insmno': 'акцентима',
            'lokmno': 'акцентима',
            'version': 1,
            'varijante': [{
                'nomjed': '',
                'genjed': '',
                'datjed': 'PROBA',
                'akujed': '',
                'vokjed': '',
                'insjed': '',
                'lokjed': '',
                'nommno': '',
                'genmno': '',
                'datmno': '',
                'akumno': '',
                'vokmno': '',
                'insmno': '',
                'lokmno': '',
            }]
        }
        broj_izmena_pre = IzmenaImenice.objects.filter(imenica_id=1).count()
        c = Client()
        response = c.put('/api/korpus/save-imenica/', data=req_obj, HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type='application/json')
        self.assertEquals(response.status_code, 204)
        imenica = Imenica.objects.get(id=1)
        self.assertEquals(imenica.nomjed, 'TEST')
        self.assertEquals(imenica.varijantaimenice_set.get(redni_broj=1).datjed, 'PROBA')
        broj_izmena_posle = IzmenaImenice.objects.filter(imenica_id=1).count()
        self.assertEquals(broj_izmena_pre + 1, broj_izmena_posle)

    def test_concurrent_update_imenica(self):
        req1 = {
            'id': 1,
            'vrsta_id': 1,
            'nomjed': 'TEST1',
            'version': 1,
        }
        req2 = {
            'id': 1,
            'vrsta_id': 1,
            'nomjed': 'TEST2',
            'version': 1,
        }
        c1 = Client()
        r1 = c1.put('/api/korpus/save-imenica/', data=req1, HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                    content_type='application/json')
        self.assertEquals(r1.status_code, 204)
        c2 = Client()
        r2 = c2.put('/api/korpus/save-imenica/', data=req2, HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                    content_type='application/json')
        self.assertEquals(r2.status_code, 409)

