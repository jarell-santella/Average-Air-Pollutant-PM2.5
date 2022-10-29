import sys
import requests
import pandas as pd
from configparser import ConfigParser
import math
import concurrent.futures
import time

config = ConfigParser()
with open('config.cfg') as f:
    config.read_file(f)

API_KEY = config.get('api_keys', 'air_quality')

def request_data(lat1, lng1, lat2, lng2, period, rate, sample):
    # Sleep for variable amount of time such that each sample is taken n times per minute for m minutes (where n = rate, m = period)
    time.sleep((60/rate)*sample)
    # Make API call with given arguments, get API response and transform it to JSON
    url = f'https://api.waqi.info/v2/map/bounds?latlng={lat1},{lng1},{lat2},{lng2}&networks=all&token={API_KEY}'
    response = requests.get(url)
    response = response.json()

    print('Minute: {minute}, Sample: {num} - ({sample_num}/{total})'.format(minute=math.floor(sample/rate), num=sample%rate+1, sample_num=sample+1, total=period*rate))

    if response['status'] == 'error':
        if response['data'] == 'Over quota':
            failure_message = 'API request failed. The request quota is over limits.'
        elif response['data'] == 'Invalid key':
            failure_message = 'API request failed. The key is not valid.'
        raise Exception(failure_message)

    # Flatten the JSON response's relevant data and store it in pandas DataFrame. Transform and manipulate the sample data, print, and return
    data = pd.json_normalize(response, 'data')
    if not data.empty:
        data = data[['aqi', 'station.name']]
        data['aqi'] = pd.to_numeric(data['aqi'], errors='coerce')
        data = data.dropna()
        data = data.sort_values(by=['aqi'], ascending=False)
        data = data.reset_index(drop=True)

        for index, row in data.iterrows():
            print('AQI: {aqi}, Station {idx}: {station}'.format(idx=index+1, aqi=row['aqi'], station=row['station.name']))
        print('')

        return data
    else:
        print('No data for given latitude and longitude arguments at this current time.\n')
        return pd.DataFrame(columns=['aqi', 'station.name'])

def main(lat1, lng1, lat2, lng2, period, rate):
    samples = period*rate

    # Use threading to make an API call n times per minute for m minutes (where n = rate, m = period)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print(f'Calculating average of {samples} PM2.5 readings over {period} minute(s) in stations between latitudes {lat1} and {lat2} and longitudes {lng1} and {lng2}.\n')

        results = [executor.submit(request_data, lat1, lng1, lat2, lng2, period, rate, sample) for sample in range(samples)]

        # Once sample data is available, store each sample's data into one DataFrame
        appended_data = pd.DataFrame(columns=['aqi', 'station.name'])
        try:
            for result in concurrent.futures.as_completed(results):
                data = result.result()
                appended_data = pd.concat([appended_data, data], ignore_index=True)
        except KeyboardInterrupt:
            # Kill all threads if KeyboardInterrupt is detected
            executor._threads.clear()
            concurrent.futures.thread._threads_queues.clear()
            raise
        except Exception:
            # Kill all threads if API response has error
            executor._threads.clear()
            concurrent.futures.thread._threads_queues.clear()
            raise
    
    # Get average AQI of all samples per each station, as well as how many samples there were per station, and sort on mean AQI in descending order
    if not appended_data.empty:
        appended_data = appended_data.groupby('station.name', as_index=False)['aqi'].agg(['mean', 'count'])
        appended_data = appended_data.sort_values(by=['mean'], ascending=False)
        appended_data = appended_data.reset_index().rename(columns={'station.name': 'Station', 'mean': 'Mean AQI', 'count': 'Number of Samples'})
        
        print(f'Average of {samples} PM2.5 readings over {period} minute(s) in stations between latitudes {lat1} and {lat2} and longitudes {lng1} and {lng2}:')
        for index, row in appended_data.iterrows():
            print('Average AQI: {aqi} ({sample_num} samples), Station {idx}: {station}'.format(idx=index+1, aqi=row['Mean AQI'], station=row['Station'], sample_num=row['Number of Samples']))
    else:
        print(f'All {samples} samples had no data for given latitude and longitude arguments at this current time. Calculating average could not be performed.')

if __name__ == '__main__':

    latlng = []

    # Validate that there are at least 4 arguments for the 2 latitude and 2 longitude arguments
    if len(sys.argv) < 5:
        raise Exception('Expected 2 latitude and 2 longitude arguments.')

    # Validate that the latitude and longitude arguments are numeric
    # Store latitude and longitude arguments into list
    for i in range(1, 5):
        try:
            float(sys.argv[i])
        except ValueError:
            raise Exception('Expected latitude and longitude arguments to be numeric.') from None
        else:
            latlng.append(sys.argv[i])

    # Validate that the sampling period argument exists and is an integer
    # Store argument into variable if valid, otherwise give variable default value (5)
    try:
        period = int(sys.argv[5])
    except:
        period = 5
        print(f'Expected integer for sampling period in seconds. Using default of {period}.\n')

    # Validate that the sampling rate argument exists is an integer
    # Store argument into variable if valid, otherwise give variable default value (1)
    try:
        rate = int(sys.argv[6])
    except:
        rate = 1
        print(f'Expected integer for sampling rate in samples per second. Using default of {rate}.\n')

    main(latlng[0], latlng[1], latlng[2], latlng[3], period, rate)