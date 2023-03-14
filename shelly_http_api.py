import sys

from bottle import route, request, run, response
from dataclasses import asdict
import json
import logging
import time

from sensor.id_mapping import IDMapping
from sensor.shelly import Sensor, Shelly


content_type = 'application/json; charset=UTF-8'
logger = logging.getLogger('shelly_http_api')
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s')
log_handler.setFormatter(log_format)
logger.addHandler(log_handler)
shelly = Shelly('sensors.json')
id_mapping = IDMapping('id_mappings.json')


def enable_cors(func):
    def wrapper(*args, **kwargs):
        response.set_header("Access-Control-Allow-Origin", "*")
        response.set_header("Content-Type", "application/json")
        response.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        response.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Origin, Content-Type")

        # skip the function if it is not needed
        if request.method == 'OPTIONS':
            return

        return func(*args, **kwargs)
    return wrapper


@route('/sensor/upsert')
def sensor_update():

    sensor_id = request.query.id

    logger.info('adding or updating sensor data of: %s', sensor_id)

    response.content_type = content_type

    name = id_mapping.resolve_name(sensor_id)

    input_lux = request.query.lux
    lux = int(input_lux) if len(input_lux) > 0 else None

    input_temp = request.query.temp
    temperature = float(input_temp) if len(input_temp) > 0 else None

    input_flood = request.query.flood
    has_flood_property = len(input_flood) > 0
    has_flood = has_flood_property and input_flood == '1'
    flood = has_flood if has_flood_property else None

    input_state = request.query.state
    state = input_state if len(input_state) > 0 else None

    sensor = Sensor(name, time.time(), lux, state, temperature, flood)
    shelly.update_sensors_data(sensor)
    shelly.write_sensor_data()

    return asdict(sensor)


@route('/sensor')
@enable_cors
def list_sensors():

    response.content_type = content_type
    shelly_sensors = shelly.list_sensors()

    return json.dumps(shelly_sensors)


if __name__ == '__main__':
    if len(sys.argv) > 3:
        print('Too many arguments!')
        sys.exit(0)

    # First argument is this python file itself
    # Second argument is optional configuration file, otherwise the default is used
    if len(sys.argv) == 2:
        configurationFile = sys.argv[1]
        shelly = Shelly(configurationFile)

    # Third argument is optional id mapping configuration file, otherwise the default is used
    if len(sys.argv) == 3:
        shellyConfigurationFile = sys.argv[1]
        shelly = Shelly(shellyConfigurationFile)
        mappingFile = sys.argv[2]
        id_mapping = IDMapping(mappingFile)

    try:
        run(host='0.0.0.0', port=5010, debug=True)
    finally:
        logger.info('Exiting...')
