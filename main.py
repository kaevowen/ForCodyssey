try:
    # mission_computer_main.log 파일을 열고 그 객체를 log_file 변수에 할당한다
    # with open 구문은 기본적으론 a = open(), a.close()와 같음
    # with open 구문을 이용하면 변수선언, 할당, 파일 닫기까지 해줌
    with open('mission_computer_main.log') as log_file:

        # for문으로 log_file(mission_computer_main.log) 에 있는 글을 한 줄씩 불러옴
        for log_line in log_file:
            print(log_line)        

        # 구분용 출력선
        print("----------------- 거꾸로 출력하기 -----------------\n")

    #위 with open 구문과 같음.
    with open('mission_computer_main.log') as log_file:
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