import RPi.GPIO as GPIO
from gpiozero import Buzzer
from time import sleep
import tkinter as tk
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
def checkDoor():
    buzzer = Buzzer(17)

    GPIO.setup(27,GPIO.IN)

    input = GPIO.input(27)

    while True:
        if (GPIO.input(27)):
            print("Door Opened")
            buzzer.on()
            sleep(1)
            buzzer.off()
            sleep(1)
def createWindow():
    root = tk.Tk(className = "Door Sensor")
    root.config(bg = 'lightblue')
    
    frame1 = tk.LabelFrame(root)
    frame2 = tk.Frame(root)
    frame3 = tk.Frame(root)
    
    label = tk.Label(frame1, text = 'waiting for an event ', width=30, fg = 'blue')    
    backButton = tk.Button(frame3, text = 'Back', bg = 'green', width = 10) 
    
    label.pack(side = 'left')
   
    frame1.pack(side = 'bottom', padx=20,pady=400)
    frame2.pack(side = 'bottom', padx=50)
    frame3.pack(side = 'bottom')
    
    backButton.pack(side = 'right')
    
    root.mainloop()                             
if __name__=='__main__':
    createWindow()
    
