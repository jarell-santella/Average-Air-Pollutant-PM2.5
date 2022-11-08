import requests
import pandas as pd
from configparser import ConfigParser
from argparse import ArgumentParser
import concurrent.futures
from threading import Event
from exceptions.api import exceptions
import time

config = ConfigParser()
with open('config.cfg') as f:
    config.read_file(f)

API_KEY = config.get('api_keys', 'air_quality')

def positive_int(value):
    # If value is not a positive integer, raise ValueError
    value = int(value)
    if value < 1:
        raise ValueError
    return value

def normalize_response(response):
    # Flatten the JSON response's relevant data and store it in pandas DataFrame. Transform and manipulate the sample data, print, and return
    data = pd.json_normalize(response, 'data')
    if not data.empty:
        data = data[['aqi', 'station.name']]
        data['aqi'] = pd.to_numeric(data['aqi'], errors='coerce')
        data = data.dropna()
        data = data.sort_values(by=['aqi', 'station.name'], ascending=False)
        data = data.reset_index(drop=True)

        for index, row in data.iterrows():
            print('AQI: {aqi}, Station {idx}: {station}'.format(idx=index+1, aqi=row['aqi'], station=row['station.name']))
        print('')

        return data
    else:
        print('No data for given latitude and longitude arguments at this current time.\n')
        return pd.DataFrame(columns=['aqi', 'station.name'])

def request_data(lat1, lng1, lat2, lng2, period, rate, sample, event):
    for _ in range(60):
        if event.is_set():
            return None
        time.sleep((sample%rate)/rate)

    # Make API call with given arguments, get API response and transform it to JSON
    url = f'https://api.waqi.info/v2/map/bounds?latlng={lat1},{lng1},{lat2},{lng2}&networks=all&token={API_KEY}'
    response = requests.get(url)
    response = response.json()

    print('Minute: {minute}, Sample: {num} - ({sample_num}/{total})'.format(minute=sample//rate, num=sample%rate+1, sample_num=sample+1, total=period*rate))

    if response['status'] == 'error':
        if response['data'] == 'Over quota':
            print("request_data api request quota error")
            raise exceptions.APIRequestQuotaError('API request failed. The request quota is over limits.')
        elif response['data'] == 'Invalid key':
            print("request_data api invalid key error")
            raise exceptions.APIInvalidKeyError('API request failed. The key is not valid.')

    if(event.is_set()):
        return None

    return response

def start_threads(lat1, lng1, lat2, lng2, period, rate):
    results_by_minute = []
    event = Event()

    # Use threading to make an API call n times per minute for m minutes (where n = rate, m = period)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for minute in range(period):

            if event.is_set():
                break

            start = time.time()
            results = [executor.submit(request_data, lat1, lng1, lat2, lng2, period, rate, minute*rate + sample, event) for sample in range(rate)]
            
            try:
                for index, result in enumerate(concurrent.futures.as_completed(results)):

                    if event.is_set():
                        break
                
                    response = result.result()
                    results[index] = normalize_response(response)

            except KeyboardInterrupt:
                event.set()
                raise
            except exceptions.APIRequestQuotaError:
                event.set()
                raise
            except exceptions.APIInvalidKeyError:
                event.set()
                raise
            
            results_by_minute.append(results)

            end = time.time()
            while end-start < 60:

                if event.is_set():
                    break

                time.sleep(0.01)
                end = time.time()
            
    return results_by_minute

def main(lat1, lng1, lat2, lng2, period, rate):
    samples = period*rate
    print(f'Calculating average of {period*rate} PM2.5 readings over {period} minute(s) in stations between latitudes {lat1} and {lat2} and longitudes {lng1} and {lng2}.\n')

    # Start fetching API data at given rate for given period, and store the processed results
    data = start_threads(lat1, lng1, lat2, lng2, period, rate)
    appended_data = pd.DataFrame(columns=['aqi', 'station.name'])

    # Put processed results together to collect averages
    for minute in data:
        for sample in minute:
            appended_data = pd.concat([appended_data, sample], ignore_index=True)
    
    # Get average AQI of all samples per each station, as well as how many samples there were per station, and sort on mean AQI in descending order
    if not appended_data.empty:
        appended_data = appended_data.groupby('station.name', as_index=False)['aqi'].agg(['mean', 'count'])
        appended_data = appended_data.sort_values(by=['mean', 'station,name'], ascending=False)
        appended_data = appended_data.reset_index().rename(columns={'station.name': 'Station', 'mean': 'Mean AQI', 'count': 'Number of Samples'})
        
        print(f'Average of {samples} PM2.5 readings over {period} minute(s) in stations between latitudes {lat1} and {lat2} and longitudes {lng1} and {lng2}:')
        for index, row in appended_data.iterrows():
            print('Average AQI: {aqi} ({sample_num} samples), Station {idx}: {station}'.format(idx=index+1, aqi=row['Mean AQI'], station=row['Station'], sample_num=row['Number of Samples']))
    else:
        print(f'All {samples} samples had no data for given latitude and longitude arguments at this current time. Calculating average could not be performed.')

if __name__ == '__main__':

    # Handle command line input arguments from user
    parser = ArgumentParser(description='Calculates the average PM2.5 readings from stations within an area over a period')
    parser.add_argument('lat1', type=float, help='Latitude bound 1')
    parser.add_argument('lng1', type=float, help='Longitude bound 1')
    parser.add_argument('lat2', type=float, help='Latitude bound 2')
    parser.add_argument('lng2', type=float, help='Longitude bound 2')
    parser.add_argument('period', nargs='?', default=5, type=positive_int, help='Sampling period in minutes')
    parser.add_argument('rate', nargs='?', default=1, type=positive_int, help='Sampling rate in samples per minute')
    args = parser.parse_args()

    main(args.lat1, args.lng1, args.lat2, args.lng2, args.period, args.rate)