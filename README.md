# Shelly HTTP API

API that receives updates via HTTP from Shelly IoT devices and provides endpoint for listing all provided sensor data.

The application persists sensor data to a json file. By default, the data is persisted to [sensors.json](sensors.json)
and that same file is used by some tests. The default configuration file can be overriden by giving path to configuration
file as a command line parameter when running the application.

The application also has capability to map sensor id's to human-readable names. By default, empty mapping array is used
from file [id_mappings.json](id_mappings.json) i.e. no mapping is done, but it can be overriden by giving path to mapping file.

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

Uses [sensors.json](sensors.json) as sensors configuration file and [id_mappings.json](id_mappings.json) as id-name
mapping configuration file.

`python shelly_http_api.py`

### Run application with custom configurations

Uses the first parameter as sensors configuration file and second as id-name mapping configuration.

`python shelly_http_api.py configuration.json id_mappings.json`

### Code organization

* [requirements.txt](requirements.txt) contains dependencies
* [shelly_http_api.py](shelly_http_api.py) is the main file and contains HTTP endpoints
* [sensor](sensor) is a module for shelly sensors
* [test](test) contains all tests

## API

### Receive data

URL: `/sensor/upsert?<query parameters>`

Query parameters
* state: optional sensor state e.g. open/closed
* temp: temperature reading
* lux: optional lux reading
* flood: optional flood indicator as 0/1

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
