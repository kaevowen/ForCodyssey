import json
from datetime import datetime
import wave
import pyaudio
import keyboard
import os
import whisper
import glob
import csv


def record_audio():
    FILE_PATH = './records'
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    os.makedirs(FILE_PATH, exist_ok=True)

    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = f'{current_time}.wav'
    file_path = os.path.join(FILE_PATH, file_name)

    p = pyaudio.PyAudio()
    print("mic opened. if you wanna stop press q")

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        if keyboard.is_pressed('q'):
            print('record stop')
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print("녹음파일이 저장되었습니다. 위치 : ./records/")


def speech_to_text():
    print('음성 파일을 텍스트로 변환합니다.')
    model = whisper.load_model('small')
    file_list = glob.glob('./records/*.wav')
    print(f'wav file list : {file_list}')

    for file in file_list:
        print(file)
        result = model.transcribe(file)
        csv_path = os.path.splitext(file)[0]+'.csv'
        with open(csv_path, "w", newline='', encoding='euc-kr') as f:
            writer = csv.writer(f)
            writer.writerow(['시간', '텍스트'])
            for segment in result['segments']:
                start = segment['start']
                end = segment['end']
                text = segment['text'].strip()
                writer.writerow([f'{start:.2f}-{end:.2f}', text])

        print('CSV 저장 완료:', csv_path)
record_audio()
# speech_to_text()