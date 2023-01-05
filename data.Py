import cv2
import time
#import Servo
#Ctrl = Servo.Servo()
#Ctrl.Servo(1, 90)
#Ctrl.Servo(2, 100)
camera = cv2.VideoCapture(-1)
camera.set(3, 640)
camera.set(4, 480)
def main() :
    filepath = '/home/pi/aaa/video/train'
    i = 0
    State = 'stop'
    try :
        while (camera.isOpened()) :
            keyValue = cv2.waitKey(1)
            if keyValue == ord('q') :
                break
            elif keyValue == 82 : # X dkv
                print('X')
                State = 'x'
                

            elif keyValue == 83 : # III >
                print('o')
                State = 'o'

            __, image = camera.read()
            height, __, __ = image.shape
            image = image[int(height / 2) : , : , : ]
            image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV) #
            image = cv2.resize(image, (200, 66))
            image = cv2.GaussianBlur(image, (5, 5), 0)
            __, image = cv2.threshold(image, 97, 255, cv2.THRESH_BINARY) #cv2.THRESH_BINARY_INV (65를 수치바꾸며테스트)

            if State == 'x': #x
                cv2.imwrite('%s_%05d_%03d.png' % (filepath, i, 45), image)
                i += 1
            elif State == 'o' : #III
                cv2.imwrite('%s_%05d_%03d.png' % (filepath, i, 135), image)
                i += 1

            cv2.imshow('Org.', image)

    except KeyboardInterrupt :
        pass
if __name__ == '__main__' :
    main()
    cv2.destroyAllWindows()
