import json
import unittest
from boddle import boddle

from sensor.shelly import Sensor
from shelly_http_api import sensor_update, list_sensors


class MyTestCase(unittest.TestCase):
    def test_kitchen_door_sensor_update(self):
        lux = 10
        state = 'closed'
        temperature = 19.9
        sensor_id = 'kitchen'

        with boddle(query={'lux': lux, 'state': state, 'temp': str(temperature), 'id': sensor_id}):
            sensor = Sensor(**sensor_update())
            self.assertIsNotNone(sensor)
            self.assertEqual(sensor.name, sensor_id)
            self.assertEqual(sensor.lux, lux)
            self.assertEqual(sensor.state, state)
            self.assertEqual(sensor.temperature, temperature)
            self.assertIsNone(sensor.flood)

    def test_water_boiler_sensor_update(self):
        temperature = 19.9
        flood = 0
        sensor_id = 'water boiler'

        with boddle(query={'temp': str(temperature), 'flood': flood, 'id': sensor_id}):
            sensor = Sensor(**sensor_update())
            self.assertIsNotNone(sensor)
            self.assertEqual(sensor.name, sensor_id)
            self.assertIsNone(sensor.lux)
            self.assertIsNone(sensor.state)
            self.assertEqual(sensor.temperature, temperature)
            self.assertFalse(sensor.flood)

    def test_list_sensors(self):
        sensors = json.loads(list_sensors())
        self.assertIsInstance(sensors, list)
        self.assertEqual(len(sensors), 3)


if __name__ == '__main__':
    unittest.main()
