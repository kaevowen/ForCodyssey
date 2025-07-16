import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format='---- %(asctime)s ----%(message)s',
    handlers=[
        logging.FileHandler('chapter_1/prob6/mars.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature':0,
            'mars_base_external_temperature':0,
            'mars_base_internal_humidity':0,
            'mars_base_external_illuminance':0,
            'mars_base_internal_co2':0,
            'mars_base_internal_oxygen':0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 1)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 1)
        self.env_values['mars_base_internal_humidity'] = random.randrange(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randrange(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 1)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 1)


    def get_env(self):
        logging.info(
            f'\n화성 기지 내부 온도 : {self.env_values['mars_base_internal_temperature']}°C\n'
            f'화성 기지 외부 온도 : {self.env_values['mars_base_external_temperature']}°C\n'
            f'화성 기지 내부 습도 : {self.env_values['mars_base_internal_humidity']}%\n'
            f'화성 기지 외부 광량 : {self.env_values['mars_base_external_illuminance']}W/m2\n'
            f'화성 기지 내부 이산화탄소 농도 : {self.env_values['mars_base_internal_co2']}%\n'
            f'화성 기지 내부 산소 농도 : {self.env_values['mars_base_internal_oxygen']}%\n'
        )
        return self.env_values
    
ds = DummySensor()

ds.set_env()
ds.get_env()