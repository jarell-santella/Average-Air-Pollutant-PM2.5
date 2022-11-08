import unittest
import os
from argparse import ArgumentTypeError
from evaluators import integers

class TestIntegers(unittest.TestCase):

    def setUp(self):
        self.ceiling = min(32, os.cpu_count() + 4)

    def test_positive_int(self):
        self.assertEqual(integers.positive_int(4.1), 4)
        self.assertEqual(integers.positive_int(4.5), 4)
        self.assertEqual(integers.positive_int(4.9), 4)
        self.assertEqual(integers.positive_int(1), 1)
        self.assertEqual(integers.positive_int('3'), 3)
        self.assertRaises(ValueError, integers.positive_int, -3)
        self.assertRaises(ValueError, integers.positive_int, -0.1)
        self.assertRaises(ValueError, integers.positive_int, 0)
        self.assertRaises(ValueError, integers.positive_int, 0.1)
        self.assertRaises(ValueError, integers.positive_int, '8.5')
        self.assertRaises(ValueError, integers.positive_int, '-7')
        self.assertRaises(ValueError, integers.positive_int, '-2.5')

    def test_reasonable_positive_int(self):
        self.assertEqual(integers.reasonable_positive_int(self.ceiling), self.ceiling)
        self.assertEqual(integers.reasonable_positive_int(str(self.ceiling)), self.ceiling)
        self.assertRaises(ArgumentTypeError, integers.reasonable_positive_int, self.ceiling + 1)
        self.assertRaises(ValueError, integers.reasonable_positive_int, -3)
        self.assertRaises(ValueError, integers.reasonable_positive_int, -0.1)
        self.assertRaises(ValueError, integers.reasonable_positive_int, 0)
        self.assertRaises(ValueError, integers.reasonable_positive_int, 0.1)
        self.assertRaises(ValueError, integers.reasonable_positive_int, '8.5')
        self.assertRaises(ValueError, integers.reasonable_positive_int, '-7')
        self.assertRaises(ValueError, integers.reasonable_positive_int, '-2.5')

if __name__ == 'main':
    unittest.main()