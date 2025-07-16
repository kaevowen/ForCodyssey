import random
import logging
from time import sleep
import json
import threading
import os
import sys


if os.name == 'nt':
    import msvcrt
elif os.name =='posix':
    import tty
    import termios

flag = False

logging.basicConfig(
    level=logging.INFO,
    format='---- %(asctime)s ----%(message)s',
    handlers=[
        logging.FileHandler('chapter_1/prob6/mars.log', encoding='utf-8'),
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
        # 평균수치의 모든 값을 초기화
        for key in self.avg_env_values.keys():
            self.avg_env_values[key] = 0

        # 5분마다 한번씩 출력할때 쓰는 함수도 초기화
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


def main_sensor_loop():
    RunComputer = MissionComputer()

    while not flag:
        print("------- Sensor Data -------")
        print(RunComputer.get_sensor_data())
        if RunComputer.avg_count == 60:
            print("------- Average Sensor Data (5 minutes) -------")
            # print(RunComputer.get_sensor_average_data())
            RunComputer.init_avg_env()

        # 0.05초씩 100번 총 5초 쉬는 함수. 키 입력을 받았을때 즉각적으로 프로그램을 종료하기 위해 단위를 좀 줄였음.
        for _ in range(100):
            if flag:
                break
            sleep(0.05)


def keystroke_listener():
    global flag

    if os.name == 'nt':
        print("[Windows] 종료하려면 아무 키나 누르세요.")
        while not flag:
            if msvcrt.kbhit():
                key = msvcrt.getch().decode() # 바이트를 문자열로 디코딩
                print(f"'{key}' 키 감지됨. 시스템 종료 중...")
                flag = True
                break
            time.sleep(0.01) # CPU 과부하 방지

    elif os.name == 'posix':
        # 터미널 설정 저장
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno()) # 터미널 raw 모드 설정
            print("[Linux/macOS] 종료하려면 아무 키나 누르세요.")
            while not flag:
                if sys.stdin.readable():
                    key = sys.stdin.read(1) # 한 글자 읽기
                    print(f"keystroke detected... System stopped...")
                    flag = True
                    break
                sleep(0.01) # CPU 과부하 방지

        finally:
            # 터미널 설정 복원 (매우 중요!)
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    else:
        # 지원하지 않는 OS인 경우
        print("경고: 현재 운영체제에서는 엔터 없는 키 입력을 지원하지 않습니다.")
        print("종료하려면 'q'를 입력하고 엔터를 누르세요.")
        user_input = input()
        if user_input.lower() == 'q':
            flag = True


ks_thread = threading.Thread(target=keystroke_listener)
ks_thread.daemon = True
ks_thread.start()

main_sensor_loop()