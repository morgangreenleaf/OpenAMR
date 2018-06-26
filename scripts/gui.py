import tkinter as tk
from tkinter import*
#def Ask_Mode_Option():


root=tk.Tk(className='Main Menu')
#mode=tk.IntVar()
#mode.set(6)
                # 0 for Client Mode
                # 1 For Server Mode
'''def out():
    root.destroy()
    return
def mode_set(value):
    mode.set(value)
    out()
    return'''
#list of images
image1 = PhotoImage(file = 'pictures/stepper.png')
image2 = PhotoImage(file = 'pictures/camera.png')
image3 = PhotoImage(file = 'pictures/fan.png')
image4 = PhotoImage(file = 'pictures/temperature.png')
image5 = PhotoImage(file = 'pictures/help.png')
image6 = PhotoImage(file = 'pictures/sensor.png')
#image7 = PhotoImage(file = 'pictures/cover.png')

#label = tk.Label(root, width = 700, height = 400, image = image7)
#label.pack()
frame =tk.LabelFrame(root, width = 450, height = 200)
label = tk.Label(root, text = 'Daeyang Third Year Students')


frame1 =tk.Frame(frame, width = 100, height = 50)
motorButton = tk.Button(frame1,text = 'Motor', image = image1, relief = 'flat', command=lambda: steppermotor.createWindow())
camButton2 = tk.Button(frame1, text = 'Camera', image = image2, relief = 'flat', command=lambda: timestamp.createWindow())
fanButton3 = tk.Button(frame1, text = 'Fan', image = image3, relief = 'flat', command=lambda: fan.createWindow())

#packing into the main Window
frame.pack(padx=20,pady=100)
label.pack()
motorButton.pack(side = 'left', padx=20,pady=30)
camButton2.pack(side = 'left', padx=20,pady=30)
fanButton3.pack(side = 'left', padx=20,pady=30)

#second frame and Buttons
frame2 = tk.Frame(frame, width = 100, height = 50)
Button4 = tk.Button(frame2, text = 'Temperature & Heat', image = image4, relief = 'flat', command=lambda: temperature .createWindow())
Button5 = tk.Button(frame2, text = 'Door sensor', image = image6, relief = 'flat')


#packing into the main window
frame1.pack()
frame2.pack()
Button4.pack(side = 'left', padx=20,pady=30)
Button5.pack(side = 'left', padx=20,pady=30)

root.mainloop()
#return mode.get()



