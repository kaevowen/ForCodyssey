import json
import platform
import subprocess
import sys

try:
    import psutil

except ImportError:
    print('의존성 오류. psutil가 설치되어 있지 않습니다. psutil을 설치합니다.')
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psutil'])
        import psutil

    except subprocess.CalledProcessError as e:
        print('의존성 설치 중 오류가 발생했습니다. : {e}')
        sys.exit(1)


class MissionComputer:
    def __init__(self):
        try:
            self.system_info = {
                'operating_system' : f'{platform.system()}',
                'operating_system_version': f'{platform.release()}',
                'type_of_cpu' : f'{platform.architecture()}',
                'number_of_cpu_cores' : f'{psutil.cpu_count()}',
                'total_memory_size' : f'{psutil.virtual_memory().total}',
            }
            
            self.current_computer_usage = {
                'cpu_usage': psutil.cpu_percent(),
                'memory_usage': psutil.virtual_memory().percent
            }

        except PermissionError:
            print("권한이 부족합니다. 관리자나 루트 권한으로 실행시켜 주세요.")

        except NotImplemented:
            print('지원하지 않는 운영체제 또는 환경 입니다.')

        except FileNotFoundError:
            print('파일 시스템/드라이버 오류')
        except OSError:
            print('지원하지 않는 운영체제 또는 환경 입니다.')

        except IOError:
            print('파일 시스템/드라이버 오류')

        except AttributeError:
            print('지금 설치된 psutil 라이브러리에 해당 함수가 없습니다. 버전을 확인해주세요.')

    def get_mission_computer_info(self):
        print(json.dumps(self.system_info))

    def get_mission_computer_load(self):
        try:
            current_computer_usage_json_format = json.dumps(self.current_computer_usage)
            print(current_computer_usage_json_format)

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


RunComputer = MissionComputer()
RunComputer.get_mission_computer_info()
RunComputer.get_mission_computer_load()