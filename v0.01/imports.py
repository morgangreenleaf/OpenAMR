from tkinter import *
from tkinter import ttk as cal
import pymysql
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
import numpy as np
from scipy import signal
import pickle
import threading

dbh = pymysql.connect(host="localhost", password="", user="root", db="incubator")


'''
                                isolate_identification={}
                                for isokey,isolates in abx_result_dictionary:
                                    isolate_identification[isokey] = cal.Label(pocket_frame,  text="Disc " + str(1) + "." + isolates[isokey])
                                    isolate_identification[isokey].pack(anchor='w')
                                    isolate_identification[isokey].bind("<Button-1>", lambda value: isolate_selectedToChange(isolate_identification[isokey], isokey))


 a
'''