try:
    from tkinter import *
    from tkinter import ttk as cal
    from tkinter.font import nametofont
    from PIL import Image
    from PIL import ImageTk
    import datetime
    import random
    import os
    import time
    import shutil
    import cv2
    import numpy as np
    import os.path
    import math
    import copy
    from scipy import stats
    from scipy import signal
    import pickle
    import threading
    import pymysql

    #Globals
    imgpath = coordinates = images = masks = antiobioticsDis = imageFilename = abxname = None
    imagedis = isolatename = imageScale = topLevelWin = uniquecode = generalOpt = None

    newImageFile = arrayDistances = discs = myflag = iflag = valHolder = None

    imagefx = imagefxs = generals = None
    showIm = None


    #========= Database =========
    hostname = "localhost"
    dbpassword = ""
    dbuser = "root"
    dbname = "incubator"
    #==========================

    try:
        dbh = pymysql.connect(host=hostname, password=dbpassword, user=dbuser, db=dbname)
        dbhBG = pymysql.connect(host=hostname, password=dbpassword, user=dbuser, db=dbname)
        dbhzonefinder = pymysql.connect(host=hostname, password=dbpassword, user=dbuser, db=dbname)
        dbhnotify = pymysql.connect(host=hostname, password=dbpassword, user=dbuser, db=dbname)

        # Database Cursor Global
        getCursor = dbh.cursor()

    except:
        print("Access denied, invalid credentials, ERR: Raised from database, Check database Connection")
        exit()
except Exception as ex:
    print("ERROR_IMPORT")
    print(ex)
    exit()
