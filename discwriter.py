import cv2
import numpy as np
import os.path
import math
import copy
from scipy import stats
import numpy as np
from scipy import signal
import pickle

def discwriter(discs, descriptors, filepath):
    # cnx = mysql.connector.connect(user='root', database='incubator', password = 'Letmein!')
    # connect to database
    #The ids, dosages, and content inputs are only necassary if there is nothing in the database for something.
    #they are arrays that correspond to the discs, i.e. dosages[0] is the dosages for disc[1], etc.
    cursor = dbh.cursor()
    cursor.execute("select abx_name from antibiotics")
    # get names
    discnames = cursor.fetchall()
    cursor.execute("select abx_descriptor from antibiotics")
    # get descriptors
    knownfeatures = cursor.fetchall()

    cursor.execute("select abx_id from antibiotics")
    ids = cursor.fetchall()

    existance = np.zeros(len(discs), np.uint8)
    head, tail = os.path.split(filepath)
    # makes sure all discs are known
    for d in range(0, len(discs)):
        for n in range(0, len(discnames)):
            if (discs[d + 1] == discnames[n]):
                if (knownfeatures[n] != ''):
                    # if a discs name matches one found in the database
                    features = open(knownfeatures[n][0], "wb")
                    pairdisc = pickle.load(features)
                    # access its descriptors
                    pairdisc[len(pairdisc)] = descriptors[d]
                    # open the dictionary and add the new descriptor to it at len(descriptors) since it starts at zero
                    features.close()
                    # close it
                    features = open(knownfeatures[n][0], "wb")
                    # dump it at the same point
                    pickle.dump(pairdisc, features)
                    features.close()
                    existance[d] = 1
                else:
                    entirepath = ''
                    if (len(filepath) > 0):
                        entirepath = head + '/' + discs[d + 1] + '.pkl'
                    # make a file at a given folder
                    else:
                        entirepath = discs[d + 1] + '.pkl'
                    tempdict = {}
                    features = open(entirepath, "wb")
                    tempdict[0] = descriptors[d + 1]
                    # make a new dictionary and dump it in that file
                    pickle.dump(tempdict, features)
                    features.close()
                    cursor.execute("update antibiotics set abx_descriptor = " + entirepath + "where abx_id = " str(abx_id[n]))

