def caesar_cipher_decode(target_text):
    caesar_list = []
    
    for i in range(1, 26):
        tmp = ''
        print(f"[{i}]: ", end='')
        for t in target_text:
            if t.isspace():
                tmp += t
                print(' ', end='')
            elif t.islower():
                tmp += chr((ord(t) - ord('a') + i) % 26 + ord('a'))
                print(chr((ord(t) - ord('a') + i) % 26 + ord('a')), end='')
            elif t.isupper():
                tmp += chr((ord(t) - ord('A') + i) % 26 + ord('A'))
                print(chr((ord(t) - ord('A') + i) % 26 + ord('A')), end='')
            else:
                tmp += t
                print(t, end='')
        
        caesar_list.append(tmp)
        print()

    idx = int(input('select list : '))
    return caesar_list[idx-1]


with open('chapter_2/prob2/password.txt', 'r') as file:
    decode_text = caesar_cipher_decode(file.read())
    with open('chapter_2/prob2/result.txt', 'w') as result:
        result.write(decode_text)