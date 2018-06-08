from picamera import PiCamera,color
import time

camera = PiCamera()

    
#picture with colourSwap effect    
def colorSwap(effect, count):
    camera.start_preview()
    camera.image_effect = effect
    for i in range(count):
        time.sleep(1)
        camera.capture('/home/pi/Desktop/Phillip/Pictures/image%s.jpg' % i)
        time.sleep(1)
    camera.stop_preview()
    
    
if __name__ == '__main__':
    colorSwap("none", 4)
    
