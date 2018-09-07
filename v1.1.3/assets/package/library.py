try:
    from tkinter import *
    from tkinter import ttk as cal
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


    #========= Database =========
    hostname = "localhost"
    dbpassword = ""
    dbuser = "root"
    dbname = "incubator"
    #==========================

    try:
        dbh = pymysql.connect(host=hostname, password=dbpassword, user=dbuser, db=dbname)
        dbhzonefinder = pymysql.connect(host=hostname, password=dbpassword, user=dbuser, db=dbname)
        dbhnotify = pymysql.connect(host=hostname, password=dbpassword, user=dbuser, db=dbname)

    except:
        try:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast("Server Connection Error",
                               "Can't connect to server, Make sure the server is turned on and credentals are correct.",
                               icon_path=None,
                               duration=5,
                               threaded=True)
            exit()
        except:
            print("Access denied, invalid credentials, ERR: Raised from database, Check database Connection")
            exit()
except Exception as ex:
    print("ERROR_IMPORT")
    print(ex)
    exit()
