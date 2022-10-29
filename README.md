# Average Air Pollutant PM2.5

This is a Python script that you run in the command line that calculates the average AQI for stations that are bounded by latitude and longitude values that the user specifies. To calculate the average, real-time data is fetched from the [World Air Quality Index](https://waqi.info/) using API calls. The user specifies how many API calls the time period (in minutes) to fetch the data, as well as how many times per minute the data is fetched.

## How to use

This is a command line script that takes in at least four but up to six arguments (in this order):
1. `lat1`
    - First latitude bound
    - Numeric
    - Mandatory
2. `lng1`
    - First longitude bound
    - Numeric
    - Mandatory
3. `lat2`
    - Second latitude bound
    - Numeric
    - Mandatory
4. `lng2`
    - Second longitude bound
    - Numeric
    - Mandatory
5. `period`
    - The sampling period in minutes
    - Integer
    - Optional (default = 5)
6. `rate`
    - The rate of sampling in sample(s)/minute
    - Integer
    - Optional (default = 1)

Download the `scripy.py` file. In command line, change your current working directory to the folder that `script.py` is in by executing `cd path/to/folder`. You can now run the script using command line by executing `python script.py lat1 lng1 lat2 lng2 period rate`. You cannot specify `rate` without `period`. If either `period` or `rate` are not specified or are given invalid inputs, the respective default will be used. This script's first four arguments must be numeric for the latitude and longitude bounds, otherwise the script will not run. Additionally, please make sure to have an API key for API access. You can get your API key [here](https://aqicn.org/data-platform/token/). In order for the script to use your API key, you will need to create a file named `config.cfg` in the same working directory that `script.py` is in. Copy and paste the following into `config.cfg`:
```
[api_keys]
air_quality: your_api_key_here
```

## Miscellaneous

This script is I/O bound as we are fetching data from API responses. As a result, in order to ensure that the sampling period and sampling rate remains consistent even while sampling rate is high, this script uses threading. If the API responds with an error, all threads stop and the script terminates immediately a raised exception detailing what happened.