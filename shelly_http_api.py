import sys

from bottle import route, request, run, response
from dataclasses import asdict
import json
import logging

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
    state = request.query.state
    sensor = Sensor(name, lux, state, temperature)
    shelly.update_sensors_data(sensor)
    shelly.write_sensor_data()

    return asdict(sensor)


@route('/sensor')
def list_sensors():

    response.content_type = content_type
    shelly_sensors = shelly.list_sensors()
    return json.dumps(shelly_sensors)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print('Too many arguments!')
        sys.exit(0)

    # First argument is this python file itself
    # Second argument is optional configuration file, otherwise the default is used
    if len(sys.argv) == 2:
        configurationFile = sys.argv[1]
        shelly = Shelly(configurationFile)

    try:
        run(host='0.0.0.0', port=5010, debug=True)
    finally:
        print('Exiting...')
