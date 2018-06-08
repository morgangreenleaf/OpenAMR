from picamera import PiCamera,color
import time

camera = PiCamera()

#taking 3 pix after every sec
def threePix():
    camera.start_preview()
    for i in range(3):
        time.sleep(1)
        camera.capture('/home/pi/Desktop/Phillip/Pictures/image%s.jpg' % i)
        time.sleep(1)
    colorSwap()
        
    camera.stop_preview()
    
#picture with colourSwap effect    
def colorSwap():
    camera.start_preview()
    camera.image_effect = 'colorswap'
    time.sleep(2)
    camera.capture('/home/pi/Desktop/Phillip/Pictures/colorswap.jpg')
    camera.stop_preview()
    
    
if __name__ == '__main__':
    threePix()
    
