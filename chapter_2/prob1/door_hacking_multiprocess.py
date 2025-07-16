import zipfile
import itertools
import string
import time
import multiprocessing


def brute_worker(prefixes, path, target, charset, length, found_flag, result_queue):
    try:
        with zipfile.ZipFile(path) as zf:
            attempt = 0
            start_time = time.perf_counter()

            for prefix in prefixes:
                for suffix in itertools.product(charset, repeat=length - len(prefix)):
                    if found_flag.is_set():
                        return  # 다른 프로세스가 성공함
                    attempt += 1
                    password = (prefix + ''.join(suffix)).encode()

                    try:
                        with zf.open(target, pwd=password) as f:
                            data = f.read()

                            elapsed = time.perf_counter() - start_time
                            print(f"\n[+] 성공: {password.decode()} | 시도: {attempt} | 시간: {elapsed:.2f}s")

                            found_flag.set()
                            result_queue.put(data)
                            return
                    except:
                        if attempt % 100000 == 0:
                            elapsed = time.perf_counter() - start_time
                            print(f"시도: {attempt} | 속도: {attempt / elapsed:.2f}개/s", end='\r')
                        continue
    except Exception as e:
        print(f"\n[!] 오류 발생: {e}")


def unlock_zip_multiproc(path, target, charset, length):
    # 문자 집합을 3등분
    charset_list = list(charset)
    chunk_size = len(charset_list) // 3
    chunks = [
        charset_list[:chunk_size],
        charset_list[chunk_size:2 * chunk_size],
        charset_list[2 * chunk_size:]
    ]
    print(chunks[0])
    print(chunks[1])
    print(chunks[2])
    # 프로세스 통신 도구
    found_flag = multiprocessing.Event()
    result_queue = multiprocessing.Queue()

    processes = []
    for chunk in chunks:
        prefixes = [''.join(p) for p in itertools.product(chunk, repeat=1)]
        p = multiprocessing.Process(
            target=brute_worker,
            args=(prefixes, path, target, charset, length, found_flag, result_queue)
        )
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    # 결과 저장
    if not result_queue.empty():
        try:
            with open('prob2/password.txt', 'wb') as f:
                f.write(result_queue.get())
            print("[+] 압축 해제된 파일을 'password.txt'로 저장했습니다.")
        except Exception as e:
            print(f"[!] 파일 저장 실패: {e}")
    else:
        print("[-] 실패: 비밀번호를 찾지 못했습니다.")


# 실행 예시
if __name__ == '__main__':
    import string

    zip_path = 'chapter_2/prob1/emergency_storage_key.zip'
    target_file = 'password.txt'
    charset = string.ascii_lowercase + string.digits
    length = 6

    unlock_zip_multiproc(zip_path, target_file, charset, length)