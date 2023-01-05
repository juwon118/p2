import RPi.GPIO as GPIO                 
import time           
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model


GPIO.setmode(GPIO.BCM)               
GPIO.setup(17, GPIO.OUT)                   # Trig=17 
GPIO.setup(18, GPIO.IN)                    # Echo=18 
GPIO.setwarnings(False) 

GPIO.setup(24, GPIO.OUT) 
p = GPIO.PWM(24, 440) 
p.start(50)


def img_preprocess(image) : 
    height, __, __ = image.shape
    image = image[int(height/2):, :, :]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image = cv2.resize(image, (200, 66))
    image = cv2.GaussianBlur(image, (5, 5), 0)
    
    __, image = cv2.threshold(image, 97, 255, cv2.THRESH_BINARY)
    image = image / 255 
    return image

camera = cv2.VideoCapture(-1)
camera.set(3, 640)
camera.set(4, 480)

def main() :
    model_path = '/home/pi/aaa/model/lane_navigation_final.h5' 
    model = load_model(model_path) 
    State = 'stop'
    try:
        while True:
            
            keyValue = cv2.waitKey(1)
            if keyValue == ord('q') :
                break
            elif keyValue == 82 : #45
                print('x') 
                State = 'x'

            elif keyValue == 83 : #135
                print('o') 
                State = 'o' 
        
            __, image = camera.read()
            cv2.imshow('Orig.', image)
            preprocessed = img_preprocess(image) # 보정한 이미지 저장
            cv2.imshow('pre', preprocessed) # 보정한 이미지 보여주기
            X = np.asarray([preprocessed]) # X값 형식에 맞게 데이터 삽입
            steering_angle = int(model.predict(X)[0]) # 각도 예측
            print('predict_angle: ', steering_angle) # 예측 각도 출력
            if steering_angle <= 70:
                print('x') 

            elif steering_angle > 70:
                print('o')
                for dc in range(500, 601, 5) :       #싸이렌소리
                    print('start_1, freq.=', dc)
                    p.ChangeFrequency(dc)
                    time.sleep(0.1)
                for dc in range(600, 499, -5) : 
                    p.ChangeFrequency(dc)
                    print('start_2, freq.=', dc)
                    time.sleep(0.1)
            GPIO.output(17, False)         
            time.sleep(0.5)

            GPIO.output(17, True)         
            time.sleep(0.00001)            
            GPIO.output(17, False)         

            while GPIO.input(18) == 0:     #시작시간 측정
                start = time.time()

            while GPIO.input(18) == 1:     #도착시간 측정
                stop = time.time()

            time_interval = stop - start     
            distance = time_interval * 17000
            distance = round(distance, 2)
            print ("Distance => ", distance, "cm")
            if distance < 10 :
                for dc in range(590, 601, 5) :       #싸이렌소리
                    print('start_1, freq.=', dc)
                    p.ChangeFrequency(dc)
                    time.sleep(0.1)
                for dc in range(600, 589, -5) : 
                    p.ChangeFrequency(dc)
                    print('start_2, freq.=', dc)
                    time.sleep(0.1)
                for dc in range(590, 601, 5) :       #싸이렌소리
                    print('start_1, freq.=', dc)
                    p.ChangeFrequency(dc)
                    time.sleep(0.1)
                for dc in range(600, 589, -5) : 
                    p.ChangeFrequency(dc)
                    print('start_2, freq.=', dc)
                    time.sleep(0.1)
            
            print ("Distance => ", distance, "cm")
    except KeyboardInterrupt:                 
        GPIO.cleanup()
            

if __name__ == '__main__':
    main()


