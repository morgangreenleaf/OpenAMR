import RPi.GPIO as GPIO
import time
import tkinter as tk

GPIO.setmode(GPIO.BOARD)


def clockWiseRevolution():
    
    ControlPin = [13,15,19,21]

    for pin in ControlPin:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)
    step_seq_num=0
    rot_spd=0.001
    rotate=4096
    rotate_dir=1
    rotateF = 1
    seq=[[1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]]

    #rotateF=float (input("Enter revolutions(0.00041 +):"))
    #rotate_dir = input("Enter direction (1CW/-1CCW):")
    #rot_spd = input("Enter speed (1-0.001):")
    rotate = int(rotateF * 4096)
    if rotate < 1:
        rotate = 4096
    rotate_dir=int(rotate_dir)
    if rotate_dir != 1 and rotate_dir != -1:
        rotate_dir = 1
    rot_spd = float(rot_spd)
    if rot_spd > 1 or rot_spd < 0.001:
        rot_spd = 0.001
    print (rotate, rotate_dir, rot_spd)

    for i in range(0, (rotate+1)):
        for pin in range(0,3):
            Pattern_Pin = ControlPin[pin]
            if seq[step_seq_num][pin] == 1:
                GPIO.output(Pattern_Pin, True)
            else:
                GPIO.output(Pattern_Pin, False)
        step_seq_num += rotate_dir
        if (step_seq_num >= 8):
            step_seq_num = 0
        elif step_seq_num < 0:
            step_seq_num = 7

        time.sleep(rot_spd)
    GPIO.cleanup()
    
def antiClockWiseRevolution():
    
    ControlPin = [13,15,19,21]

    for pin in ControlPin:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)
    step_seq_num=0
    rot_spd=0.001
    rotate=4096
    rotate_dir=-1
    rotateF = 1
    seq=[[1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]]

    #rotateF=float (input("Enter revolutions(0.00041 +):"))
    #rotate_dir = input("Enter direction (1CW/-1CCW):")
    #rot_spd = input("Enter speed (1-0.001):")
    rotate = int(rotateF * 4096)
    if rotate < 1:
        rotate = 4096
    rotate_dir=int(rotate_dir)
    if rotate_dir != 1 and rotate_dir != -1:
        rotate_dir = 1
    rot_spd = float(rot_spd)
    if rot_spd > 1 or rot_spd < 0.001:
        rot_spd = 0.001
    print (rotate, rotate_dir, rot_spd)

    for i in range(0, (rotate+1)):
        for pin in range(0,3):
            Pattern_Pin = ControlPin[pin]
            if seq[step_seq_num][pin] == 1:
                GPIO.output(Pattern_Pin, True)
            else:
                GPIO.output(Pattern_Pin, False)
        step_seq_num += rotate_dir
        if (step_seq_num >= 8):
            step_seq_num = 0
        elif step_seq_num < 0:
            step_seq_num = 7

        time.sleep(rot_spd)
    GPIO.cleanup()
        
    
def createWindow():

    root = tk.Tk(className = "Stepper Mortor")
    root.config(bg = 'lightblue')
    
    frame1 = tk.LabelFrame(root)
    frame2 = tk.Frame(root, width = 400)
    frame3 = tk.Frame(root)
    
    label = tk.Label(frame2, text = 'press the Buttons to move the motor ', width=30, fg = 'blue')
    #label2 = tk.Label(frame2, text = celsTemp, width=30)
    
    
    #tempButton = tk.Button(frame1, text = 'diplay Temp & Humidity', bg = 'green')
    heatButton = tk.Button(frame1, text = 'CW Direction', bg = 'green', width = 20, command =clockWiseRevolution )
    offheatButton = tk.Button(frame1, text = 'CCW Direction', bg = 'green', width = 20, command = antiClockWiseRevolution)
    
    label.pack(side = 'left')
    #label2.pack(side = 'left')
    frame1.pack(side = 'bottom', padx=20,pady=400)
    frame2.pack(side = 'bottom', padx=50)
    frame3.pack(side = 'bottom')
    
    
    #tempButton.pack(side = 'left',padx=20,pady=30)
    heatButton.pack(side = 'left',padx=20,pady=30)
    offheatButton.pack(side = 'left',padx=20,pady=30)
    root.mainloop()
if __name__ == '__main__':
    
    createWindow()