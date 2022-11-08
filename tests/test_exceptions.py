import unittest
from exceptions.api import exceptions

class TestExceptions(unittest.TestCase):

    def test_APIRequestQuotaError(self):
        self.assertEqual(str(exceptions.APIRequestQuotaError('test')), 'test')

        with self.assertRaises(exceptions.APIRequestQuotaError):
            raise exceptions.APIRequestQuotaError('test')

        with self.assertRaises(exceptions.APIRequestQuotaError):
            raise exceptions.APIRequestQuotaError('')

        with self.assertRaises(exceptions.APIRequestQuotaError):
            raise exceptions.APIRequestQuotaError()

        with self.assertRaises(exceptions.APIRequestQuotaError):
            raise exceptions.APIRequestQuotaError

    def test_APIInvalidKeyError(self):
        self.assertEqual(str(exceptions.APIInvalidKeyError('test')), 'test')

        with self.assertRaises(exceptions.APIInvalidKeyError):
            raise exceptions.APIInvalidKeyError('test')

        with self.assertRaises(exceptions.APIInvalidKeyError):
            raise exceptions.APIInvalidKeyError('')

        with self.assertRaises(exceptions.APIInvalidKeyError):
            raise exceptions.APIInvalidKeyError()

        with self.assertRaises(exceptions.APIInvalidKeyError):
            raise exceptions.APIInvalidKeyError

if __name__ == 'main':
    unittest.main()