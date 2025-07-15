import random
import logging
from time import sleep
import json
import threading
import os
import sys
import platform
import os
import json

from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process, Value

if os.name == 'nt':
    import msvcrt
elif os.name =='posix':
    import tty
    import termios

logging.basicConfig(
    level=logging.INFO,
    format='---- %(asctime)s ----%(message)s',
    handlers=[
        logging.FileHandler('prob6/mars.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

flag = Value('b', False)

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

    def get_mission_computer_info(self, flag):
        print("computer info")
        try:
            import psutil

            while True:
                operating_system = platform.system()
                operating_system_version = platform.release()
                type_of_cpu = platform.architecture()
                number_of_cpu_cores = psutil.cpu_count()
                total_memory_size = psutil.virtual_memory().total
                print(f'operating system : {operating_system}\n'
                    f'system version : {operating_system_version}\n'
                    f'cpu types : {type_of_cpu}\n'
                    f'cpu cores : {number_of_cpu_cores}\n'
                    f'total memory size : {total_memory_size}\n'
                    )
                
                for _ in range(400):
                    if flag.value:
                        return
                    sleep(0.05)

        except PermissionError:
            print("권한이 부족합니다. 관리자나 루트 권한으로 실행시켜 주세요.")
        except NotImplemented:
            print('지원하지 않는 운영체제 또는 환경 입니다.')
        except OSError:
            print('지원하지 않는 운영체제 또는 환경 입니다.')
        except IOError:
            print('파일 시스템/드라이버 오류')
        except FileNotFoundError:
            print('파일 시스템/드라이버 오류')
        except AttributeError:
            print('지금 설치된 psutil 라이브러리에 해당 함수가 없습니다. 버전을 확인해주세요.')
        except ImportError:
            print('psutil 라이브러리가 설치되어 있지 않습니다. pip install psutil을 통해 설치해주세요.')

    def get_mission_computer_load(self, flag):
        print("computer load")
        try:
            import psutil

            while True:
                current_computer_usage = {
                    'cpu_usage': psutil.cpu_percent(),
                    'memory_usage': psutil.virtual_memory().percent
                }

                print(json.dumps(current_computer_usage))

                # 0.05초씩 400번 총 20초 쉬는 함수. 키 입력을 받았을때 즉각적으로 프로그램을 종료하기 위해 단위를 좀 줄였음.
                for _ in range(400):
                    if flag.value:
                        return
                    sleep(0.05)

        except PermissionError:
            print("권한이 부족합니다. 관리자나 루트 권한으로 실행시켜 주세요.")
        except NotImplemented:
            print('지원하지 않는 운영체제 또는 환경 입니다.')
        except OSError:
            print('지원하지 않는 운영체제 또는 환경 입니다.')
        except IOError:
            print('파일 시스템/드라이버 오류')
        except FileNotFoundError:
            print('파일 시스템/드라이버 오류')
        except AttributeError:
            print('지금 설치된 psutil 라이브러리에 해당 함수가 없습니다. 버전을 확인해주세요.')
        except ImportError:
            print('psutil 라이브러리가 설치되어 있지 않습니다. pip install psutil을 통해 설치해주세요.')
      
    def init_avg_env(self):
        # 평균수치의 모든 값을 초기화
        for key in self.avg_env_values.keys():
            self.avg_env_values[key] = 0

        # 5분마다 한번씩 출력할때 쓰는 함수도 초기화
        self.avg_count = 0

    def get_sensor_data(self, flag):
        print("sensor data")
        while True:
            self.set_env()
            self.avg_env_values['mars_base_internal_avg_temperature'] += self.env_values['mars_base_internal_temperature']
            self.avg_env_values['mars_base_external_avg_temperature'] += self.env_values['mars_base_external_temperature']
            self.avg_env_values['mars_base_internal_avg_humidity'] += self.env_values['mars_base_internal_humidity']
            self.avg_env_values['mars_base_external_avg_illuminance'] += self.env_values['mars_base_external_illuminance']
            self.avg_env_values['mars_base_internal_avg_co2'] += self.env_values['mars_base_internal_co2']
            self.avg_env_values['mars_base_internal_avg_oxygen'] += self.env_values['mars_base_internal_oxygen']
            
            self.avg_count += 1
            print(json.dumps(self.get_env()))
            # 0.05초씩 400번 총 20초 쉬는 함수. 키 입력을 받았을때 즉각적으로 프로그램을 종료하기 위해 단위를 좀 줄였음.
            for _ in range(400):
                if flag.value:
                    return
                sleep(0.05)


def keystroke_listener(flag):

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
            while not flag.value:
                if sys.stdin.readable():
                    key = sys.stdin.read(1) # 한 글자 읽기
                    print(f"keystroke detected... System stopped...")
                    flag.value = True
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


runComputer = MissionComputer()

# ks_process = Process(target=keystroke_listener, args=(flag,))
# ks_process.start()


print("Starting Mission Processes... Press Any key to stop...")
p1 = Process(target=runComputer.get_mission_computer_info, args=(flag,))
p2 = Process(target=runComputer.get_mission_computer_load, args=(flag,))
p3 = Process(target=runComputer.get_sensor_data, args=(flag,))
ks = threading.Thread(target=keystroke_listener, args=(flag,))

p1.start()
p2.start()
p3.start()
ks.start()
p1.join()
p2.join()
p3.join()
