# -*- coding: utf-8 -*-
from django.test import TestCase
from odrednice.models import Odrednica
from .renderer import render_one, render_slovo


class RenderPdfTest(TestCase):
    fixtures = [
        'renderi',
        'test_odrednice_1',
    ]

    def setUp(self) -> None:
        pass

    def xtest_render_one(self):
        from .views import FAKE_ODREDNICE
        odrednice = [FAKE_ODREDNICE[key] for key in sorted(FAKE_ODREDNICE.keys())]
        result = render_one(odrednice[0])
        self.assertGreaterEqual(len(result), 1)

    def test_render_slovo(self):
        odrednice = Odrednica.objects.filter(rec__startswith='а')
        output_file = render_slovo(odrednice, 'А')
        self.assertIsNotNone(output_file)
