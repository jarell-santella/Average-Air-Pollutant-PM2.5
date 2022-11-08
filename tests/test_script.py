import unittest
from unittest.mock import patch
from configparser import ConfigParser
from threading import Event
import json
from src import script

class TestScript(unittest.TestCase):

    def setUp(self):
        self.config = ConfigParser()
        with open('config.cfg') as f:
            self.config.read_file(f)

        self.API_KEY = self.config.get('api_keys', 'air_quality')

        self.lat1 = 49.135713
        self.lng1 = -122.892371
        self.lat2 = 50.271092
        self.lng2 = -123.612322

        self.url = f'https://api.waqi.info/v2/map/bounds?latlng={self.lat1},{self.lng1},{self.lat2},{self.lng2}&networks=all&token={self.API_KEY}'

        self.mock_response1 = {
            "status": "ok",
            "data": [
                {
                    "lat": 49.3017,
                    "lon": -123.0203,
                    "uid": 4227,
                    "aqi": "20",
                    "station": {
                        "name": "North Vancouver Second Narrows, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.227045,
                    "lon": -122.894487,
                    "uid": 14102,
                    "aqi": "26",
                    "station": {
                        "name": "New Westminster Sapperton Park, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.3686,
                    "lon": -123.2766,
                    "uid": 4224,
                    "aqi": "23",
                    "station": {
                        "name": "Horseshoe Bay, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.70516,
                    "lon": -123.15133,
                    "uid": 8838,
                    "aqi": "21",
                    "station": {
                        "name": "Squamish Elementary, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 50.144285,
                    "lon": -122.960402,
                    "uid": 4245,
                    "aqi": "13",
                    "station": {
                        "name": "Whistler Meadow Park, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.1864,
                    "lon": -123.1522,
                    "uid": 10133,
                    "aqi": "35",
                    "station": {
                        "name": "Vancouver International Airport #2, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.2794,
                    "lon": -122.9711,
                    "uid": 4219,
                    "aqi": "21",
                    "station": {
                        "name": "Burnaby Kensington Park, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.1414,
                    "lon": -123.1083,
                    "uid": 4230,
                    "aqi": "22",
                    "station": {
                        "name": "Richmond South, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.3239,
                    "lon": -123.0836,
                    "uid": 14100,
                    "aqi": "14",
                    "station": {
                        "name": "North Vancouver Mahon Park, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.438848,
                    "lon": -123.479185,
                    "uid": 4243,
                    "aqi": "19",
                    "station": {
                        "name": "Langdale Elementary, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.2153,
                    "lon": -122.9856,
                    "uid": 4221,
                    "aqi": "23",
                    "station": {
                        "name": "Burnaby South, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.2875,
                    "lon": -123.0078,
                    "uid": 4220,
                    "aqi": "10",
                    "station": {
                        "name": "Burnaby North Eton, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.725586,
                    "lon": -123.142586,
                    "uid": -344797,
                    "aqi": "-",
                    "station": {
                        "name": "AQSU-VCH-Brennan Park Recreation Centre pool outside",
                        "time": "2022-11-08T12:12:59+09:00"
                    }
                },
                {
                    "lat": 49.1583,
                    "lon": -122.9017,
                    "uid": 4226,
                    "aqi": "27",
                    "station": {
                        "name": "North Delta, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.26029,
                    "lon": -123.077811,
                    "uid": 14111,
                    "aqi": "22",
                    "station": {
                        "name": "Vancouver Clark Drive, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                }
            ]
        }
        self.mock_response2 = {
            "status": "ok",
            "data": [
                {
                    "lat": 49.227045,
                    "lon": -122.894487,
                    "uid": 14102,
                    "aqi": "26",
                    "station": {
                        "name": "New Westminster Sapperton Park, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.3686,
                    "lon": -123.2766,
                    "uid": 4224,
                    "aqi": "23",
                    "station": {
                        "name": "Horseshoe Bay, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 50.144285,
                    "lon": -122.960402,
                    "uid": 4245,
                    "aqi": "13",
                    "station": {
                        "name": "Whistler Meadow Park, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.1864,
                    "lon": -123.1522,
                    "uid": 10133,
                    "aqi": "35",
                    "station": {
                        "name": "Vancouver International Airport #2, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.2794,
                    "lon": -122.9711,
                    "uid": 4219,
                    "aqi": "21",
                    "station": {
                        "name": "Burnaby Kensington Park, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.1414,
                    "lon": -123.1083,
                    "uid": 4230,
                    "aqi": "22",
                    "station": {
                        "name": "Richmond South, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.3239,
                    "lon": -123.0836,
                    "uid": 14100,
                    "aqi": "14",
                    "station": {
                        "name": "North Vancouver Mahon Park, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.438848,
                    "lon": -123.479185,
                    "uid": 4243,
                    "aqi": "19",
                    "station": {
                        "name": "Langdale Elementary, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.2875,
                    "lon": -123.0078,
                    "uid": 4220,
                    "aqi": "10",
                    "station": {
                        "name": "Burnaby North Eton, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                },
                {
                    "lat": 49.1583,
                    "lon": -122.9017,
                    "uid": 4226,
                    "aqi": "27",
                    "station": {
                        "name": "North Delta, British Comlumbia, Canada",
                        "time": "2022-11-08T11:00:00+09:00"
                    }
                }
            ]
        }
        self.mock_response3 = {
            "status": "ok",
            "data": [
                {
                    "lat": 49.725586,
                    "lon": -123.142586,
                    "uid": -344797,
                    "aqi": "-",
                    "station": {
                        "name": "AQSU-VCH-Brennan Park Recreation Centre pool outside",
                        "time": "2022-11-08T12:12:59+09:00"
                    }
                }
            ]
        }
        self.mock_empty_response = {
            "status": "ok",
            "data": []
        }

    def test_normalize_response(self):
        response = script.normalize_response(self.mock_response1)

        self.assertEqual(response.shape[0], 14)
        self.assertEqual(list(response.columns.values), ['aqi', 'station.name'])

        response = script.normalize_response(self.mock_response2)

        self.assertEqual(response.shape[0], 10)
        self.assertEqual(list(response.columns.values), ['aqi', 'station.name'])

        response = script.normalize_response(self.mock_response3)

        self.assertEqual(response.shape[0], 0)
        self.assertEqual(list(response.columns.values), ['aqi', 'station.name'])
        
        response = script.normalize_response(self.mock_empty_response)

        self.assertEqual(response.shape[0], 0)
        self.assertEqual(list(response.columns.values), ['aqi', 'station.name'])

    def test_api_call(self):
        with patch('src.script.requests.get') as mock_api_call:
            url = f'https://api.waqi.info/v2/map/bounds?latlng={self.lat1},{self.lng1},{self.lat2},{self.lng2}&networks=all&token=testinvalid'
            text = '{"status":"error","data":"Invalid key"}'
            mock_api_call.return_value.ok = True
            mock_api_call.return_value.text = text

            api_call = script.api_call(url)
            mock_api_call.assert_called_with(url)
            self.assertEqual(api_call.text, text)
            self.assertCountEqual(json.loads(api_call.text), json.loads(text))

            url = f'https://api.waqi.info/v2/map/bounds?latlng={self.lat1},{self.lng1},{self.lat2},{self.lng2}&networks=all&token={self.API_KEY}'
            text = '{"status":"ok","data":[{"lat":49.725586,"lon":-123.142586,"uid":-344797,"aqi":"-","station":{"name":"AQSU-VCH-Brennan Park Recreation Centre pool outside","time":"2022-11-08T12:12:59+09:00"}},{"lat":49.1583,"lon":-122.9017,"uid":4226,"aqi":"27","station":{"name":"North Delta, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":49.2875,"lon":-123.0078,"uid":4220,"aqi":"10","station":{"name":"Burnaby North Eton, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":49.3017,"lon":-123.0203,"uid":4227,"aqi":"20","station":{"name":"North Vancouver Second Narrows, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":49.438848,"lon":-123.479185,"uid":4243,"aqi":"19","station":{"name":"Langdale Elementary, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":49.1414,"lon":-123.1083,"uid":4230,"aqi":"22","station":{"name":"Richmond South, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":49.1864,"lon":-123.1522,"uid":10133,"aqi":"35","station":{"name":"Vancouver International Airport #2, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":49.26029,"lon":-123.077811,"uid":14111,"aqi":"22","station":{"name":"Vancouver Clark Drive, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":49.227045,"lon":-122.894487,"uid":14102,"aqi":"26","station":{"name":"New Westminster Sapperton Park, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":49.3239,"lon":-123.0836,"uid":14100,"aqi":"14","station":{"name":"North Vancouver Mahon Park, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":49.70516,"lon":-123.15133,"uid":8838,"aqi":"21","station":{"name":"Squamish Elementary, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":50.144285,"lon":-122.960402,"uid":4245,"aqi":"13","station":{"name":"Whistler Meadow Park, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":49.2153,"lon":-122.9856,"uid":4221,"aqi":"23","station":{"name":"Burnaby South, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":49.2794,"lon":-122.9711,"uid":4219,"aqi":"21","station":{"name":"Burnaby Kensington Park, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}},{"lat":49.3686,"lon":-123.2766,"uid":4224,"aqi":"23","station":{"name":"Horseshoe Bay, British Comlumbia, Canada","time":"2022-11-08T11:00:00+09:00"}}]}'
            mock_api_call.return_value.text = text

            api_call = script.api_call(url)
            mock_api_call.assert_called_with(url)
            self.assertCountEqual(json.loads(api_call.text), json.loads(text))
            self.assertCountEqual(json.loads(api_call.text)['data'], json.loads(text)['data'])

            api_lat_set = set()
            api_lng_set = set()
            api_uid_set = set()
            for station in json.loads(api_call.text)['data']:
                api_lat_set.add(station['lat'])
                api_lng_set.add(station['lon'])
                api_uid_set.add(station['uid'])

            mock_lat_set = set()
            mock_lng_set = set()
            mock_uid_set = set()
            for station in json.loads(text)['data']:
                mock_lat_set.add(station['lat'])
                mock_lng_set.add(station['lon'])
                mock_uid_set.add(station['uid'])

            self.assertSetEqual(api_lat_set, mock_lat_set)
            self.assertSetEqual(api_lng_set, mock_lng_set)
            self.assertSetEqual(api_uid_set, mock_uid_set)

    def test_request_data(self):
        event = Event()

        data = script.request_data(self.lat1, self.lng1, self.lat2, self.lng2, 0, 1, 0, event)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(len(data), 2)
        self.assertEqual(len(data['data']), 15)

        event.set()

        data = script.request_data(self.lat1, self.lng1, self.lat2, self.lng2, 0, 1, 0, event)
        self.assertIsNone(data)

if __name__ == '__main__':
    unittest.main()