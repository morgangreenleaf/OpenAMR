from scripts import gui,steppermotor, fan, temperature, doorSensor, timestamp
#/home/pi/Desktop/pythonGroupProject

if __name__ == '__main__':
    storeobj=gui.Ask_Mode_Option()
    if storeobj==1:
        steppermotor.createWindow().mainloop()
        root.destroy()
        pass
    elif storeobj==1:
        fan.createWindow().mainloop()
    elif storeobj==2:
        temperature.createWindow().mainloop()
    elif storeobj==3:
        timestamp.createWindow().mainloop()
    elif storeobj==4:
        doorSensor.createWindow().mainloop()
    #elif storeobj==5:
        
    else:
        pass
