# 계산 / 저장을 위한 전역변수들
pi = 3.141592
material_result = 0
diameter_result = 0
thickness_result = 0
area_result = 0
weight_result = 0

# 돔의 면적을 구하는 함수. 인수로 재료, 지름, 두께를 받는다. 
# 두께는 기본값이 1로 설정되어있다.
def shape_area(material, diameter, thickness=1):
    # 전역변수로 지정해 값이 저장 될 수 있도록 한다.
    # global 키워드로 지정하지 않으면 값이 외부로 전달되지 않는다.
    global material_result, diameter_result, thickness_result, area_result, weight_result
    """
    계산해야 할 것
    반구 면적 = 2πr² (r = diameter / 2)
    면적 단위: m² → cm² (곱하기 10,000)
    무게 = 면적(cm²) × 두께(cm) × 밀도 (g/cm³)
    무게 단위 변환: g → kg (나누기 1,000)
    화성 중력 보정: 지구 중량의 × 0.38
    """

    # 재료의 이름과 값을 저장하기 위한 dictionary 형식
    materials = {
        '유리': 2.4,
        '알루미늄':2.7,
        '탄소강': 7.85
    }

    # 재질, 지름, 두께, 면적, 무게를 구하는 구간
    r = diameter / 2
    area_cm2 = (2 * pi * (r ** 2)) * 10000
    density = materials[material]
    volumn_cm3 = area_cm2 * thickness
    weight_kg = volumn_cm3 * density / 1000
    mars_weight = weight_kg * 0.38

    material_result = material
    diameter_result = diameter
    thickness_result = thickness
    area_result = round(area_cm2/10000, 3)
    weight_result = round(mars_weight, 3)
    
    print(f'재질 ==> {material_result}, ' 
          f'지름 ==> {diameter_result}, '
          f'두께 ==> {thickness_result}, '
          f'면적 ==> {area_result}, '
          f'무게 ==> {weight_result}kg')


def is_float(value):
    try:
        float(value)
        return True
    except:
        return False


def get_valid_diameter():
    while True:
        diameter_input = input('돔의 지름을 입력하세요(단위: m) : ').strip()
        if not is_float(diameter_input):
            print('숫자가 아닌 값이 입력되었습니다.')
            continue

        # 문자열이 아니면 실수형으로 변환
        diameter_input = float(diameter_input)
        if diameter_input <= 0:
            print('지름은 0이거나 음수일 수 없습니다.')
            continue

        return diameter_input
    

def get_valid_material():
    while True:
        material_input = input('재질을 입력하세요(유리, 알루미늄, 탄소강). '
                               '아무것도 입력하지 않으면 기본값인 유리가 선택됩니다. : ').strip()
        
        if material_input == '':
            print('아무것도 입력하지 않아 기본값인 유리가 선택되었습니다.')
            return '유리'
        
        elif material_input in ['유리', '알루미늄', '탄소강']:
            return material_input
        
        else :
            print('사용할 수 없는 재료입니다. 유리, 알루미늄, 탄소강 중 선택해주세요.')
            continue

# 사용 가능한 재료 유리 / 알루미늄 / 탄소강
# 화성의 무게는 지구 대비 38% 수준. weight 계산시에 0.38을 곱할것
# 결과는 소수점이하 세자리까지

# 지름은 0이 될 수 없음
# 한번 출력했다고 끝이 아니라 계속 쓸 수 있어야함.
# 계산이 필요 없을땐 종료할 수 있어야함.
# 출력형식 재질 ==> 유리, 지름 ==> 000, 두께 ==> 000, 면적 ==> 000, 무게 ==> 000kg

# 계산이 다 끝난 후 다시 계산 할 것인지 판별하기 위한 변수. 처음에 한 번은 무조건 실행해야하니 True로 설정
condition = True

# condition이 False가 될때까지 반복한다.

#                       ----- 프로그램의 전체적인 흐름 -----
# 입력받은 지름과 재료가 유효한 값인지 판별하고(get_valid_diameter, get_valid_material)
# 유효하지 않은 값이라면 유효한 값을 받을때까지 반복
# 유효한 값이라면 shape_area에 해당 값을 전달해 계산 수행(shpae_area(material, diameter))
# 계산완료 후 다시 계산을 수행할것인지 물어봄. Y/N 둘중에 하나를 입력값으로 받고 나머지는 무시됨.
while condition:
    diameter = get_valid_diameter()
    material = get_valid_material()
    shape_area(material, diameter)
    print(area_result, weight_result)
    while True:
        q = input('계산이 완료되었습니다. 다른 값으로 계속 계산할까요? (Y/N)')
        if not q.upper() in ['Y', 'N']:
            continue

        # 사용자가 N을 입력했다면 condition 변수에 False를 할당한다.
        elif q.upper() == 'N':
          print('프로그램을 종료합니다.')  
          condition = False
          break