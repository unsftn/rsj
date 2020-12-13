# -*- coding: utf-8 -*-
import json
from django.test import TestCase, Client
from .models import Imenica, IzmenaImenice, Glagol, IzmenaGlagola, Pridev, IzmenaPrideva


def get_jwt_token():
    c = Client()
    response = c.post('/api/token/', {'username': 'admin@rsj.rs', 'password': 'admin'})
    return json.loads(response.content.decode('UTF-8'))['access']


JSON = 'application/json'


class TestImenicaApi(TestCase):
    fixtures = [
        'users',
        'imenice',
    ]

    def test_find_imenica_by_id(self):
        c = Client()
        response = c.get('/api/korpus/imenica/1/', HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type=JSON)
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(res_obj['nomjed'], 'акценат')

    def test_find_imenica_by_nomjed(self):
        c = Client()
        response = c.get('/api/korpus/imenica/?nomjed=дама', HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(res_obj[0]['genjed'], 'даме')

    def test_find_imenica_by_vrsta_id(self):
        c = Client()
        response = c.get('/api/korpus/imenica/?vrsta_id=2', HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
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
                          HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type=JSON)
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
                          HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type=JSON)
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
                         HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type=JSON)
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
                         content_type=JSON)
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
                    content_type=JSON)
        self.assertEquals(r1.status_code, 204)
        c2 = Client()
        r2 = c2.put('/api/korpus/save-imenica/', data=req2, HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                    content_type=JSON)
        self.assertEquals(r2.status_code, 409)


