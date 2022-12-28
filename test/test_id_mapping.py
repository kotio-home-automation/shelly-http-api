import unittest

from sensor.id_mapping import IDMapping


class IDMappingTestCase(unittest.TestCase):
    def test_name_is_resolved_from_id(self):
        id_mapping = IDMapping('test/single_mapping.json')
        sensor_id = '1-a'
        sensor_name = 'foyer'
        resolved_sensor_name = id_mapping.resolve_name(sensor_id)
        self.assertEqual(sensor_name, resolved_sensor_name)

    def test_name_is_resolved_as_id_by_default(self):
        id_mapping = IDMapping('test/single_mapping.json')
        sensor_id = '1-b'
        resolved_sensor_name = id_mapping.resolve_name(sensor_id)
        self.assertEqual(sensor_id, resolved_sensor_name)


if __name__ == '__main__':
    unittest.main()
