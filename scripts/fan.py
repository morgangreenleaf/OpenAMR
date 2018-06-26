import RPi.GPIO as GPIO #include a library that tells the interpreter how to work with Raspberry pis GPIO pins
import time
import tkinter as tk
from tkinter import *
import smbus
GPIO.setwarnings(False)

LedPin = 11; #GPIO pin 11

bus = smbus.SMBus(1)
bus.write_byte(0x40, 0xF5)
 
time.sleep(0.3)
 
# SI7021 address, 0x40  Read 2 bytes, Humidity
data0 = bus.read_byte(0x40)
data1 = bus.read_byte(0x40)
   
# Convert the data
humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
   
time.sleep(0.3)
bus.write_byte(0x40, 0xF3)
time.sleep(0.3)
   
# SI7021 address, 0x40 Read data 2 bytes, Temperature
data0 = bus.read_byte(0x40)
data1 = bus.read_byte(0x40)
   
# Convert the data and output it
celsTemp = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
fahrTemp = celsTemp * 1.8 + 32

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
      
def turnDcMotorOn():  #A function to turn the dc motor on
    while True:
        GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to turn on led
        

def turnDcMotorOff():  #A functionn to turn the dc motor off
    GPIO.output(LedPin,GPIO.LOW) #Turn the GPIO pin 11 off
    GPIO.cleanup();
    
def createWindow():
    setup()
    root = tk.Tk(className = "Fan")
    root.config(bg = 'lightblue')
    
    frame1 = tk.LabelFrame(root)
    frame2 = tk.Frame(root)
    frame3 = tk.Frame(root)
    
    label = tk.Label(frame2, text = 'Tempearture: ', width=30, fg = 'blue')
    label2 = tk.Label(frame2, text = celsTemp, width=30)
    
    
    #tempButton = tk.Button(frame1, text = 'diplay Temp & Humidity', bg = 'green')
    #heatButton = tk.Button(frame1, text = 'turnOnHeater', bg = 'green', command = startSystem)
    offheatButton = tk.Button(frame1, text = 'turnOffFan', bg = 'green', width = 20, command = turnDcMotorOff)
    
    label.pack(side = 'left')
    label2.pack(side = 'left')
    frame1.pack(side = 'bottom', padx=20,pady=400)
    frame2.pack(side = 'bottom', padx=50)
    frame3.pack(side = 'bottom')
    
   
    #tempButton.pack(side = 'left',padx=20,pady=30)
    #heatButton.pack(side = 'left',padx=20,pady=30)
    offheatButton.pack(side = 'left',padx=20,pady=30)
    root.mainloop()
    
    if (celsTemp < 25) :
            turnDcMotorOn()
if __name__ == '__main__':
    createWindow()
    
    '''try:
        turnDcMotorOn()
        time.sleep(100)
        turnDcMotorOff()
    except KeyboardInterrupt:
        print("true")
        turnDcMotorOff()'''