class TestGlagolApi(TestCase):
    fixtures = [
        'users',
        'glagoli',
    ]

    def test_find_glagol_by_id(self):
        c = Client()
        response = c.get('/api/korpus/glagol/1/', HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type=JSON)
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(res_obj['rgp_zj'], 'блокирала')

    def test_find_glagol_by_infinitiv(self):
        c = Client()
        response = c.get('/api/korpus/glagol/?infinitiv=блокирати', HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(res_obj[0]['rgp_zj'], 'блокирала')

    def test_find_glagol_by_rod(self):
        c = Client()
        response = c.get('/api/korpus/glagol/?rod=1', HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type=JSON)
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertGreaterEqual(len(res_obj), 1)

    def test_create_glagol(self):
        req_obj = {
            'infinitiv': 'прочитати',
            'vid': 2,
            'rod': 1,
            'rgp_mj': 'прочитао',
            'rgp_zj': 'прочитала',
            'rgp_sj': 'прочитало',
            'rgp_mm': 'прочитали',
            'rgp_zm': 'прочитале',
            'rgp_sm': 'прочитала',
            'gpp': '',
            'gps': '',
            'oblici': [{
                'vreme': 1,
                'jd1': 'прочитам',
                'jd2': 'прочиташ',
                'jd3': 'прочита',
                'mn1': 'прочитамо',
                'mn2': 'прочитате',
                'mn3': 'прочитају',
            }, {
                'vreme': 3,
                'jd1': 'прочитах',
                'jd2': 'прочита',
                'jd3': 'прочита',
                'mn1': 'прочитасмо',
                'mn2': 'прочитасте',
                'mn3': 'прочиташе',
            }]
        }
        c = Client()
        response = c.post('/api/korpus/save-glagol/', data=req_obj, HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                          content_type=JSON)
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 201)
        self.assertEquals(res_obj['rgp_sj'], 'прочитало')
        self.assertEquals(res_obj['oblikglagola_set'][0]['mn1'], 'прочитамо')
        broj_izmena = IzmenaGlagola.objects.filter(glagol_id=res_obj['id']).count()
        self.assertEquals(broj_izmena, 1)

    def test_update_glagol(self):
        req_obj = {
            'id': 1,
            'infinitiv': 'блокирати',
            'vid': 2,
            'rod': 1,
            'rgp_mj': 'TEST',
            'rgp_zj': 'блокирала',
            'rgp_sj': 'блокирало',
            'rgp_mm': 'блокирали',
            'rgp_zm': 'блокирале',
            'rgp_sm': 'блокирала',
            'gpp': '',
            'gps': '',
            'version': 1,
            'oblici': [{
                'vreme': 1,
                'jd1': 'блокирам',
                'jd2': 'блокираш',
                'jd3': 'блокира',
                'mn1': 'блокирамо',
                'mn2': 'блокирате',
                'mn3': 'блокирају',
            }, {
                'vreme': 3,
                'jd1': 'блокираћу',
                'jd2': 'блокираћеш',
                'jd3': 'блокираће',
                'mn1': 'блокираћемо',
                'mn2': 'блокираћете',
                'mn3': 'блокираће',
            }]
        }
        broj_izmena_pre = IzmenaGlagola.objects.filter(glagol_id=1).count()
        c = Client()
        response = c.put('/api/korpus/save-glagol/', data=req_obj, HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        self.assertEquals(response.status_code, 204)
        glagol = Glagol.objects.get(id=1)
        self.assertEquals(glagol.rgp_mj, 'TEST')
        self.assertEquals(glagol.oblikglagola_set.get(vreme=3).jd3, 'блокираће')
        broj_izmena_posle = IzmenaGlagola.objects.filter(glagol_id=1).count()
        self.assertEquals(broj_izmena_pre + 1, broj_izmena_posle)

    def test_concurrent_update_glagol(self):
        req1 = {
            'id': 1,
            'rod': 1,
            'vid': 1,
            'rgp_mj': 'TEST1',
            'version': 1,
        }
        req2 = {
            'id': 1,
            'rod': 1,
            'vid': 1,
            'rgp_mj': 'TEST2',
            'version': 1,
        }
        c1 = Client()
        r1 = c1.put('/api/korpus/save-glagol/', data=req1, HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                    content_type=JSON)
        self.assertEquals(r1.status_code, 204)
        c2 = Client()
        r2 = c2.put('/api/korpus/save-glagol/', data=req2, HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                    content_type=JSON)
        self.assertEquals(r2.status_code, 409)


class TestPridevApi(TestCase):
    fixtures = [
        'users',
        'pridevi',
    ]

    def test_find_pridev_by_id(self):
        c = Client()
        response = c.get('/api/korpus/pridev/1/', HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}', content_type=JSON)
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(res_obj['tekst'], 'адаптиран')

    def test_find_pridev_by_tekst(self):
        c = Client()
        response = c.get('/api/korpus/pridev/?tekst=адаптиран', HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(res_obj[0]['tekst'], 'адаптиран')

    def test_create_pridev(self):
        req_obj = {
            'tekst': 'читав',
            'oblici': [{
                'tekst': 'читави',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 1
            }, {
                'tekst': 'читавог',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 2
            }, {
                'tekst': 'читавом',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 3
            }, {
                'tekst': 'читавог',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 4
            }, {
                'tekst': 'читав',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 5
            }, {
                'tekst': 'читавим',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 6
            }, {
                'tekst': 'читавом',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 7
            }, {
                'tekst': 'читави',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 1
            }, {
                'tekst': 'читавих',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 2
            }, {
                'tekst': 'читавим',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 3
            }, {
                'tekst': 'читаве',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 4
            }, {
                'tekst': 'читави',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 5
            }, {
                'tekst': 'читавим',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 6
            }, {
                'tekst': 'читавим',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 7
            }]
        }
        c = Client()
        response = c.post('/api/korpus/save-pridev/', data=req_obj, HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                          content_type=JSON)
        res_obj = json.loads(response.content.decode('UTF-8'))
        self.assertEquals(response.status_code, 201)
        self.assertEquals(res_obj['tekst'], 'читав')
        self.assertEquals(res_obj['oblikprideva_set'][0]['tekst'], 'читави')
        broj_izmena = IzmenaPrideva.objects.filter(pridev_id=res_obj['id']).count()
        self.assertEquals(broj_izmena, 1)

    def test_update_pridev(self):
        req_obj = {
            'id': 1,
            'tekst': 'TEST1',
            'version': 1,
            'oblici': [{
                'tekst': 'TEST2',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 1
            }, {
                'tekst': 'адаптираног',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 2
            }, {
                'tekst': 'адаптираном',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 3
            }, {
                'tekst': 'адаптираног',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 4
            }, {
                'tekst': 'адаптирани',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 5
            }, {
                'tekst': 'адаптираним',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 6
            }, {
                'tekst': 'адаптираном',
                'vid': 1,
                'rod': 1,
                'broj': 1,
                'padez': 7
            }, {
                'tekst': 'адаптирани',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 1
            }, {
                'tekst': 'адаптираних',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 2
            }, {
                'tekst': 'адаптираним',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 3
            }, {
                'tekst': 'адаптиране',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 4
            }, {
                'tekst': 'адаптирани',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 5
            }, {
                'tekst': 'адаптираним',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 6
            }, {
                'tekst': 'адаптираним',
                'vid': 1,
                'rod': 1,
                'broj': 2,
                'padez': 7
            }]
        }
        broj_izmena_pre = IzmenaPrideva.objects.filter(pridev_id=1).count()
        c = Client()
        response = c.put('/api/korpus/save-pridev/', data=req_obj, HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                         content_type=JSON)
        self.assertEquals(response.status_code, 204)
        pridev = Pridev.objects.get(id=1)
        self.assertEquals(pridev.tekst, 'TEST1')
        self.assertEquals(pridev.oblikprideva_set.get(pridev_id=1, vid=1, rod=1, broj=1, padez=1).tekst, 'TEST2')
        broj_izmena_posle = IzmenaPrideva.objects.filter(pridev_id=1).count()
        self.assertEquals(broj_izmena_pre + 1, broj_izmena_posle)

    def test_concurrent_update_pridev(self):
        req1 = {
            'id': 1,
            'tekst': 'TEST1',
            'version': 1,
        }
        req2 = {
            'id': 1,
            'tekst': 'TEST2',
            'version': 1,
        }
        c1 = Client()
        r1 = c1.put('/api/korpus/save-pridev/', data=req1, HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                    content_type=JSON)
        self.assertEquals(r1.status_code, 204)
        c2 = Client()
        r2 = c2.put('/api/korpus/save-pridev/', data=req2, HTTP_AUTHORIZATION=f'Bearer {get_jwt_token()}',
                    content_type=JSON)
        self.assertEquals(r2.status_code, 409)
