import itertools
import string
import zipfile
import time

# the password is 6 digits with lower alphabet and numbers
# the worst case is 26+10^6 = 2,176,782,336
def unlock_zip(path, target, charset, length):
    attempt = 0
    start_time = time.perf_counter()

    with zipfile.ZipFile(path) as zf:
        for candidate in itertools.product(charset, repeat=length):
            attempt += 1
            password = ''.join(candidate).encode()
            end = time.perf_counter()
            try:
                with zf.open(target, pwd=password) as f:
                    data = f.read()
                    print(
                        f'Success! the password is {password}\n'
                        f'Attempt : {attempt:>7} / '
                        f'Elapsed : {end-start_time:.3f} / '
                        f'Processing speed {attempt / elapsed_time:>8.2f}/s'
                    )

            except:
                elapsed_time = time.perf_counter() - start_time
                print(
                    f'Attempt : {attempt:>7} / '
                    f'Elapsed : {end-start_time:.3f} / '
                    f'Processing speed {attempt / elapsed_time:>8.2f}/s',
                    end='\r'
                )
                continue
            
            else:
                with open('password.txt', 'wb') as f:
                    f.write(data)


charset = string.ascii_lowercase + string.digits
unlock_zip('chapter_2/prob1/emergency_storage_key.zip','password.txt', charset, 6)
