import os
import zipfile
import glob
import cv2
import os
from pathlib import Path


class MasImageHelper:
    def __init__(self):
        self.all_image_files = []

    def get_image_lists(self):
        p = Path('./cctv')
        extensions = ['*.jpg', '*.png', '*.gif', '*.webp', '*.jpeg']
        for ext in extensions:
            self.all_image_files.extend(sorted(p.glob(ext)))

    def show_images(self):
        idx = 0
        window_title = 'Image Viewer : press "esc" to end program'

        while True:
            img = cv2.imread(self.all_image_files[idx])

            cv2.imshow(window_title, img)
            key = cv2.waitKeyEx(0)

            if key == 27:
                print('프로그램을 종료합니다.')
                break

            # 왼쪽 방향키
            elif key == 2424832:
                idx -= 1
                if idx < 0:
                    idx = len(self.all_image_files) - 1

            # 오른쪽 방향키
            elif key == 2555904:
                idx += 1
                if idx >= len(self.all_image_files):
                    idx = 0

        cv2.destroyAllWindows()


if __name__ == '__main__':
    if not os.path.exists('./cctv'):
        with zipfile.ZipFile('./cctv.zip', 'r') as zf:
            zf.extractall('./cctv')
            print("압축 풀기 완료.")

        mih = MasImageHelper()
        mih.get_image_lists()
        mih.show_images()

