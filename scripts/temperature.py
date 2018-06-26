import tkinter as tk
from tkinter import *
import smbus
import time
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)




# TEMPERATURE CODE
#def temperature():
# Get I2C bus
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

'''print ("Relative Humidity is : %.2f %%" %humidity)
print ("Temperature in Celsius is : %.2f C" %celsTemp)
print ("Temperature in Fahrenheit is : %.2f F" %fahrTemp)'''


    
# HEATER CODES

#def heater():

LedPin = 23    # pin11

def setup():
  GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
  GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
  GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to turn on led
  

def heater_on():
  while True:
    GPIO.output(LedPin, GPIO.HIGH)  # led on
    #time.sleep(1)
    #GPIO.output(LedPin, GPIO.LOW) # led off
    #time.sleep(1)

def heater_off():
  GPIO.output(LedPin, GPIO.LOW)   # led off
  GPIO.cleanup()                  # Release resource

def turnOffHeatetSystem():
    '''setup()
    try:
        if (celsTemp < 30) :
            heater_on()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.'''
    heater_off()
def createWindow():
    setup()
    root = tk.Tk(className = "Temperature and Humidity sensor")
    root.config(bg = 'lightblue')
    
    frame1 = tk.LabelFrame(root)
    frame2 = tk.Frame(root)
    frame3 = tk.Frame(root)
    
    label = tk.Label(frame2, text = 'Tempearture: ', width=30, fg = 'blue')
    label2 = tk.Label(frame2, text = celsTemp, width=30)
    label3 = tk.Label(frame3, text = 'Humidity: ', width=30, fg = 'blue')
    label4 = tk.Label(frame3, text = humidity, width=30)
    
    backButton = tk.Button(root, text = 'Back', bg = 'green', width = 10) 
    #tempButton = tk.Button(frame1, text = 'diplay Temp & Humidity', bg = 'green')
    #heatButton = tk.Button(frame1, text = 'turnOnHeater', bg = 'green', command = startSystem)
    offheatButton = tk.Button(frame1, text = 'turnoffHeater', bg = 'green', width = 20, command = turnOffHeatetSystem)
    
    label.pack(side = 'left')
    label2.pack(side = 'left')
    label3.pack(side = 'left')
    label4.pack(side = 'left')
    frame1.pack(side = 'bottom', padx=20,pady=400)
    frame2.pack(side = 'bottom', padx=50)
    frame3.pack(side = 'bottom')
    
    backButton.pack(side = 'right')
    #tempButton.pack(side = 'left',padx=20,pady=30)
    #heatButton.pack(side = 'left',padx=20,pady=30)
    offheatButton.pack(side = 'left',padx=20,pady=30)
    
    root.mainloop()
    if (celsTemp < 25) :
            heater_on()
    
if __name__ == '__main__':     # Program start from here
     
     createWindow()
     
     



   
