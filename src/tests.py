import unittest
from programming import count_pairs

class TestStringMethods(unittest.TestCase):

    def test_count_pairs_1(self):
        result = count_pairs([1, 3, 1, 4], 1, 2)
        self.assertEqual(result, 2)

    def test_count_pairs_2(self):
        result = count_pairs([1, 1, 2, 2], 1, 2)
        self.assertEqual(result, 1)

    def test_count_pairs_3(self):
        result = count_pairs([1, 1, 2, 2, 3], 2, 4)
        self.assertEqual(result, 1)

    def test_count_pairs_4(self):
        result = count_pairs([1, 2, 1, 6, 3], 2, 4)
        self.assertEqual(result, 3)

if __name__ == '__main__':
    unittest.main()