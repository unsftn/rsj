# -*- coding: utf-8 -*-
import json
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from odrednice.models import Odrednica
from .renderer import render_slovo, process_tags

JSON = 'application/json'
HTML = 'text/html'


def get_jwt_token():
    c = Client()
    response = c.post('/api/token/', {'username': 'admin@rsj.rs', 'password': 'admin'})
    return json.loads(response.content.decode('UTF-8'))['access']


class RenderPdfTest(TestCase):
    fixtures = [
        'users',
        'renderi',
        'test_odrednice_1',
    ]
    databases = ['default', 'memory']

    def setUp(self) -> None:
        self.token = f'Bearer {get_jwt_token()}'

    def test_render_slovo(self):
        output_file = render_slovo('А', 'pdf')
        self.assertIsNotNone(output_file)

    def test_odrednice_newest(self):
        c = Client()
        r = c.get('/api/render/odrednice/newest/10/', HTTP_AUTHORIZATION=self.token, content_type=HTML)
        soup = BeautifulSoup(r.content.decode('UTF-8'), 'html.parser')
        self.assertEqual(len(soup.contents), 10)

    def test_odrednice_latest(self):
        c = Client()
        r = c.get('/api/render/odrednice/latest/10/', HTTP_AUTHORIZATION=self.token, content_type=HTML)
        soup = BeautifulSoup(r.content.decode('UTF-8'), 'html.parser')
        self.assertEqual(len(soup.contents), 10)

    def test_odrednice_popular(self):
        c = Client()
        r = c.get('/api/render/odrednice/popular/10/', HTTP_AUTHORIZATION=self.token, content_type=HTML)
        soup = BeautifulSoup(r.content.decode('UTF-8'), 'html.parser')
        self.assertEqual(len(soup.contents), 10)

    def test_render_styling_1(self):
        test_znacenje = 'зељаста @биљка@ с белим звонастим висећим цветовима #Galantus Nivalis# из ф. љиљана (#Amaryllidaceae#), која цвета у рано пролеће'
        expected_html = 'зељаста <b>биљка</b> с белим звонастим висећим цветовима <i>Galantus Nivalis</i> из ф. љиљана (<i>Amaryllidaceae</i>), која цвета у рано пролеће'
        test_html = process_tags(test_znacenje, False)
        self.assertEqual(test_html, expected_html)
