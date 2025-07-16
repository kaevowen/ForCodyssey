# numpy 라이브러리를 np라는 별명으로 불러들임. 이러면 numpy.함수 가 아닌 np.함수 로도 사용이 가능해진다.
import numpy as np

# genfromtxt 함수에 들어간 인수에 대한 설명
# delimiter : 구분자가 , 로 되어있으니 ,를 기준으로 데이터를 구분한다
# dtype : 배열의 데이터 타입을 지정하는 인수. object를 쓰면 각 배열에 대해 "알아서 적당히" 데이터 타입을 정해준다.
# (아무거나 집어넣은 상자에 비유할 수 있음.)
# 또는 [(컬럼1, 데이터 타입), (컬럼2, 데이터 타입)] 이런식으로 명시적으로 지정해줄수도있다.
# (상자에 물건을 집어넣고 거기에 이름표를 붙이는것에 비유할 수 있음.)
# 속도는 후자가 훨씬 빠름. 지금은 표본이 적어 속도차이를 느낄 수 없지만 
# 보통 이런식의 데이터 전처리는 엄청난 양의 데이터를 동반하므로 나중엔 적절한 데이터 타입의 정의가 필요하다고 생각함.
# 
# encoding : 인코딩 방식을 설정
# skip_header : 읽어들이는 파일의 n번째를 스킵한다. 보통 첫번째에 컬럼헤더가 존재하는데 이건 데이터 처리에 필요가 없으니 스킵함.


# U30 : 최대 30글자의 유니코드 문자열
# i4 : 32비트 정수형

data_type = [('parts', 'U30'), ('strength', 'i4')]
mars_base_main_parts = [
    np.genfromtxt('chapter_1/prob5/mars_base_main_parts-001.csv', 
                  delimiter=',', dtype=data_type, 
                  encoding='utf-8', skip_header=1),
    np.genfromtxt('chapter_1/prob5/mars_base_main_parts-002.csv', 
                  delimiter=',', dtype=data_type, 
                  encoding='utf-8', skip_header=1),
    np.genfromtxt('chapter_1/prob5/mars_base_main_parts-003.csv', 
                  delimiter=',', dtype=data_type, 
                  encoding='utf-8', skip_header=1)
]

# [이름, 값1, 값2, 값3] 이런 형태로 합칠거임. 행렬의 크기가 같으므로 column_stack 함수로 쉽게 병합이 가능함
parts = np.column_stack([
    mars_base_main_parts[0]['parts'],
    mars_base_main_parts[0]['strength'],
    mars_base_main_parts[1]['strength'],
    mars_base_main_parts[2]['strength']
    ])

# parts의 첫번째값부터 끝까지(숫자가 담겨있는 부분임) 실수형으로 변환
# 그 후에 산술 평균값을 계산함
parts_strength = parts[:, 1:].astype(float)
parts_strength_average = np.mean(parts_strength, axis=1)

# 평균이 50 미만인 값을 추려내기 위한 마스크
# parts[is_weak]는 50 미만인 값들을 추려내고 그 결과를 parts_to_work_on에 할당한다
is_weak = parts_strength_average < 50
parts_to_work_on = parts[is_weak]

# 그 후 parts_to_work_on.csv에 저장함
# part, s1, s2, s3
# material, s1, s2, s3 
# 이런 형태로 저장됨
column_header = 'part, s1, s2, s3'
np.savetxt(
    'chapter_1/prob5/parts_to_work_on.csv', 
    parts_to_work_on, 
    delimiter=',', 
    fmt='%s', 
    header=column_header, 
    comments=''
)