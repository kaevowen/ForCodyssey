import zipfile
import cv2
import os
from pathlib import Path
import numpy as np


class MasImageHelper:
    def __init__(self):
        self.all_image_files = []
        print("Loading YOLOv4-tiny model...")
        self.net = cv2.dnn.readNet("yolov4-p6.weights", "yolov4-p6.cfg")
        self.classes = []
        with open("coco.names", "r") as f:
            self.classes = [line.strip() for line in f.readlines()]

        # GPU를 사용하도록 설정 (사용 가능한 경우)
        # self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        # self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        layer_names = self.net.getLayerNames()
        # 최종 출력 레이어의 이름을 가져옴
        self.output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def get_image_lists(self):
        """CCTV 폴더에서 이미지 파일 목록을 가져옵니다."""
        if not os.path.exists('./cctv'):
            with zipfile.ZipFile('./cctv.zip', 'r') as zf:
                zf.extractall('./cctv')
                print("압축 풀기 완료.")

        p = Path('./cctv')
        extensions = ['*.jpg', '*.png', '*.gif', '*.webp', '*.jpeg']
        temp_files = []
        for ext in extensions:
            temp_files.extend(p.glob(ext))

        self.all_image_files = sorted([str(f) for f in temp_files])

        if not self.all_image_files:
            print("cctv 폴더에 이미지 파일이 없습니다.")
            return False
        return True

    def search_person_yolo(self):
        """YOLO를 이용해 사람을 찾고, 찾으면 출력 후 대기합니다."""
        if not self.all_image_files:
            return

        CONFIDENCE_THRESHOLD = 0.1 # 신뢰도 임계값 (낮출수록 많이 찾음)
        NMS_THRESHOLD = 0.3  # NMS 임계값 (높일수록 겹친 대상을 덜 제거함)
        print("YOLO 사람 탐색을 시작합니다...")

        for img_path in self.all_image_files:
            img = cv2.imread(img_path)
            if img is None:
                continue

            height, width, channels = img.shape

            # 2. 이미지를 YOLO가 처리할 수 있는 blob 형태로 변환
            blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (1280, 1280), swapRB=True, crop=False)
            # blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)

            class_ids = []
            confidences = []
            boxes = []

            # 3. 탐지 결과 분석
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    # 'person' 클래스이고, 신뢰도가 50% 이상인 것만
                    if self.classes[class_id] == "person" and confidence > CONFIDENCE_THRESHOLD:
                        # bounding box 좌표 계산
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            # 4. 노이즈 제거 (가장 신뢰도 높은 박스만 남김)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)

            # 5. 사람이 한 명이라도 찾아졌다면 화면에 표시
            if len(indexes) > 0:
                print(f"'{os.path.basename(img_path)}'에서 사람을 {len(indexes)}명 찾았습니다! (엔터: 계속, ESC: 종료)")
                font = cv2.FONT_HERSHEY_PLAIN
                for i in indexes.flatten():
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    confidence_text = f"{confidences[i]:.2f}"
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(img, label + " " + confidence_text, (x, y + 20), font, 2, (255, 255, 255), 2)

                cv2.imshow("Person Detected (YOLO)", img)
                key = cv2.waitKey(0)

                if key == 13:  # Enter
                    continue
                elif key == 27:  # ESC
                    print("사용자가 프로그램을 종료했습니다.")
                    cv2.destroyAllWindows()
                    return

        print("\n모든 이미지 검색이 끝났습니다.")
        cv2.destroyAllWindows()


# --- 메인 실행 부분 ---
if __name__ == "__main__":
    mih = MasImageHelper()
    if mih.get_image_lists():
        mih.search_person_yolo()