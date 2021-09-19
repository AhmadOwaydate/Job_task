
import unittest
import requests

from middleware.check_if_in_mkad import check_if_in_mkad
from middleware.get_cordinates import get_cordinates
from middleware.get_distance import get_distance_to_mscow_ring


class TestApp(unittest.TestCase):
    try:
        def test_get_distance(self):
            # coordinates of Tverskaya 6
            distance = get_distance_to_mscow_ring(30.379828, 59.947189)
            self.assertEqual(distance, 894.064330960043)
            # coordinates of moscow ring road
            distance = get_distance_to_mscow_ring(37.620312, 55.729747)
            self.assertEqual(distance, 0)

        def test_check_in_mkad(self):
            check = check_if_in_mkad(1.0, 1.0)
            self.assertEqual(check, False)
            # coordinates already checked in mkad
            check = check_if_in_mkad(37.842762, 55.774558)
            self.assertEqual(check, True)

        def test_get_coordinates(self):
            # unit test with Tverskaya 6 as address input

            response = requests.get(
                url="https://geocode-maps.yandex.ru/1.x/?"
                + "apikey=c97769fc-875c-4678-8139-08b6e7400a8e"
                + "&format=json"
                + "&geocode=Tverskaya 6")
            response = response.json()

            coordinates = get_cordinates(response)
            self.assertEqual(coordinates, [30.379828, 59.947189])
            # unit test with moscow ring as address input
            response = requests.get(
                url="https://geocode-maps.yandex.ru/1.x/?"
                + "apikey=c97769fc-875c-4678-8139-08b6e7400a8e"
                + "&format=json"
                + "&geocode=Moscow Ring Road")
            response = response.json()
            coordinates = get_cordinates(response)
            self.assertEqual(coordinates, [37.620312, 55.729747])

            # test with a wrong input
            response = requests.get(
                url="https://geocode-maps.yandex.ru/1.x/?"
                + "apikey=c97769fc-875c-4678-8139-08b6e7400a8e"
                + "&format=json"
                + "&geocode=this is a wrong address okay?")
            response = response.json()
            coordinates = get_cordinates(response)
            self.assertEqual(coordinates, [])
    except:
        # if there is an error caused by the response the app is considered failed
        self.assertEqual(1, 2)


if __name__ == '__main__':
    unittest.main()
