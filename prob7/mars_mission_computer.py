import random
import logging
from time import sleep
import json

logging.basicConfig(
    level=logging.INFO,
    format='---- %(asctime)s ----%(message)s',
    handlers=[
        logging.FileHandler('prob6/mars.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature':0,
            'mars_base_external_temperature':0,
            'mars_base_internal_humidity':0,
            'mars_base_external_illuminance':0,
            'mars_base_internal_co2':0,
            'mars_base_internal_oxygen':0
        }

        self.avg_env_values = {
            'mars_base_internal_avg_temperature':0,
            'mars_base_external_avg_temperature':0,
            'mars_base_internal_avg_humidity':0,
            'mars_base_external_avg_illuminance':0,
            'mars_base_internal_avg_co2':0,
            'mars_base_internal_avg_oxygen':0          
        }

        # get average values when avg_count reached at 60(5 minutes)
        # increased value at 5 seconds
        self.avg_count = 0

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 1)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 1)
        self.env_values['mars_base_internal_humidity'] = random.randrange(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randrange(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 1)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 1)


    def get_avg_env(self):
        return self.avg_env_values
    

    def get_env(self):
        return self.env_values
    

    def get_sensor_average_data(self):
        for key in self.avg_env_values.keys():
            self.avg_env_values[key] /= 60

        return json.dumps(self.get_avg_env(), indent=4)


    def init_avg_env(self):
        for key in self.avg_env_values.keys():
            self.avg_env_values[key] = 0

        self.avg_count = 0

    def get_sensor_data(self):
        self.set_env()
        self.avg_env_values['mars_base_internal_avg_temperature'] += self.env_values['mars_base_internal_temperature']
        self.avg_env_values['mars_base_external_avg_temperature'] += self.env_values['mars_base_external_temperature']
        self.avg_env_values['mars_base_internal_avg_humidity'] += self.env_values['mars_base_internal_humidity']
        self.avg_env_values['mars_base_external_avg_illuminance'] += self.env_values['mars_base_external_illuminance']
        self.avg_env_values['mars_base_internal_avg_co2'] += self.env_values['mars_base_internal_co2']
        self.avg_env_values['mars_base_internal_avg_oxygen'] += self.env_values['mars_base_internal_oxygen']
        
        self.avg_count += 1
        return json.dumps(self.get_env(), indent=4)


RunComputer = MissionComputer()


while True:
    print("------- Sensor Data -------")
    print(RunComputer.get_sensor_data())
    print(RunComputer.avg_count)
    if RunComputer.avg_count == 60:
        print("------- Average Sensor Data (5 minutes) -------")
        print(RunComputer.get_sensor_average_data())
        RunComputer.init_avg_env()

    sleep(5)