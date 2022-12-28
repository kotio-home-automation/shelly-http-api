import json


class IDMapping:

    sensor_names: list[dict]

    def __init__(self, id_mappings_file: str):
        self.file = id_mappings_file
        with open(file=self.file, encoding='UTF-8') as sensor_mapping_file:
            self.sensor_names = json.load(sensor_mapping_file)
        sensor_mapping_file.close()

    def resolve_name(self, sensor_id: str) -> str:
        sensors = filter(lambda s: s['id'] == sensor_id, self.sensor_names)
        matching_sensor = next(sensors, dict())
        return matching_sensor['name'] if len(matching_sensor) > 0 else sensor_id
