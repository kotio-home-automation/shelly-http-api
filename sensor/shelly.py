import json
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Sensor:
    name: str
    time: float
    lux: Optional[int]
    state: Optional[str]
    temperature: float
    flood: Optional[bool]


class Shelly:

    sensor_readings: list[dict]

    def __init__(self, readings_file: str):
        self.file = readings_file
        with open(file=self.file, encoding='UTF-8') as sensor_readings_file:
            self.sensor_readings = json.load(sensor_readings_file)
        sensor_readings_file.close()

    def list_sensors(self) -> list[dict]:
        return self.sensor_readings

    def update_sensors_data(self, sensor: Sensor) -> Sensor:
        other_sensors = list(filter(lambda known_sensor: known_sensor['name'] != sensor.name, self.sensor_readings))
        other_sensors.append(asdict(sensor))
        self.sensor_readings = other_sensors

        return sensor

    def write_sensor_data(self):
        with(open(file=self.file, mode='w', encoding='UTF-8')) as sensor_readings_file:
            sensor_data = json.dumps(self.sensor_readings)
            sensor_readings_file.write(sensor_data)
