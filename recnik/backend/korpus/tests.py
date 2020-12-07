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

    def test_create_imenica(self):
        # TODO
        req_obj = {
            ''
        }
        pass

    def test_update_imenica(self):
        # TODO
        pass

    def test_concurrent_update_imenica(self):
        # TODO
        pass
