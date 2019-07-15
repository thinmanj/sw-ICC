from django.test import TestCase

from rest_framework.test import APIClient

class temperaturetestCase(TestCase):
    fixtures = ['init.json']

    def setUp(self):
        self.client = APIClient()

    def test_geo_normal(self):
        data = [
            (0, 0),
            (90, 180),
            (-90, -180),
            (90, -180),
            (-90, 180),
            (20, 50)
        ]
        for entry in data:
            response = self.client.get(f'/{entry[0]}/{entry[1]}/')
            self.assertEqual(response.status_code, 200)


    def test_geo_invalid(self):
        data = [
            (-99, 0),
            (0, -181)
        ]
        for entry in data:
            response = self.client.get(f'/{entry[0]}/{entry[1]}/')
            self.assertEqual(response.status_code, 404)

