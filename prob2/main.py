import json

log_lists = []
# json으로 변환하기 위한 리스트 객체
log_json = []

# prob2 폴더에 있는 mission_computer_main.log 파일을 열어 log_file 변수에 할당함.
with open('prob2/mission_computer_main.log') as log_file:

    # string.split() - 문자열을 split 안의 문자나 문자열 기준으로 나눠서 리스트 형태로 만들어줌.
    # 문제의 log는 콤마(,) 형태로 저장된 csv(Comma Seperated Value)파일이라는 설정임. 
    # 콤마를 기준으로 나눠서 리스트에 저장해줌.
    # 저장 형태는 리스트안의 리스트같은 형태임
    # [ [1,2,3], [4,5,6], [7,8,9]] 같은...
    for line in log_file:
        log_csv = line.split(',')
        log_lists.append(log_csv)
        log_json.append(
            {
                'timestamp': log_csv[0],
                'event': log_csv[1],
                # log_csv[2]에는 메세지가 담겨있음. 해당 문자열의 끝에 개행문자('\n')가 존재해서 strip()으로 제거해줘야함.
                'message': log_csv[2].strip()
            }
        )

# 전환된 리스트 객체 출력
for log in log_lists:
    print(log)


print('------------------- 구분선 -------------------')

# 리스트 역순 출력
# list.reverse()는 리스트를 뒤집지만
# reversed(list)는 뒤집어진 리스트를 반환함.
# 원본에 영향을 주지 않는것이 차이점
for log in reversed(log_lists):
    print(log)

with open('prob2/mission_computer_main.json', 'w+', encoding='utf-8') as f:
    f.write(json.dumps(log_json))
