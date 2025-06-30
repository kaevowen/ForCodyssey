# 지구였으면 Hello World인데 화성이라 Hello Mars
print('Hello Mars')

# try - except 구문
# try 안의 코드를 실행하다가 어떤 오류가 발생한다면 except 구문으로 넘어가 거기에 있는 코드를 실행한다.
# 이 코드의 경우엔 
# 파일을 찾지 못했을때(FileNotFoundError)
# 파일을 열었는데 인코딩이 utf-8가 아니라 제대로 읽을 수 없을때 (UnicodeDecodeError)
# 그 외 알 수 없는 오류가 발생한다면(Exception) 그 오류의 내용을 변수 e에 할당하고 출력한다.
try:
    # mission_computer_main.log 파일을 열고 그 객체를 log_file 변수에 할당한다
    # with open 구문은 기본적으론 a = open(), a.close()와 같음
    # with open 구문을 이용하면 변수선언, 변수할당, 파일 닫기까지 해줌
    with open('prob1/mission_computer_main.log') as log_file:

        # for문으로 log_file(mission_computer_main.log) 에 있는 글을 한 줄씩 불러옴
        for log_line in log_file:
            print(log_line)        


    # 구분용 출력선
    print("----------------- 거꾸로 출력하기 -----------------\n")

    #위 with open 구문과 같음.
    with open('prob1/mission_computer_main.log') as log_file:
        # 거꾸로 출력하기 위해 log_file.readlines()를 이용해 log_file을 전체적으로 읽어줌
        # log_file.read() -> 한 줄만 읽기 // log_file.readlines() -> 전체적으로 읽기(그 파일의 끝까지)
        # readlines()로 로그파일을 읽어올 경우 개행(엔터키)을 기준으로 한 줄씩 List 형태로 저장됨.
        # List ? -> 파이썬 자료형중 하나인데 어떤 데이터들을 담기 편하게 만들어져있음.
        # 그 리스트를 log_reversed라는 변수에 할당함.
        log_reversed = log_file.readlines()

        # log_reversed에 저장 되어있는 리스트를 reverse() 함수로 뒤집음.
        log_reversed.reverse()

        # 뒤집은 리스트를 하나씩 출력함
        for log_line in log_reversed:
            print(log_line)

except FileNotFoundError:
    print("파일을 찾을 수 없습니다. 파일명 : mission_computer_main.log")
except UnicodeDecodeError:
    print("파일을 utf-8로 디코딩할 수 없습니다.")
except Exception as e:
    print(f"알 수 없는 에러 발생: {e}")