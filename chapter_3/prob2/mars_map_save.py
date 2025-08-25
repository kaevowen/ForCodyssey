import csv
import matplotlib.pyplot as plt

output_file = 'chapter_3/prob2/mars_map.png'


def prepare_struct_data(filename='chapter_3/prob2/map.csv'):
    map_points = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            p = {
                'x': int(row[0]),
                'y': int(row[1]),
                'category': row[2]
            }
            map_points.append(p)
    
    return map_points


def load_rock_data(filename='chapter_3/prob1/area_map.csv'):
    rock_points = []

    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            is_mountain = int(row[2])
            
            # area가 1이고, mountain이 1인 경우에만 좌표를 추가
            if is_mountain == 1:
                point = {'x': int(row[0]), 'y': int(row[1])}
                rock_points.append(point)
    return rock_points

struct_data = prepare_struct_data()
rock_data = load_rock_data()
# print(plot_data)

# --- 2단계: 지도 틀 생성 시작 ---

# 1. 도화지(figure)와 좌표계(axes)를 준비합니다.
fig, ax = plt.subplots(figsize=(10, 10))

# 2. 지도의 최대 크기를 결정합니다. (데이터의 x, y 최대값 기준)
# 데이터가 없는 경우를 대비해 기본값 15를 설정합니다.
max_x = 15
max_y = 15

# 3. 축의 범위와 눈금을 설정합니다. 0부터 시작하지 않도록 0.5부터 설정합니다.
ax.set_xlim(0.5, max_x + 0.5)
ax.set_ylim(max_y + 0.5, 0.5)  # Y축은 아래로 갈수록 커지도록 순서를 반대로 지정

# 4. 그리드(격자)를 그리고, 눈금을 1단위로 설정합니다.
ax.set_xticks(range(1, max_x + 1))
ax.set_yticks(range(1, max_y + 1))
ax.grid(True)

# 5. 축 레이블을 설정합니다.
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Mars Area Map')

# 6. 좌표계의 가로 세로 비율을 동일하게 맞춥니다.
ax.set_aspect('equal', adjustable='box')


for p in rock_data:
    ax.scatter(p['x'], p['y'], marker='o', color='brown', s=1700, label='Rock')


for p in struct_data:
    x = p['x']
    y = p['y']
    category = p['category']

    # !!! 디버깅을 위해 현재 처리 중인 데이터 출력 !!!
    # print(f"처리 중 -> x: {x}, y: {y}, category: '{category}'")

    if category == 'nan':
        pass

    # 조건: 이름에 'Base'가 포함된 기지인 경우
    elif 'Base' in category:
        ax.scatter(x, y, marker='^', color='green', s=200, label='Base')
        
    # 조건: 그 외 기타 구조물인 경우
    else:
        ax.scatter(x, y, marker='s', color='gray', s=150, label='Structure')

# --- 최종 저장 ---
# 최종 파일 이름인 mars_map.png로 저장합니다.
plt.savefig(output_file)
plt.close(fig)

print(f"모든 데이터가 포함된 지도가 '{output_file}'로 저장되었습니다.")