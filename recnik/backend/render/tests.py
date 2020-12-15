from django.test import TestCase


class RenderPdfTest(TestCase):
    fixtures = [
        'renderi',
    ]

    def setUp(self) -> None:
        pass

    def test_render_one(self):
        from .views import FAKE_ODREDNICE
        from .renderer import render_one
        odrednice = [FAKE_ODREDNICE[key] for key in sorted(FAKE_ODREDNICE.keys())]
        result = render_one(odrednice[0])
        self.assertGreaterEqual(len(result), 1)
