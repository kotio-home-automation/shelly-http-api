import json
import unittest
from boddle import boddle

from sensor.shelly import Sensor
from shelly_http_api import sensor_update, list_sensors


class MyTestCase(unittest.TestCase):
    def test_kitchen_sensor_update(self):
        lux = 1
        state = 'closed'
        temperature = 19.9
        name = 'kitchen'

        with boddle(query={'lux': lux, 'state': state, 'temp': str(temperature)}):
            sensor = Sensor(**sensor_update(name))
            self.assertIsNotNone(sensor)
            self.assertEqual(sensor.name, name)
            self.assertEqual(sensor.lux, lux)
            self.assertEqual(sensor.state, state)
            self.assertEqual(sensor.temperature, temperature)

    def test_list_sensors(self):
        sensors = json.loads(list_sensors())
        self.assertIsInstance(sensors, list)
        self.assertEqual(len(sensors), 2)


if __name__ == '__main__':
    unittest.main()