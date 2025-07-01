import csv
import pickle
from operator import itemgetter
import traceback

""" TODO
인화성(Flammability) 순으로 정렬하고 정렬한 배열의 내용을 이진 파일형태로 저장 
인화성이 0.7 이상인 목록은 별도로 출력
그 목록을 Mars_Base_Inventory_danger.csv로 저장
"""

"""
라이브러리 설명
csv - csv 파일을 편하게 처리하기 위한 라이브러리
pickle - 파이썬에서 사용하는 자료형을 변환 없이 그대로 파일로 저장하거나 불러올때 쓰는 라이브러리
operator.itemgetter - 리스트의 특정 요소를 기준으 정렬하기 위해 씀.
"""
# Mars_Base_Inventory_danger.csv파일 내용의 컬럼 헤더 설정
column_header = ['Substance', 'Weight (g/cm³)', 'Specific Gravity', 'Strength', 'Flammability']
csv_list = []

try:
    with open('prob3/Mars_Base_Inventory.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)

        # csv 라이브러리로 불러온 내용을 리스트 객체로 변환. 뒤의 [1:]은 2번째 내용부터 저장한다는 뜻.
        # 첫번째 줄엔 ['Substance', 'Weight (g/cm³)', 'Specific Gravity', 'Strength', 'Flammability']
        # 이 내용이 담겨있는데 컬럼 헤더는 정렬하거나 데이터를 다룰땐 쓸모없으니 리스트에 넣을때 제외했음.
        csv_list = list(reader)[1:]

        # 정렬 기준을 인화성(각 리스트 요소의 맨 뒤에 있음)으로, 높은 순으로 정렬해야하니 내림차순으로
        # 어떤 리스트의 맨 뒤에 있는 요소는 -1을 쓰면 편하다.
        # sort 함수의 reverse 인수를 True로 설정하면 내림차순 정렬된다
        csv_list.sort(key=itemgetter(-1), reverse=True)

    with open('prob3/Mars_Base_Inventory_danger.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)

        # 파일의 첫 줄에 컬럼 헤더 삽입
        writer.writerow(column_header)

        print('인화성 물질 목록 (가연성 0.7 이상)')
        # 반복문으로 csv_list 요소 순환
        for c in csv_list:
            """
            # 인화성 수치가 문자열 타입으로 되어있어서 숫자 비교를 할 수 없으니 실수(float) 형태로 타입 캐스팅 해줘야함.
            # 만약 이 전에 컬럼헤더를 따로 떼놓지 않았다면 'Flammability'라는 글자를 실수로 변환할 수 없었을테고, 
            # 그렇게 되면 오류가 떠서 프로그램이 뻗어버릴테니 그 오류에 대한 예외처리를 미리 해놔야 했을것임.
            """
            # 타입 캐스팅 이후에 해당 수치가 0.7 이상이라면 출력하고 Mars_Base_Inventory_danger.csv에 저장
            if float(c[-1]) >= 0.7:
                print(c)
                writer.writerow(c)

    # 이진 파일 형태로 저장
    with open('prob3/Mars_Base_Inventory_List.bin', 'wb') as f:
        pickle.dump(csv_list, f)


    print('\n\n\n저장된 이진파일 Mars_Base_Inventory_List.bin을 불러옵니다.\n')
    # 이진 파일을 불러오는 코드
    with open('prob3/Mars_Base_Inventory_List.bin', 'rb') as f:
        inventory_bin = pickle.load(f)
        # 한 줄씩 출력
        for inv in inventory_bin:
            print(inv)
        
except FileNotFoundError as e:
    print(f"파일을 찾을 수 없습니다. {e}")
except PermissionError:
    print("파일을 열 수 있는 권한이 없습니다.")
except pickle.UnpicklingError as e:
    print(f"pickle로 잘못된 포맷의 파일을 읽으려 시도했습니다. {e}")
except ValueError as e:
    print(f"부적절한 값을 가진 인자를 받았습니다 {e}")
except TypeError as e:
    print(f"잘못된 타입이 전달되었습니다. {e}")
except EOFError as e:
    print(f"이진 파일 데이터를 이미 다 읽었지만 계속 읽으려 시도 했습니다.(End of File Error) {e}")
    print(traceback.print_exc())