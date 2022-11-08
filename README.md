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

To run this script, download all of the files into one folder. In command line, change your current working directory to the folder that `script.py` is in by executing `cd path/to/folder`. Next, this script uses several libraries that are not included in Python's standard library. Please ensure you have the following libraries:
- [requests](https://pypi.org/project/requests/)
- [pandas](https://pypi.org/project/pandas/)

If either of these libraries are missing, you can use `pip install requests` and/or `pip install pandas` in command line to install these libraries. If you do not have `pip`, then you can use `python -m ensurepip --upgrade`. (more information about installing `pip` [here](https://pip.pypa.io/en/stable/installation/))

You can now run the script using command line by executing `python script.py lat1 lng1 lat2 lng2 period rate`.

You can also execute `python script.py -h` for information on the input arguments from the command line, albeit more detailed information is available [above](#how-to-use).

### Input constraints

You cannot specify `rate` without `period`. If either `period` or `rate` are not specified or are given invalid inputs, the respective default will be used. This script's first four arguments must be numeric otherwise the script will not run, and needs at least four arguments to run. This is to ensure that the latitude and longitude bounds are given as there are no defaults for these values unlike for sampling period and the rate of sampling.

If there is no recorded AQI data for stations within the latitude or longitude bounds at the time an API call is made, then only the stations with recorded AQI data are kept in that sample's data. Moreover, if there is no data recorded, the script handles that as well.

There is a maximum limit of `rate` depending on the CPU core count of your computer. This is because it isn't really practical to collect the averages of samples taken so many times per minute. Furthermore, it will just cause the script to have poorer performance.

### API key for API access and config.cfg file

Please make sure to have an API key for API access. You can get your API key [here](https://aqicn.org/data-platform/token/). In order for the script to use your API key, you will need to create a file named `config.cfg` in the same working directory that `script.py` is in. Copy and paste the following into `config.cfg`:
```
[api_keys]
air_quality: your_api_key_here
```

### Running tests

If you would like to run the tests I have included, the process is similar to how to run the Python script. Follow the first steps of changing your current working directory and making sure that the libraries that don't come in Python's standard library are installed. Next, depending on what you would like to test, you can execute any of the following in command line to test `script.py`, `evaluators/integers.py`, and `exceptions/api/exceptions.py` respectively:
- `python -m unittest tests.test_script -b`
- `python -m unittest tests.test_integers -b`
- `python -m unittest tests.test_exceptions -b`

## Some changes
- Uses `ArgumentParser` from `argparse` for command line input retrieval and validation
- Uses custom functions in `evaluators/integers.py` to evaluate appropriate input integer values for `period` and `rate`
- `rate` is now limited based on the user's CPU core count to ensure performance without compromising on practicality
- No longer violates encapsulation to kill all threads by using `Event` from `threading`
- Starts threads by the minute rather than all threads at once to save computing resources and maximize performance
- Break functions down into smaller components
- Created new exception classes in `exceptions/api/exceptions.py` for API errors, and handle the exceptions individually rather than catching them all together
- Use `unittest` to perform tests on the main script, the custom functions, and the custom exception classes

## Closing Thoughts (and Miscellaneous)

This script is I/O bound as we are fetching data from API responses. As a result, in order to ensure performance and that the sampling period and sampling rate remains consistent even while sampling rate is high, this script uses threading. If the API responds with an error, all threads stop and the script terminates immediately with a raised exception detailing what happened. There is lots of exception handling throughout the app, and especially with what kind of arguments the user can input in command line when executing the script.

Previously, I terminated all threads while violating encapsulation. Now, my method of terminating all threads isn't as immediate, but it no longer violates encapsulation. I would still like to try to see if I can improve how immediate the termination is, but it's not very necessary or practical to have it terminate at a faster speed than it already does right now. The method I used makes the threads check whether or not they should terminate as they are waiting to be started. But depending on which sample number in a minute the thread is handling, the time intervals that the threads make these checks is not consistent. I would like to fix that and have a consistent time interval for all threads to check on whether they should be terminated or not, regardless of which sample number in a minute that the thread is handling.

I would also like to see if it's possible for me to increase the rate limit. This seems challening as, assuming I stick with threading, it's heavily limited by the hardware of the user who is running the script. Furthermore, it serves no practical purpose to increase the rate limit, unless the AQI in a given area is changing many times every minute, which does not seem very realistic. Many users would be able to have a rate of 12, meaning a call to the APi every 5 seconds, and that should be enough.

The last thing, and arguably one of the most important, is that I want to create more tests and figure out how to make the tests more robust.