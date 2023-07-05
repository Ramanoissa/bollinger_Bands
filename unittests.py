import unittest
from get_data import get_prices
from bollinger import df
from get_data import data

 
class MyTest(unittest.TestCase):
    def test_get_prices(self):
        # Unit test for the get_prices function
        get_prices()
        self.assertGreater(len(data), 0)
        
    def test_bollinger_calculation(self):
        # Unit test for the Bollinger Bands calculation
        self.assertEqual(len(df), 100)
        self.assertTrue('bb_upperband' in df.columns)
        self.assertTrue('bb_middleband' in df.columns)
        self.assertTrue('bb_lowerband' in df.columns)
        self.assertTrue('bb_lowerband_value' in df.columns)
        self.assertTrue('bb_upperband_value' in df.columns)

if __name__ == '__main__':
    unittest.main()

