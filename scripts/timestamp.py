caimport picamera
from subprocess import call
from datetime import datetime
from time import sleep
from picamera import PiCamera,color
import tkinter as tk

def startCamera():
    # Our file path
    filePath = "/home/pi/Desktop/Phillip/timestamped_pics/"
    #picTotal = 5
    #picCount = 0
    a = ["colorswap","none","negative","sketch"] 
    for o in range(len(a)):

        # Grab the current time
        currentTime = datetime.now()
        # Create file name for our picture
        picTime = currentTime.strftime("%Y.%m.%d-%H%M%S")
        picName = picTime + '.jpg'
        completeFilePath = filePath + picName

        # Take picture using new filepath
        with picamera.PiCamera() as camera:
            camera.start_preview()
            camera.resolution = (1280,720)
            camera.image_effect = a[o]
            sleep(1)
            camera.capture(completeFilePath)
            camera.stop_preview()
            print("We have taken a picture.")

        # Create our stamp variable
        timestampMessage = currentTime.strftime("%Y.%m.%d - %H:%M:%S")
        # Create time stamp command to have executed
        timestampCommand = "/usr/bin/convert " + completeFilePath + " -pointsize 36 \
        -fill red -annotate +700+650 '" + timestampMessage + "' " + completeFilePath
        # Actually execute the command!
        call([timestampCommand], shell=True)
        print("We have timestamped our picture!")

        # Advance our picture counter

        sleep(1)
        
def createWindow():
    root = tk.Tk(className = "Camera")
    root.config(bg = 'lightblue')
    
    frame1 = tk.LabelFrame(root)
    frame2 = tk.Frame(root)
    frame3 = tk.Frame(root)
    
    #label = tk.Label(frame2, text = 'Tempearture: ', width=30, fg = 'blue')
    label2 = tk.Label(frame2, text = 'ready to take pictures', width=30)
    
    backButton = tk.Button(root, text = 'Back', bg = 'green', width = 10) 
    #tempButton = tk.Button(frame1, text = 'diplay Temp & Humidity', bg = 'green')
    #heatButton = tk.Button(frame1, text = 'turnOnHeater', bg = 'green', command = startSystem)
    offheatButton = tk.Button(frame1, text = 'takePictures', bg = 'green', width = 20, command = startCamera)
    
    #label.pack(side = 'left')
    label2.pack(side = 'left')
    frame1.pack(side = 'bottom', padx=20,pady=400)
    frame2.pack(side = 'bottom', padx=50)
    frame3.pack(side = 'bottom')
    
    backButton.pack(side = 'right')
    #tempButton.pack(side = 'left',padx=20,pady=30)
    #heatButton.pack(side = 'left',padx=20,pady=30)
    offheatButton.pack(side = 'left',padx=20,pady=30)
    root.mainloop()
    
if __name__ == '__main__':
    createWindow()
    
