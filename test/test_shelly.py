import unittest
from dataclasses import replace

from sensor.shelly import Shelly, Sensor

TWO_SENSORS_READINGS_FILE = 'test/two_sensors.json'

NAME_KITCHEN = 'kitchen'

NAME = 'name'


class ShellyTestCase(unittest.TestCase):
    def test_list_has_no_sensors(self):
        shelly = Shelly('test/no_sensors.json')
        sensors = shelly.list_sensors()
        self.assertEqual(sensors, list())

    def test_list_has_two_sensors(self):
        shelly = Shelly(TWO_SENSORS_READINGS_FILE)
        sensors = shelly.list_sensors()
        self.assertEqual(len(sensors), 2)

    def test_list_has_kitchen_door_sensor(self):
        shelly = Shelly(TWO_SENSORS_READINGS_FILE)
        sensors = shelly.list_sensors()
        kitchen_sensors = list(filter(lambda sensor: sensor[NAME] == NAME_KITCHEN, sensors))
        self.assertEqual(len(kitchen_sensors), 1)

        kitchen_sensor = Sensor(**kitchen_sensors[0])
        self.assertEqual(kitchen_sensor.lux, 0)
        self.assertEqual(kitchen_sensor.state, 'closed')
        self.assertEqual(kitchen_sensor.temperature, 21.1)
        self.assertIsNone(kitchen_sensor.flood)

    def test_list_has_foyer_flood_sensor(self):
        shelly = Shelly(TWO_SENSORS_READINGS_FILE)
        sensors = shelly.list_sensors()
        foyer_sensors = list(filter(lambda sensor: sensor[NAME] == 'foyer', sensors))
        self.assertEqual(len(foyer_sensors), 1)

        foyer_sensor = Sensor(**foyer_sensors[0])
        self.assertIsNone(foyer_sensor.lux)
        self.assertIsNone(foyer_sensor.state)
        self.assertEqual(foyer_sensor.temperature, 20.1)
        self.assertFalse(foyer_sensor.flood)

    def test_update_kitchen_sensor_state(self):
        shelly = Shelly(TWO_SENSORS_READINGS_FILE)
        sensors = shelly.list_sensors()
        kitchen_sensors = list(filter(lambda sensor: sensor[NAME] == NAME_KITCHEN, sensors))
        self.assertEqual(len(kitchen_sensors), 1)

        kitchen_sensor = Sensor(**kitchen_sensors[0])
        update_kitcher_sensor = replace(kitchen_sensor, state='open')
        self.assertNotEqual(kitchen_sensor, update_kitcher_sensor)

        shelly.update_sensors_data(update_kitcher_sensor)

        updated_sensors = shelly.list_sensors()
        updated_kitchen_sensors = list(filter(lambda sensor: sensor[NAME] == NAME_KITCHEN, updated_sensors))
        self.assertEqual(len(updated_kitchen_sensors), 1)
        self.assertNotEqual(kitchen_sensor, updated_kitchen_sensors)

        updated_kitchen_sensor = Sensor(**updated_kitchen_sensors[0])
        self.assertEqual(updated_kitchen_sensor, update_kitcher_sensor)

    def test_add_new_sensor(self):
        shelly = Shelly(TWO_SENSORS_READINGS_FILE)
        sensors = shelly.list_sensors()

        new_sensor = Sensor('test', 1, 'open', -12.3, None)
        shelly.update_sensors_data(new_sensor)
        new_sensors = shelly.list_sensors()
        self.assertEqual(len(new_sensors), len(sensors) + 1)

        sensor_names = list(map(lambda sensor: sensor[NAME], new_sensors))
        self.assertIn(new_sensor.name, sensor_names)


if __name__ == '__main__':
    unittest.main()
