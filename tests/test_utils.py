import unittest
from math import radians
from common.utils import calc_dist

class TestUtils(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_calc_dist(self):
        distance = calc_dist(21.0122287, 52.2296756, 16.9251681, 52.406374)
        self.assertAlmostEqual(distance, 278.5455, places=3)