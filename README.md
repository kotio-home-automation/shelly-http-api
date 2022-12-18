# Shelly HTTP API

API that receives updates via HTTP from Shelly IoT devices and provides endpoint for listing all provided sensor data.

The application persists sensor data to a json file. By default, the data is persisted to [sensors.json](sensors.json)
and that same file is used by some tests. The default configuration file can be overriden by giving path to configuration
file as a command line parameter when running the application.

## Requirements

* Python 3.9

## Howto develop

### Setup virtual environment

https://python.land/virtual-environments/virtualenv

#### Example

Create virtual environment: `python -m venv venv`

Activate virtual environment: `source venv/bin/activate`

Deativate virtual environment: `deactivate`

### Install dependencies

`pip install -r requirements.txt`

### Run tests

`python -m unittest discover`

### Run application with default configuration

Uses [sensors.json](sensors.json) as configuration file.

`python shelly_http_api.py`

### Run application with custom configuration

Uses the given parameter as a configuration file.

`python shelly_http_api.py configuration.json`

### Code organization

* [requirements.txt](requirements.txt) contains dependencies
* [shelly_http_api.py](shelly_http_api.py) is the main file and contains HTTP endpoints
* [sensor](sensor) is a module for shelly sensors
* [test](test) contains all tests

## API

### Receive data

URL: `/sensor/<sensor name>?<query parameters>`

Query parameters
* state: sensor state e.g. open/closed
* temp: temperature reading
* lux: lux reading

Response:
```json
{
  "name": "kitchen",
  "lux": 10,
  "state": "open",
  "temperature": 19.7
}
```

### List sensors

URL: `/sensor`

Response:
```json
[
  {
    "name": "kitchen",
    "lux": 10,
    "state": "open",
    "temperature": 19.7
 }
]
```