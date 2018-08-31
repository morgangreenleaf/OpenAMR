from tkinter import *
from tkinter import ttk as cal

import pymysql

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
import numpy as np
from scipy import signal

import pickle
import threading

try:
    dbh = pymysql.connect(host="localhost", password="", user="root", db="incubator")
    dbhzonefinder = pymysql.connect(host="localhost", password="", user="root", db="incubator")
    dbhnotify = pymysql.connect(host="localhost", password="", user="root", db="incubator")
    #=======================================================================================
    #dbh = pymysql.connect(host="localhost", password="0000", user="root", db="incubator")
    #dbhzonefinder = pymysql.connect(host="localhost", password="0000", user="root", db="incubator")
    #=======================================================================================

except:
    print("Server offline")

