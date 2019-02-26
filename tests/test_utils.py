import unittest
from math import radians
from common.utils import calc_dist, get_weekday_from_datetime

class TestUtils(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_calc_dist(self):
        distance = calc_dist(21.0122287, 52.2296756, 16.9251681, 52.406374)
        self.assertAlmostEqual(distance, 278.5455, places=3)
    
    def test_get_weekday_from_datetime(self):
        weekday = get_weekday_from_datetime('2019-02-15T20:14:00')
        self.assertEqual(weekday, 4)