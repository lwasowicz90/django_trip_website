import unittest

class TestSecond(unittest.TestCase):
    def test_list_int(self):
        self.assertEqual(6, 6)

    def test_list_fraction(self):
        self.assertEqual(6, 6)

if __name__ == '__main__':
    unittest.main()