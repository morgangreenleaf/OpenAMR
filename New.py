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
    dbh = pymysql.connect(host="localhost", password="0000", user="root", db="incubator")
except:
    print("Server offline")






def zonefinder(filepath):
    # This file takes a file path for a petri dish and finds the Zones of inhibition for that dish, and draws them
    # It writes an image to the disc of the petri dish with zones drawns in the same location as the input image, but with zonesfound before the original image name
    # It returns the filepath to this new image, as well as an array of diameters that correspond to the image, i.e. actualdists[0] gives the diameter
    # of the zone of inhibition to disc 1 on the image, actualdiscs[1] gives disc 2, etc.

    # Import these libraries
    # import cv2
    # import numpy as np
    # import os.path
    # import math
    # import copy
    # from scipy import stats
    # FYI ZOE(s) = Zone of Inhibition(s)

    # Take an input image and do pre-processing
    global shrunkimg
    wordup = filepath
    img = cv2.imread(wordup)
    imgblur = cv2.GaussianBlur(img, (15, 15), 0)
    imggray = cv2.cvtColor(imgblur, cv2.COLOR_BGR2GRAY)
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # The image has to be split into hsv channels to get the value of all the pixels
    imgbgr = cv2.cvtColor(imghsv, cv2.COLOR_HSV2BGR)
    # turn it to B/W and blur it to eliminate noise


    hue, sat, val = cv2.split(imghsv)
    width, height = img.shape[:2]
    dishblank = np.zeros((width, height, 3), np.uint8)
    # image made for the isolated dish
    pxtomm = 0.0307692
    mmtopx = 1 / pxtomm
    # conversionfactor

    retrival, dishimg = cv2.threshold(imggray, np.mean(val) - (np.std(val)), 255, cv2.THRESH_BINARY)
    # The mean value of all the pixels + the standard deviation is used to determine the usual threshold optimal for finding discs on a dish
    # Mean value minus standard deviation is ideal for finding the plate, the edges of the plate must be found
    # , as they often interfere with the zone of inhibition; more elaboration later o
    # Finds the contours of the discs
    im2, dishape, hierarch = cv2.findContours(dishimg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Finds the contour of the petri dish


    # Arrays made to store information about the discs, as they are the central feature used to find ZOEs
    maxarea = dishape[0]
    M = cv2.moments(dishape[0])
    if M["m00"] == 0:
        M["m00"] = 1
    cdX = int(M["m10"] / M["m00"])
    cdY = int(M["m01"] / M["m00"])
    dishrad = math.sqrt(cv2.contourArea(dishape[0]) / math.pi)
    # Setting defaults about the petri dish


    # The array to be used to store the contour that represents the petri dish
    for d in dishape:

        M = cv2.moments(d)

        if cv2.contourArea(maxarea) < cv2.contourArea(d):
            maxarea = d
            cdX = int(M["m10"] / M["m00"])
            cdY = int(M["m01"] / M["m00"])
            dishrad = math.sqrt(cv2.contourArea(d) / math.pi)

    cv2.circle(dishblank, (int(cdX), int(cdY)), int(dishrad), (255, 255, 255), 1)
    # Makes an image with the petri dish in white and everything else in black. Useful later to make sure the program doesn't take the dish into account
    # when finding zones


    v = 0
    discs = {}
    index = []
    imgclean = cv2.imread(wordup)
    # V represents the discs
    # discs is a dictionary to store the discs' location in the image
    # imgclean is a new img to work with

    for x in range(0, 256):
        retval3, threshphoto = cv2.threshold(imggray, x, 255, cv2.THRESH_BINARY)
        edgephoto, contours, hierarchy = cv2.findContours(threshphoto, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Thresholds and finds the contours of the image given threshold x
        v = 0
        # v is to count discs at a given threshold
        for c in contours:
            # loops through contours to finds any ones that fit the parameter of a disc

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # INFORMATION THAT MAY BE USEFUL TO BE MORE ACCURATE IN FINDING DISCS USE AT YOUR OWN DISCRETION
            # Area = cv2.contourArea(c) * pxtomm
            # circumfrence = cv2.arcLength(c, True)*pxtomm
            # AreaR = math.sqrt(cv2.contourArea(c)/math.pi)*pxtomm
            # CircR = circumfrence/(math.pi*2)
            # diametermm = AreaR*2
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


            M = cv2.moments(c)
            # Establishes a moment, they're like moments in physics gives a snapshot of the image
            # Long story short they help you understand information about the contour
            if (M["m00"] != 0) and (1.2 / 1) > M['mu20'] / M['mu02'] > (1 / 1.2) and 500 < cv2.arcLength(c,
                                                                                                         True) < 800 and 15000 < cv2.contourArea(
                c) < 30000:
                # These checks need to past to find a disc, mu02 and mu20 are moments that describe the standard deviation of the contour in the x and y directions
                # m00 is the moment's size
                # These make sure the disc is the right size, has a circumfrence that seems right given the size, and is circular enough
                v = v + 1
                # counts the number of discs found
        index.append(v)
    # Records the discs found in each threshold, index[x] gives the number of discs found at threshold x



    goodthresh = []
    # best thresh = best threshold number ... kinda self explanatory
    bestthresh = 0
    z = 0
    for y in range(0, len(index)):
        if index[y] > index[bestthresh]:
            bestthresh = y
    for z in range(0, len(index)):
        if index[z] == index[bestthresh]:
            goodthresh.append(z)
    bestthresh = int(np.mean(goodthresh))
    # Searches through the index to find the threshold with the right number of discs, i.e. the one equal to the discnum(inputted by the user)
    # Hope to un-hardcode at some point
    if bestthresh == 0:
        bestthresh = 127
    # Precautionary measure if the discs aren't found 127 is considered a good "default threshold"

    ret3, otsuThresh = cv2.threshold(imggray, bestthresh, 255, cv2.THRESH_BINARY)
    im3, contours, hierarchy = cv2.findContours(otsuThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    v = 0
    # V Serves the same purpose


    for c in contours:

        M = cv2.moments(c)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # INFORMATION THAT MAY BE USEFUL TO BE MORE ACCURATE IN FINDING DISCS USE AT YOUR OWN DISCRETION
        # Area = cv2.contourArea(c) * pxtomm
        # circumfrence = cv2.arcLength(c, True)*pxtomm
        # AreaR = math.sqrt(cv2.contourArea(c)/math.pi)*pxtomm
        # CircR = circumfrence/(math.pi*2)
        # diametermm = AreaR*2
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # Same contour function as before, looks for discs at the threshold that finds the most discs

        if (M["m00"] != 0) and (1.2 / 1) > M['mu20'] / M['mu02'] > (1 / 1.2) and 500 < cv2.arcLength(c,
                                                                                                     True) < 800 and 15000 < cv2.contourArea(
            c) < 30000:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            v = v + 1
            discs[v] = cX, cY
            # This time the discs are recorded in the disc disctionary at their points

    downfactor = 0.1
    Ynew = int(cdY * downfactor)
    Xnew = int(cdX * downfactor)
    Cnew = int(dishrad * downfactor)
    imgdif = cv2.resize(imgblur, (0, 0), fx=downfactor, fy=downfactor)
    height0, width0, channels0 = imgdif.shape
    hdif = 0
    wdif = 0
    # The images taken with the camera are really big, so they need to be shrunk downfactor is the downsampling factor
    # these new variables are to work with this smaller version of the image

    if Ynew - Cnew > 0 and Xnew - Cnew > 0:
        cropimg = imgdif[Ynew - Cnew:Ynew + Cnew, Xnew - Cnew: Xnew + Cnew].copy()
        hdif = Ynew - Cnew
        wdif = Xnew - Cnew
    elif Ynew - Cnew > 0 and Xnew - Cnew < 0:
        cropimg = imgdif[Ynew - Cnew:Ynew + Cnew, 0: Xnew + Cnew].copy()
        hdif = Ynew - Cnew
    elif Ynew - Cnew < 0 and Xnew - Cnew > 0:
        cropimg = imgdif[0:Ynew + Cnew, Xnew - Cnew: Xnew + Cnew].copy()
        wdif = Xnew - Cnew
    else:
        cropimg = imgdif[0:Ynew + Cnew, 0:Xnew + Cnew].copy()
    # Crop image works to isolate the dish, depending on where it is in the original image.
    # this series of elif statements make sure the dish isn't hitting against an edge of the image and crop the image accordingly
    # cropping the image makes the program faster on the pi, and a better image for visualization


    hsvmask = cv2.cvtColor(cropimg, cv2.COLOR_BGR2HSV)
    # labmask = cv2.cvtColor(cropimg, cv2.COLOR_BGR2LAB)
    grayimg = cv2.cvtColor(cropimg, cv2.COLOR_BGR2GRAY)
    height, width, channels = cropimg.shape
    blank_image = np.zeros((height, width, 3), np.uint8)
    smalldish = copy.deepcopy(blank_image)
    # Creating new images based on the small image
    # Others may be useful in the future
    cv2.circle(smalldish, (int(width / 2), int(height / 2)), Cnew - 5, (255, 255, 255), -1)
    # Draws an image with a circle representing the petri dish on a smaller image, using the information of the shape of the petri dish based on the
    # petri dish locater at the beggining of the program



    alldish = np.zeros(shape=(1, 2), dtype=int)
    background = np.zeros(shape=(1, 2), dtype=int)
    # Arrays that represent the points where the petri dish is or isn't

    newdiscs = {}
    for z in range(1, len(discs) + 1):
        newdiscs[z] = (int(discs[z][0] * downfactor) - wdif, int(discs[z][1] * downfactor) - hdif)
        cv2.circle(smalldish, (newdiscs[z]), 10, (0, 0, 0), -1)
    # finds the new locations of the disc on this downsampled image
    # draws them on the dish

    for x in range(0, height):
        for y in range(0, width):
            if smalldish[x][y][0] == 255 and smalldish[x][y][1] == 255 and smalldish[x][y][2] == 255:
                alldish = np.append(alldish, [[x, y]], axis=0)
            else:
                background = np.append(background, [[x, y]], axis=0)
    # Looks through the image with a white dish with black background and records those points in two arrays,
    # If a check happens outside the dish it's discounted, because it's not actually part of what would be the zone
    # Other discs are also not used to factor a theoretical zoe



    valttests = {}
    satttests = {}
    # Arrays to store t tests  of value and saturation
    r = 0
    # r is to count iteration number, it is useful when storing t tests
    for d in range(1, len(discs) + 1):
        # loops through all d discs

        valttests['disc' + str(d)] = {}
        satttests['disc' + str(d)] = {}
        # establishes  that the t tests for value and saturation will all be stored as a dictionary at a certian point at an index at point
        # in a dictionary corresponding to their disc
        r = 0
        # resetting r

        for h in range(15, 100, 2):
            r = r + 1
            # Counts up 1 at a time

            innervalues = np.array([])
            outervalues = np.array([])
            innersats = np.array([])
            outersats = np.array([])
            # Establishes arrays of an inner circle and outer circles
            # These will store the saturation and value of a two circles

            blank_image = np.zeros((height, width, 3), np.uint8)
            cv2.circle(blank_image, (int(newdiscs[d][0]), int(newdiscs[d][1])), h, (255, 255, 255), 1)
            # Creates a circles of radius h of white on a c
            s = 0
            for s in range(0, background.shape[0]):
                blank_image[background[s][0]][background[s][1]][0] = 0
                blank_image[background[s][0]][background[s][1]][1] = 0
                blank_image[background[s][0]][background[s][1]][2] = 0
            # Then any point on that circle that is part of a disc, or the edge of the petri dish is written over
            # Those points do not count in finding the zoes

            for x in range(0, height):
                for y in range(0, width):
                    if (int(blank_image[x][y][0]) == 255 and int(blank_image[x][y][1]) == 255 and int(
                            blank_image[x][y][2]) == 255):
                        innervalues = np.append(grayimg[x][y], innervalues)
                        innersats = np.append(hsvmask[x][y][1], innersats)
            # This goes through the image and finds the points of the blank image that are white, and recored the saturation and value of those points


            # This next portion of the code does the same thing as the previous portion of code, but with a slightly larger circle
            blank_image = np.zeros((height, width, 3), np.uint8)
            cv2.circle(blank_image, (int(newdiscs[d][0]), int(newdiscs[d][1])), h + 4, (255, 255, 255), 1)
            s = 0
            for s in range(0, background.shape[0]):
                blank_image[background[s][0]][background[s][1]][0] = 0
                blank_image[background[s][0]][background[s][1]][1] = 0
                blank_image[background[s][0]][background[s][1]][2] = 0
            for x in range(0, height):
                for y in range(0, width):
                    if (int(blank_image[x][y][0]) == 255 and int(blank_image[x][y][1]) == 255 and int(
                            blank_image[x][y][2]) == 255):
                        outervalues = np.append(grayimg[x][y], outervalues)
                        outersats = np.append(hsvmask[x][y][1], outersats)
                        # The outer circle values and saturations are then recorded

            # Now there are four arrays innervalues and inner saturations contain the values of saturation of a small
            #  circle outervalues and outersats contain the saturation and values of a slightly bigger circle

            p = 3
            innervalmed = np.median(innervalues)
            innervalstd = np.std(innervalues)
            outervalmed = np.median(outervalues)
            outervalstd = np.std(outervalues)
            innervalmean = np.mean(innervalues)
            outervalmean = np.mean(outervalues)

            innersatmed = np.median(innersats)
            innersatstd = np.std(innersats)
            outersatmed = np.median(outersats)
            outersatstd = np.std(outersats)
            innersatmean = np.mean(innersats)
            outersatmean = np.mean(outersats)
            # Establishing statistics of these arrays

            innersats = innersats[abs(innersats - innersatmean) < (p * innersatstd)]
            outersats = outersats[abs(outersats - outersatmean) < (p * outersatstd)]

            innervalues = innervalues[abs(innervalues - innervalmean) < (p * innervalstd)]
            outervalues = outervalues[abs(outervalues - outervalmean) < (p * outervalstd)]
            # Removing outliers for saturation and value


            toppercentile = 90
            botpercentile = 10
            innervalq1 = np.percentile(innervalues, botpercentile)
            innervalq3 = np.percentile(outervalues, toppercentile)
            outervalq1 = np.percentile(outervalues, botpercentile)
            outervalq3 = np.percentile(outervalues, toppercentile)
            innervalues = innervalues[abs(innervalues) < innervalq3]
            outervalues = outervalues[abs(outervalues) < outervalq3]
            innervalues = innervalues[abs(innervalues) > innervalq1]
            outervalues = outervalues[abs(outervalues) > outervalq1]
            # Furter data processing, only for value though.
            # The saturation values are very similar, given a small size, making percentile filtering not fesable given the image size


            valttests['disc' + str(d)][r] = stats.ttest_ind(innervalues, outervalues, equal_var=False)
            satttests['disc' + str(d)][r] = stats.ttest_ind(innersats, outersats, equal_var=False)
            # Does a t test of the value and saturation of the inner circle vs the outer circle
            # The more statistically significant the, higer likelyhood the zone border is there
            # This finds the t statistic and p value for the value and saturation for a theoretical zone for 100 px

    graddists = []
    # distances of the gradient
    resizedists = []
    # array that holds the pixel distances needed for the full size image
    actualdists = []
    # holds the mm distances for each disc
    # Establishing arrays

    for a in range(1, len(discs) + 1):
        # looping through all a discs

        valuetvals = []
        valuepvals = []
        saturationtvals = []
        saturationpvals = []
        mostsignificant = []
        # more arrays, names should be self explanatory

        for b in range(1, len(valttests['disc' + str(a)])):
            valuetvals.append(valttests['disc' + str(a)][b][0])
            valuepvals.append(valttests['disc' + str(a)][b][1])
            saturationtvals.append(satttests['disc' + str(a)][b][0])
            saturationpvals.append(satttests['disc' + str(a)][b][1])
        # separates all the t and p values for a given disc

        for e in range(1, len(valuetvals)):
            if (saturationpvals[e] * 0.5 < 0.001 and valuepvals[e] * 0.5 < 0.01 and saturationtvals[e] < -2 and
                        valuetvals[e] > 2):
                mostsignificant.append((e * 2) + 15)
                # loops through t and p values for every possible zone of inhibition and then goes to find the ones that are statistically significant
                # It looks for a significant change in value and saturation i.e. where the white and lawn interact, or the ZOE

        if len(mostsignificant) == 0:
            graddists.append(10)
            resizedists.append(int(graddists[a - 1] * (1 / downfactor)))
            actualdists.append(6 * mmtopx)
        # If there are no significant p values or t values, there is no zone of inhibition beyond the disc itself and the zone is 6 mm
        else:
            graddists.append(np.median(mostsignificant))
            resizedists.append(int(graddists[a - 1] * (1 / downfactor)))
            actualdists.append(resizedists[a - 1] * 2)
            # Of all the significant distances the median is taken, to avoid outliers throwing of the mean, the most significant distances for a zoe
            # should be next to each other

    zonesats = np.array([])
    zonevals = np.array([])
    zonehues = np.array([])
    # More arrays to check the zone the program arrived at

    finalimg = img.copy()
    # The final image to be output
    for k in range(1, len(discs) + 1):
        # loops through discs
        X = discs[k][0]
        Y = discs[k][1]
        # Location of the disk k

        blank_image = np.zeros((height, width, 3), np.uint8)
        cv2.circle(blank_image, (int(newdiscs[k][0]), int(newdiscs[k][1])), int(graddists[k - 1]), (255, 255, 255), -1)
        cv2.circle(blank_image, (int(newdiscs[k][0]), int(newdiscs[k][1])), int(10), (0, 0, 0), -1)
        # Draws the zone the program found on a blank image in white

        for x in range(0, height):
            for y in range(0, width):
                if (int(blank_image[x][y][0]) == 255 and int(blank_image[x][y][1]) == 255 and int(
                        blank_image[x][y][2]) == 255):
                    zonesats = np.append(hsvmask[x][y][1], zonesats)
                    zonevals = np.append(hsvmask[x][y][2], zonevals)
                    zonehues = np.append(hsvmask[x][y][0], zonehues)
        # Finds the hues saturation, and values of that zone

        m = 3
        toppercentile = 80
        botpercentile = 20

        if graddists[k - 1] != 10:
            # If there's no zone no need to check
            valstd = np.std(zonevals)
            satstd = np.std(zonesats)
            satavg = np.mean(zonesats)
            valavg = np.mean(zonevals)
            satmed = np.median(zonesats)
            valmed = np.median(zonevals)

            zonevals = zonevals[abs(zonevals - valmed) < (p * valstd)]
            zonesats = zonesats[abs(zonesats - satmed) < (p * satstd)]

            satq1 = np.percentile(zonesats, botpercentile)
            satq3 = np.percentile(zonesats, toppercentile)
            valq1 = np.percentile(zonevals, botpercentile)
            valq3 = np.percentile(zonevals, toppercentile)
            # print(satq1, satq3, valq1, valq3)
            zonesats = zonesats[abs(zonesats) < satq3]
            zonevals = zonevals[abs(zonevals) < valq3]
            zonesats = zonesats[abs(zonesats) > satq1]
            zonevals = zonevals[abs(zonevals) > valq1]
            # more data processing of the values and saturation of this zone, taking out outliers

            if np.mean(zonesats) < 35 and np.median(zonesats) < 35:
                # Makes sure the zone's saturation is not to high, meaning that the zones are white and not filled with something
                # cv2.circle(finalimg, (X, Y), resizedists[k - 1], (0, 0, 0), 20)
                cv2.circle(finalimg, (X, Y), resizedists[k - 1], (0, 0, 0), 5)
                text = "Disc " + str(k) + ': ' + str(math.floor(actualdists[k - 1] * pxtomm)) + 'mm'
                # cv2.putText(finalimg, text, (X - 140, Y - 140),
                #            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 20)
                cv2.putText(finalimg, text, (X - 140, Y - 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5)
            # Draws circles and puts text of the zones diameter, does it twice to get a clear readable red on black text
            # Morgan - adjusting to black text and circle
            else:
                # cv2.circle(finalimg, (X, Y), int(10 * (1 / downfactor)), (0, 0, 0), 20)
                cv2.circle(finalimg, (X, Y), int(10 * (1 / downfactor)), (0, 0, 0), 5)
                text = "Disc " + str(k) + ': ' + str(6) + 'mm'
                # cv2.putText(finalimg, text, (X - 140, Y - 140),
                #            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 20)
                cv2.putText(finalimg, text, (X - 140, Y - 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5)
                # Draws circles and puts text of the zones diameter, does it twice to get a clear readable red on black text
                # If the zone has too much stuff inside there is no zone drawn and it become 6 mm (a disc)
                # Morgan - adjusting to black text for circle and text
        else:
            # cv2.circle(finalimg, (X, Y), int(10 * (1 / downfactor)), (0, 0, 0), 20)
            cv2.circle(finalimg, (X, Y), resizedists[k - 1], (0, 0, 0), 5)
            text = "Disc " + str(k) + ': ' + str(math.floor(actualdists[k - 1] * pxtomm)) + 'mm'
            # cv2.putText(finalimg, text, (X - 140, Y - 140),
            #            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 20)
            cv2.putText(finalimg, text, (X - 140, Y - 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 5)
            # Draws circles and puts text of the zones diameter, does it twice to get a clear readable red on black text
            # If the zone has too much stuff inside there is no zone drawn and it become 6 mm (a disc)
            # Morgan Edit - Changing to black instead of red for text and circle drawing
        shrunkimg = cv2.resize(finalimg, (0, 0), fx=0.2, fy=0.2)

        ####################################print(actualdists)

    head, tail = os.path.split(filepath)
    if len(head) > 0:
        # Makes it so that if you use a univeral path it writes correctly as a the split function doesn't add a slash at the end of the head string
        cv2.imwrite(head + '/zonesfound' + tail, shrunkimg)
        return (head + '/zonesfound' + tail), actualdists, discs
    # writes a file of an image with zones and returns the filepath along with the zone diameters in order of the zones labeled on the image
    else:
        cv2.imwrite(head + '/zonesfound' + tail, shrunkimg)
        return (head + '/zonesfound' + tail), actualdists, discs


def locatediscs(filepath):
    # This function takes in an image file path, finds the discs on that image writes a new image to the disc with the same path, but with 'discsfound'
    # before the title of the orignal image, and returns the file path to the new image

    # Import These Libraries
    # import cv2
    # import numpy as np
    # import os
    # import math
    # import copy
    # FYI ZOE(s) = Zone of Inhibition(s)

    # Take an input image and do pre-processing
    wordup = filepath
    # No current way to set multiple images to each other this string is used multiple points in the code for the program to see what image to read

    img = cv2.imread(wordup)
    imgblur = cv2.GaussianBlur(img, (15, 15), 0)
    imggray = cv2.cvtColor(imgblur, cv2.COLOR_BGR2GRAY)
    imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgbgr = cv2.cvtColor(imghsv, cv2.COLOR_HSV2BGR)
    # turn it to B/W and blur it to eliminate noise
    hue, sat, val = cv2.split(imghsv)
    # The image has to be split into hsv channels to get the value of all the pixels
    width, height = img.shape[:2]
    dishblank = np.zeros((width, height, 3), np.uint8)
    pxtomm = 0.0307692
    mmtopx = 1 / pxtomm

    v = 0
    discs = {}
    discimgs = {}
    discmask = {}
    index = []
    imgclean = cv2.imread(wordup)
    verifyimg = copy.deepcopy(img)
    # V represents the discs
    # discs is a dictionary to store the discs' location in the image
    # imgclean is a new img to work with

    for x in range(0, 256):
        retval3, threshphoto = cv2.threshold(imggray, x, 255, cv2.THRESH_BINARY)
        edgephoto, contours, hierarchy = cv2.findContours(threshphoto, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Thresholds and finds the contours of the image given threshold x
        v = 0
        # v is to count discs at a given threshold
        for c in contours:
            # loops through contours to finds any ones that fit the parameter of a disc

            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            # INFORMATION THAT MAY BE USEFUL TO BE MORE ACCURATE IN FINDING DISCS USE AT YOUR OWN DISCRETION
            # Area = cv2.contourArea(c) * pxtomm
            # circumfrence = cv2.arcLength(c, True)*pxtomm
            # AreaR = math.sqrt(cv2.contourArea(c)/math.pi)*pxtomm
            # CircR = circumfrence/(math.pi*2)
            # diametermm = AreaR*2
            # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


            M = cv2.moments(c)
            # Establishes a moment, they're like moments in physics gives a snapshot of the image
            # Long story short they help you understand information about the contour
            if (M["m00"] != 0) and (1.2 / 1) > M['mu20'] / M['mu02'] > (1 / 1.2) and 500 < cv2.arcLength(c,
                                                                                                         True) < 800 and 15000 < cv2.contourArea(
                c) < 30000:
                # These checks need to past to find a disc, mu02 and mu20 are moments that describe the standard deviation of the contour in the x and y directions
                # m00 is the moment's size
                # These make sure the disc is the right size, has a circumfrence that seems right given the size, and is circular enough
                v = v + 1
                # counts the number of discs found
        index.append(v)
    # Records the discs found in each threshold, index[x] gives the number of discs found at threshold x



    goodthresh = []
    # best thresh = best threshold number ... kinda self explanatory
    bestthresh = 0
    z = 0
    for y in range(0, len(index)):
        if index[y] > index[bestthresh]:
            bestthresh = y
    for z in range(0, len(index)):
        if index[z] == index[bestthresh]:
            goodthresh.append(z)
    bestthresh = int(np.mean(goodthresh))
    # Searches through the index to find the threshold with the right number of discs, i.e. the one equal to the discnum(inputted by the user)
    # Hope to un-hardcode at some point
    if bestthresh == 0:
        bestthresh = 127
    # Precautionary measure if the discs aren't found 127 is considered a good "default threshold"

    ret3, otsuThresh = cv2.threshold(imggray, bestthresh, 255, cv2.THRESH_BINARY)
    im3, contours, hierarchy = cv2.findContours(otsuThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    v = 0
    # V Serves the same purpose


    for c in contours:

        M = cv2.moments(c)
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        # INFORMATION THAT MAY BE USEFUL TO BE MORE ACCURATE IN FINDING DISCS USE AT YOUR OWN DISCRETION
        Area = cv2.contourArea(c) * pxtomm
        circumfrence = cv2.arcLength(c, True) * pxtomm
        AreaR = math.sqrt(cv2.contourArea(c) / math.pi) * pxtomm
        CircR = circumfrence / (math.pi * 2)
        diametermm = AreaR * 2
        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # Same contour function as before, looks for discs at the threshold that finds the most discs

        if (M["m00"] != 0) and (1.2 / 1) > M['mu20'] / M['mu02'] > (1 / 1.2) and 500 < cv2.arcLength(c,
                                                                                                     True) < 800 and 15000 < cv2.contourArea(
            c) < 30000:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            v = v + 1
            discs[v] = cX, cY
            text = "Disc " + str(v)
            discimgs[v] = imgclean[int(cY - (CircR * mmtopx)):int(cY + (CircR * mmtopx)),
                          int(cX - (CircR * mmtopx)): int(cX + (CircR * mmtopx))].copy()
            # Isolating the disc in a small array, which is saved to a dictionary
            cv2.drawContours(imgclean, [c], -1, (0, 0, 0), -1)
            discmask[v] = imgclean[int(cY - (CircR * mmtopx)):int(cY + (CircR * mmtopx)),
                          int(cX - (CircR * mmtopx)): int(cX + (CircR * mmtopx))].copy()
            cv2.drawContours(verifyimg, [c], -1, (0, 0, 255), 5)
            cv2.putText(verifyimg, text, (cX - 140, cY - 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    head, tail = os.path.split(filepath)
    shrunkimg = cv2.resize(verifyimg, (0, 0), fx=0.2, fy=0.2)
    # splits file path
    # /home/documents/zone/dish.jpeg -> head = '/home/documents/zone and' tail = 'dish.jpeg'
    # writes
    if len(head) > 0:
        # Makes it so that if you use a univeral path it writes correctly as a the split function doesn't add a slash at the end of the head string or
        # start of the tail string
        cv2.imwrite(head + '/discsfound' + tail, shrunkimg)
        return head + '/discsfound' + tail, discs, discimgs, discmask
    else:
        cv2.imwrite(head + 'discsfound' + tail, shrunkimg)
        return head + 'discsfound' + tail, discs, discimgs, discmask


def zoneadjuster(zonedists, disc, increasing, magnitude):
    newdists = []
    pxtomm = 0.0307692
    mmtopx = 1 / 0.0307692

    # Takes All the zone RADII as zonedists as an array that starts from zero
    # It takes the zones as mm
    # The discs and zones whould always correspond with the exception of being in array or dictionary
    # Zonefinder returns  an array of zone radii with their index being the disc number, so you can feed that programs output into this one
    # Takes the disc's zone you want to add or subtract from
    # Increasing = true means you want to make the zone bigger
    # magnitude is how much you want to change the circle by
    if increasing == True:
        direction = 1
    else:
        direction = -1
    # Which direction

    for x in range(0, len(zonedists)):
        if x == disc - 1:
            # Disc nnumber is 1 higher in the array since disc 1 is stored at zonedists[0]
            newdists.append((direction * magnitude * mmtopx) + zonedists[x])
        else:
            newdists.append(zonedists[x])
            # converts from mm to px for circle drawer

    # Return
    return newdists


def circledrawer(cleanimg, distances, coordinates):
    # This function takes an petri dish image with nothing on it, and draws it's zones, given the distances and coordinates, are the same and correspond
    # If you are using my previous programs they should

    pxtomm = 0.0307692
    mmtopx = 1 / pxtomm
    downfactor = 0.2
    # Take an input image and do pre-processing
    img = cv2.imread(str(cleanimg))
    # Cleanimg is an unaltered image
    # distances are the zone dists
    # coordinates are the disc coords in the image
    # coordinates[x] should match distances[x]

    for Z in range(0, len(distances)):
        # loops through
        X = int(coordinates[Z + 1][0])
        Y = int(coordinates[Z + 1][1])
        #print(coordinates)
        pxdist = int(distances[Z])
        #print(pxdist)
        # xy coords and the pixel distance established
        # cv2.circle(img, (X, Y), int(pxdist / 2), (0, 0, 0), 20)
        cv2.circle(img, (X, Y), int(pxdist / 2), (0, 0, 0), 5)
        text = 'Disc ' + str(Z + 1) + ': ' + str(math.ceil((pxtomm * pxdist))) + ' mm'
        # cv2.putText(img, text, (X - 140, Y - 140),
        #            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 20)
        cv2.putText(img, text, (X - 140, Y - 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 3)
        # Morgan - Adjusting to black text and thin line only
    # convert back into mm and put text on the disc
    smallimg = imgdif = cv2.resize(img, (0, 0), fx=downfactor, fy=downfactor)
    head, tail = os.path.split(cleanimg)
    if len(head) > 0:
        # Makes it so that if you use a univeral path it writes correctly as a the split function doesn't add a slash at the end of the head string or
        # start of the tail string
        cv2.imwrite(head + '/newzones' + tail, smallimg)
        return head + '/newzones' + tail
    else:
        cv2.imwrite(head + 'newzones' + tail, smallimg)
        return head + 'newzones' + tail


def featurefinder(discimgs, discmask):
    lonediscs = {}
    graydiscs = {}
    textdiscs = {}

    # Loops throuh the discs its found, and isolates them, making sure that only the disc itself is viewable
    for d in range(1, len(discmask) + 1):
        width, height = discimgs[d].shape[:2]
        graydiscs[d] = cv2.cvtColor(discimgs[d], cv2.COLOR_BGR2GRAY)
        lonediscs[d] = np.zeros((height, width, 3), np.uint8)
        # making the discs B/W, and a new disc to assign these values to
        for y in range(0, width - 1):
            for x in range(0, height - 1):
                if discmask[d][x][y][0] == 0 and discmask[d][x][y][1] == 0 and discmask[d][x][y][2] == 0:
                    lonediscs[d][x][y][0] = graydiscs[d][x][y]
                    lonediscs[d][x][y][1] = graydiscs[d][x][y]
                    lonediscs[d][x][y][2] = graydiscs[d][x][y]
                # looping over the mask and getting rid of the background
                else:
                    lonediscs[d][x][y][0] = 255
                    lonediscs[d][x][y][0] = 255
                    lonediscs[d][x][y][0] = 255

        imghsv = cv2.cvtColor(discimgs[d], cv2.COLOR_BGR2HSV)

        hue, sat, val = cv2.split(imghsv)
        # Converting to hsv to get the value
        flattenedvalues = val.flatten()
        # Getting the value as a 1 d array for data processing
        reorganizer = np.zeros(256, np.uint8)
        # Making another array to reorganize the data
        for a in range(0, len(flattenedvalues)):
            reorganizer[flattenedvalues[a]] = reorganizer[flattenedvalues[a]] + 1
        # Reorganizing the data for the scipy peaks function
        peaks = signal.find_peaks_cwt(reorganizer, np.arange(2, 10), noise_perc=40.0)
        # finding the peaks

        if len(peaks) != 0:
            # Finding the peaks that are low, i.e. the peaks that represent the darkness of the text
            thresh = int(np.amin(peaks) + 2)
        # Adding two so it doesn't accidentally cut of any text
        else:
            thresh = int(np.mean(flattenedvalues - np.std(flattenedvalues)))
        # If no peaks are found then proceed to take the mean - the standard deviation, this means the text is very strange

        retval, textdiscs[d] = cv2.threshold(graydiscs[d], thresh, 255, cv2.THRESH_BINARY)
    # Threshold the discs to get a binary image


    orb = cv2.ORB_create(200, scaleFactor=1.1, nlevels=20, edgeThreshold=10, firstLevel=0, WTA_K=2, patchSize=50)
    # Orb creates a descriptor
    features = {}
    keypoints = {}
    # Dictionary of features and keypoints
    for t in range(1, len(textdiscs) + 1):
        keypoints[t], features[t] = orb.detectAndCompute(textdiscs[t], None)
    # making a dictionary of features and key points, 1 for each disc
    return features


def discsearcher(features):
    cursor = dbh.cursor()
    # connect to database
    # execute the SQL query using execute() method.
    cursor.execute("select abx_descriptor from antibiotics")
    data = cursor.fetchall()
    # get antibiotic descriptors
    cursor.execute("select abx_name  from antibiotics")
    prevdiscnames = cursor.fetchall()
    # get antibiotic names
    notfoundmessage = 'No matching antibiotic Discs found'
    # message for when nothing is found
    discnames = {}
    if len(features) == 0:
        for d in range(1, len(features) + 1):
            discnames[d] = notfoundmessage
    else:
        # If the database is empty say nothing is found
        # If the database is empty say nothing is found

        discalignments = np.zeros(len(data), np.uint8)
        bestmatches = np.zeros(len(data), np.uint8)
        discdatapoint = np.zeros(len(features), np.uint8)
        discmatchnums = np.zeros(len(features), np.uint8)
        for e in range(0, len(data)):
            if data[e][0] != '':
                # loops through every known features for discs
                matchcomparison = np.array([])
                # array to store the matches
                discfile = open(data[e][0].rstrip(), "rb")
                # open the filepath to the pickle that contains the eth disc
                seendisc = pickle.load(discfile)
                # loads a file to a dictionary
                for h in range(0, len(seendisc)):
                    # loops through the dictionary containing feature set(s) for each previous disc
                    for b in range(1, len(features) + 1):
                        # loops through the features of all 6 discs given by the input
                        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                        # matcher object used by orb
                        aligner = matcher.match(seendisc[h], features[b])
                        # matched features
                        truematches = []
                        distances = []
                        # arrays to store the matches and sdistances there of
                        for f in range(0, len(aligner)):
                            distances.append(aligner[f].distance)
                            if aligner[f].distance < 25:
                                truematches.append(aligner[f].distance)
                        # stores the distances that pass a cutoff, i.e. true matches
                        # print('stds', np.std(distances))

                        matchcomparison = np.append(matchcomparison, len(truematches))
                        # records all the matches, and number of true matches between the 6 discs
                index = np.argmax(matchcomparison)
                # gets the index of the best match
                basic = math.floor(index / len(features)) * len(features)
                matchindex = index - basic
                # find what disc it belongs to
                if np.amax(matchcomparison) > discmatchnums[matchindex]:
                    # if this is the best match for this disc, then record it, and then put it as the candidate to beat for best match
                    discmatchnums[matchindex] = np.amax(matchcomparison)
                    discdatapoint[matchindex] = e
        # print(discdatapoint)
        # print(discmatchnums)

        for g in range(0, len(discdatapoint)):
            # looks through the best matches found for each disc
            if discmatchnums[g] != 0:
                # If a match was found find it's name in the database and asign it to a dictionary at the index of the disc at the same position
                discnames[g + 1] = prevdiscnames[discdatapoint[g]][0]
            else:
                # if nothing was found say so at that index
                discnames[g + 1] = notfoundmessage
        # return a dictionary of disc names starting at one
        return discnames


def discwriter(discs, descriptors, filepath):
    # cnx = mysql.connector.connect(user='root', database='incubator', password = 'Letmein!')
    # connect to database
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
            if discs[d + 1] == discnames[n]:
                if knownfeatures[n] != '':
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
                    if len(filepath) > 0:
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
                        cursor.execute(
                            "update antibiotics set abx_descriptor = " + str(entirepath) + "where abx_id = " + str(
                                knownfeatures[n]))


    num = 0
    for a in range(1, len(discs) + 1):
        num += 1

        if existance[a - 1] != 1:
            entirepath = ''
            # If you don't find a matching antibiotic
            if len(filepath) > 0:
                entirepath = head + '/' + discs[a] + '.pkl'
            # make a file at a given folder
            else:
                entirepath = discs[a] + '.pkl'
            # make a pickle file with those descriptors in a dictionary
            tempdict = {}
            features = open(entirepath, "wb")
            tempdict[0] = descriptors[a]
            # make a new dictionary and dump it in that file
            pickle.dump(tempdict, features)
            features.close()
            # push it to the database.
            # Modified the code to update antibiotic table descriptors [Comfort]
            cursor.execute(
                "update antibiotics set abx_descriptor = '" + str(entirepath) + "' where abx_name = '" + str(
                    discs[num])+"'")


# noinspection PyUnusedLocal,PyShadowingNames
def zonefinderInitializer():
    global newImageFile
    global arrayDistances
    global discs
    global old_img

    calledsample_id = StringVar()
    calledsample_img = StringVar()
    callzonefinder = dbh.cursor()
    exec_stateSet = dbh.cursor()

    dbh.commit()
    callzonefinder.execute(zonefinderInitializerQ)
    for callerfinder in callzonefinder.fetchall():
        if callerfinder[0] == 0:
            print(callerfinder[3])
            try:
                exec_stateSet.execute("UPDATE petri_dish SET exec_state = 1 WHERE  sample_id = " + str(callerfinder[3]))
                dbh.commit()
            except pymysql.Error as e:
                print(e)
                dbh.rollback()
            global notificationBtn
            baseLoopcolor = None

            def change_color():
                global baseLoopcolor

                try:
                    current_color = notificationBtn.cget("foreground")
                    next_color = "white" if current_color == "black" else "black"
                    notificationBtn.config(foreground=next_color)
                    baseLoopcolor = base.after(1000, change_color)
                except:
                    pass

            change_color()
            try:
                notificationBtn["text"] = "EXECUTING BACKGROUND PROCESS"
            except:
                pass

            old_img = imglocationhome + str(callerfinder[3]) + ".png"
            calledsample_id.set(callerfinder[3])
            calledsample_img.set(callerfinder[4])

            def executeTestCompleted():
                global newImageFile
                global arrayDistances
                global discs
                try:
                    newImageFile, arrayDistances, discs = zonefinder(old_img)
                except:
                    pass

            zonefinderInitializerThread = threading.Thread(target=executeTestCompleted,
                                                           name="zonefinderInitializerThread")
            zonefinderInitializerThread.start()
            #zonefinderInitializerThread.join()

            def waitForThreadtoComplete():
                baseLoop = base.after(1000, waitForThreadtoComplete)

                if zonefinderInitializerThread.isAlive():
                    #print(zonefinderInitializerThread.isAlive())

                    pass
                else:
                    global baseLoopcolor

                    arrayD = arrayDistances.copy()
                    arrayDist = arrayDistances.copy()
                    arrayDist[:] = [x * 0.0307692 for x in arrayD]

                    notificationBtn["text"] = "PROCCESSING COMPLETED"
                    next_color = "Black"
                    notificationBtn.config(foreground=next_color)
                    #base.after_cancel(baseLoopcolor)

                    discsObject = dbh.cursor()
                    for a1 in discs:
                        dbh.commit()
                        try:
                            discsObject.execute(
                                "INSERT INTO zones (disc,sample_id) VALUES ('" + str(discs[a1]) + "'," + str(
                                    calledsample_id.get()) + ")")
                            dbh.commit()
                            print(1)
                        except:
                            dbh.rollback()
                            print(0)

                    print("Completed...Zones")



                    imgcompleted = imglocationhome + "zonesfound" + str(callerfinder[3]) + ".png"

                    dbh.commit()
                    try:
                        discsObject.execute(
                            "INSERT INTO images (state,imagelocation,sample_id) VALUES (3,'" + str(
                                imgcompleted) + "'," + str(
                                calledsample_id.get()) + ")")
                        dbh.commit()
                        print(1)

                    except:
                        dbh.rollback()
                        print(0)

                    print("Completed...Images")


                    dbh.commit()
                    try:
                        discsObject.execute(
                            "UPDATE pocket_state set state = 1 WHERE pocket_id = " + str(callerfinder[5]))
                        dbh.commit()
                        print(1)

                    except:
                        dbh.rollback()
                        print(0)

                    print("Completed... pocket state")

                    dbh.commit()
                    try:
                        discsObject.execute(
                            "UPDATE petri_dish set state = 3 WHERE sample_id = " + str(calledsample_id.get()))
                        dbh.commit()
                        print(1)

                    except:
                        dbh.rollback()
                        print(0)

                    print("Completed...petridish")

                    count = -1
                    count_12 = 0
                    arr = None
                    vals = {}
                    insertIntoDiameter = dbh.cursor()
                    checkAbx = dbh.cursor()
                    checkAbx.execute("SELECT disc_id  FROM discs WHERE sample_id =" + str(calledsample_id.get()) + "")

                    for _ in arrayDist:
                        count += 1
                        count_12 += 1
                        arr = math.floor(arrayDist[count])
                        vals[count_12] = arr

                    count_12 = 0
                    count = -1
                    valueInsert = StringVar()
                    for abx_sample_id, coount in zip(vals, checkAbx.fetchall()):
                        count_12 += 1
                        count += 1
                        valueInsert.set(str(vals[count_12]))
                        dbh.commit()
                        try:
                            insertIntoDiameter.execute(
                                "UPDATE discs set diameter=" + str(
                                    valueInsert.get()) + " WHERE sample_id=" + str(
                                    calledsample_id.get()) + " and disc_id =" + str(coount[0]) + "")
                            dbh.commit()
                        except:
                            print(0)
                            dbh.rollback()
                        dbh.rollback()
                    base.after_cancel(baseLoop)

            waitForThreadtoComplete()

    base.after(1000, zonefinderInitializer)


# noinspection PyUnusedLocal,PyShadowingNames
def printAgarLabel():
    agarRoot = Toplevel(base)
    agar_frame = cal.Frame(agarRoot, relief=SOLID, padding=10)
    agarRoot.config(background="#fff")

    # noinspection PyUnusedLocal
    def agar_input_Field(self):
        agar_input.delete(0, "end")

    def quantity_input_Field():
        quantity_input.delete(0, "end")

    def printLabel():
        file_write = open("assets/file/print.lbl", "w")
        file_write.write('\nN\nA30,20,0,3,1,1,N,"' + agar_input.get() + '"\nB30,100,0,1,2,2,30,B,"' + str(
            random.randint(24, 74)) + "-" + str(random.randint(24, 304)) + "-" + str(
            random.randint(34, 454)) + '"\nP1')
        file_write.close()

        os.system("bash /home/pi/Desktop/pi_integr/incubator/assets/file/script")

    agar_input = cal.Entry(agar_frame, width=35, font=("SEGOEUI", 14), justify="center")
    labe1 = cal.Label(agar_frame, text="Suggested Text", padding=10)
    label2 = cal.Label(agar_frame, text="MH | Date Made | Date Expire", padding=10)
    quantity_input = cal.Entry(agar_frame, width=35, font=("SEGOEUI", 14), justify="center")
    printBtn = cal.Button(agar_frame, text="Print Label", padding=30, width=30, command=printLabel)
    cancelBtn = cal.Button(agar_frame, text="Cancel", padding=30, width=30, command=agarRoot.destroy)
    cal.Label(agarRoot, text="PRINT AGAR LABEL").pack(pady=10)
    agar_input.pack(ipady=10)
    agar_input.insert(0, "Enter Label Text")
    quantity_input.insert(0, "Enter Label Quantity")
    agar_input.bind("<FocusIn>", agar_input_Field)
    quantity_input.bind("<FocusIn>", quantity_input_Field)
    label2.pack()
    quantity_input.pack(ipady=10)
    printBtn.pack(pady=10)
    cancelBtn.pack(pady=10)
    agar_frame.pack()


# noinspection PyUnusedLocal,PyShadowingNames
def reportResults():
    def singleTestProgressing(val):

        sample_id = StringVar()
        sample_id.set(val)
        newImageFile = None

        global imageDisplayScaled
        global imgDisplay

        singleTestdbobject = dbh.cursor()
        dbh.commit()
        singleTestdbobject.execute(
            "SELECT imagelocation FROM images WHERE state=3 AND sample_id= " + str(sample_id.get()))
        for imgloc in singleTestdbobject.fetchall():
            newImageFile = imgloc[0]

        discs = {}
        sampleBuild.execute("SELECT * from zones where sample_id =" + str(sample_id.get()))
        count = 1
        for a2 in sampleBuild.fetchall():
            val = a2[1].split(",")[0]
            val2 = a2[1].rsplit(",")[-1]
            discs[count] = ((int(val[1:])), (int(val2[:-1])))

            count += 1

        imgDisplay = PhotoImage(file=newImageFile)
        B_name = StringVar()
        singleRoot = Toplevel(base, background="#FFF")
        callId = dbh.cursor()
        callId.execute(
            "SELECT * FROM samples sa inner join bacteria ba on sa.bacteria_id = ba.bacteria_id where sa.sample_id=" + str(
                sample_id.get()) + " limit 1")
        for p_id in callId.fetchall():
            cal.Label(singleRoot,
                      text="PATIENT ID[" + str(p_id[1]) + "] BACTERIA [" + str(p_id[5]) + "]").pack(
                pady=10)
        frame_top = cal.Frame(singleRoot, padding=5, relief=SOLID)
        cal.Label(frame_top, text="Antibiotics", width=21).pack(side="left", padx=3, anchor="w")
        cal.Label(frame_top, text="Dose", width=5).pack(side="left", padx=3, anchor="w")
        cal.Label(frame_top, text="MM", width=4).pack(side="left", padx=3, anchor="w")
        cal.Label(frame_top, text="S>", width=4).pack(side="left", padx=3, anchor="w")
        cal.Label(frame_top, text="R<", width=4).pack(side="left", padx=3, anchor="w")
        cal.Label(frame_top, text="Inter", width=4).pack(side="left", padx=3, anchor="w")
        frame_top.pack()

        callData_TestDone = dbh.cursor()
        dbh.commit()
        abx_result_labelSwitch = {}
        abx_result_labeldec = {}
        callData_TestDone.execute(
            "SELECT * FROM samples sa INNER JOIN petri_dish pd INNER JOIN discs ds INNER JOIN antibiotics an on sa.sample_id=pd.sample_id and ds.abx_id = an.abx_id and sa.sample_id=ds.sample_id where sa.sample_id=" + str(
                sample_id.get()) + " and state =3")
        counter_abx = 0
        for conterPlus in callData_TestDone.fetchall():
            counter_abx += 1
            B_name.set(conterPlus[16])
            data_m = (B_name.get()[:20] + "...") if len(B_name.get()) > 20 else B_name.get()
            frame_top = cal.Frame(singleRoot, padding=5, relief=SOLID)
            abx_result_label[counter_abx] = cal.Label(frame_top,
                                                      text=str(counter_abx) + ". " + str(data_m),
                                                      width=21)
            abx_result_label[counter_abx].pack(side="left", padx=3, anchor="w")
            abx_result_label[counter_abx] = cal.Label(frame_top, text=str(conterPlus[17]), width=5)
            abx_result_label[counter_abx].pack(side="left", padx=3, anchor="w")
            abx_result_labelSwitch[counter_abx] = cal.Label(frame_top, text=str(conterPlus[12]),
                                                            width=4)
            abx_result_labelSwitch[counter_abx].pack(side="left", padx=3, anchor="w")
            abx_result_label[counter_abx] = cal.Label(frame_top, text=str(conterPlus[19]), width=4)
            abx_result_label[counter_abx].pack(side="left", padx=3, anchor="w")
            abx_result_label[counter_abx] = cal.Label(frame_top, text=str(conterPlus[20]), width=4)
            abx_result_label[counter_abx].pack(side="left", padx=3, anchor="w")
            if conterPlus[12] >= conterPlus[19]:
                abx_result_labeldec[counter_abx] = cal.Label(frame_top, text="S", width=4)
                abx_result_labeldec[counter_abx].pack(side="left", padx=3, anchor="w")
            elif conterPlus[12] < conterPlus[20]:
                abx_result_labeldec[counter_abx] = cal.Label(frame_top, text="R", width=4)
                abx_result_labeldec[counter_abx].pack(side="left", padx=3, anchor="w")
            else:
                abx_result_labeldec[counter_abx] = cal.Label(frame_top, text="I", width=4)
                abx_result_labeldec[counter_abx].pack(side="left", padx=3, anchor="w")

            frame_top.pack()

        # print(abx_result_label)

        lower_frame = cal.Frame(singleRoot, padding=5)
        approveBtn = cal.Button(lower_frame, text="Approve", command=singleRoot.destroy, padding=20,
                                width=20)
        cal.Button(lower_frame, text="Cancel", padding=20, command=singleRoot.destroy,
                   width=20)
        approveBtn.pack()
        lower_frame.pack()

    dbh.commit()
    getBacteria.execute(
        "SELECT sa.accession_number,pd.sample_id ,ba.bacteria_name,pd.sample_id FROM samples sa INNER JOIN petri_dish pd inner join bacteria ba on ba.bacteria_id = sa.bacteria_id and sa.sample_id=pd.sample_id where state =3")
    bacteria_list = getBacteria.fetchall()
    bacteria_list1.set(bacteria_list)

    list_sample = list()
    counter = 1
    for row in bacteria_list:
        list_sample.append(str(counter) + "." + str(row[0]) + "  (" + str(row[2]) + ")")
        counter += 1

    def isolate_selected(event):
        serch_1.delete(0, 'end')
        try:
            serch_1.insert(0, event.widget.get(event.widget.curselection()))
            isolate_name.set(event.widget.get(event.widget.curselection()))
        except:
            pass

    # noinspection PyShadowingNames
    def serch_isolate(val):
        value = val.widget.get()
        value = value.strip().lower()
        if value == '':
            data = list_sample

        else:
            data = []
            for item in list_sample:
                if value in item.lower():
                    data.append(item)

        listbox_update(data)

    def listbox_update(data):
        isolate_list.delete(0, 'end')
        data = sorted(data, key=str.lower)
        for item in data:
            isolate_list.insert('end', item)

    pocket_stateCount = IntVar()
    completedTestsRoot = Toplevel(base, background="#FFF")
    frame_b1 = cal.Frame(completedTestsRoot, padding=20, relief=SOLID)

    cal.Label(completedTestsRoot, text="TESTS REPORT").pack(pady=10)
    serch_1 = cal.Entry(frame_b1, width=35, font=("SEGOE UI", 15))
    serch_1.pack(ipady=10, pady=10)
    isolate_list = Listbox(frame_b1, width=35, font=("SEGOE UI", 15))
    listbox_update(list_sample)
    isolate_list.bind("<<ListboxSelect>>", isolate_selected)
    serch_1.bind("<KeyRelease>", serch_isolate)
    isolate_list.pack()
    optSection = cal.Frame(frame_b1)
    cal.Button(optSection, text="CLOSE", padding=15, width=14, command=completedTestsRoot.destroy).pack(padx=3, pady=10,
                                                                                                        side=LEFT)
    cal.Button(optSection, text="VIEW", padding=15, width=14,
               command=lambda: singleTestProgressing(isolate_name.get())).pack(padx=3, pady=10, side=LEFT)
    optSection.pack()
    frame_b1.pack()


# noinspection PyUnusedLocal,PyShadowingNames
def resultsInProgress():
    global newImageFile
    global arrayDistances
    global discs
    global old_img

    pocket_stateCount = IntVar()
    resultRoot = Toplevel(base, background="#FFF")
    upperFrame = cal.Frame(resultRoot, padding=5)
    test_in_progress = dbh.cursor()
    dbh.commit()
    test_in_progress.execute("SELECT COUNT(*) FROM pocket_state WHERE state=0")
    for count in test_in_progress.fetchall():
        pocket_stateCount.set(count[0])

    pocket_stateCountNumber = IntVar()
    timeLeftDifference = IntVar()
    callData_Test_Number = dbh.cursor()
    callData_Test_One = dbh.cursor()
    assesionNumber = StringVar()

    if pocket_stateCount.get() == 0:
        pocketRoot_Frame = cal.Frame(upperFrame, padding=15, relief=SOLID)
        cal.Label(pocketRoot_Frame, text="NO TEST IN PROGRESS", padding=10, foreground="blue").pack(side="left",
                                                                                                    padx=10, anchor="w")
        pocketRoot_Frame.pack()


    elif pocket_stateCount.get() > 0:
        countsize = -1
        callData_Test_Number.execute("SELECT pocket_id FROM pocket_state  WHERE state = 0")
        for count_1 in callData_Test_Number.fetchall():
            pocket_stateCountNumber.set(count_1[0])
            # print(pocket_stateCountNumber.get())
            callData_Test_One.execute(
                "SELECT CONCAT(timestampdiff(hour,now(),pd.endTime),' Hours') as durationLeft," + str(
                    " ") + "sa.accession_number,pd.dish_id,pd.sample_id, timestampdiff(hour,now(),pd.endTime) as durationzero " + str(
                    " ") + ",  timestampdiff(minute,now(),pd.endTime) as mins FROM samples sa INNER JOIN petri_dish pd on sa.sample_id=pd.sample_id where pd.dish_id = " + str(
                    pocket_stateCountNumber.get()) + " and state =1 ")
            for cnt in range(pocket_stateCount.get()):
                for count in callData_Test_One.fetchall():
                    countsize += 1
                    assesionNumber.set(str(count[1]))
                    # print(assesionNumber.get())
                    cal.Frame(upperFrame).pack(pady=5)
                    pocketRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)

                    cal.Label(pocketRoot_Frame, text="    POCKET  NUMBER " + str(count[2]), width=20).pack(
                        side="left", padx=10, anchor="w")
                    patient_idRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    cal.Label(patient_idRoot_Frame, text="Assesion #", width=20).pack(side="left", padx=10, anchor="w")
                    patient_Ids[countsize] = cal.Label(patient_idRoot_Frame, text=str(count[1]), width=20)
                    patient_Ids[countsize].pack(side="left", padx=10, anchor="w")
                    letfTimeRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    cal.Label(letfTimeRoot_Frame, text="Time Left", width=20).pack(side="left", padx=10, anchor="w")
                    timeLeftDifference.set(count[4])
                    patient_Ids[countsize] = cal.Label(letfTimeRoot_Frame,
                                                       text=str(count[0]), width=20)
                    patient_Ids[countsize].pack(side="left", padx=10, anchor="w")
                    statusRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    cal.Label(statusRoot_Frame, text="Status", width=20).pack(side="left", padx=10, anchor="w")
                    if timeLeftDifference.get() == 0:
                        progress_label[0] = cal.Label(statusRoot_Frame, text="PROCESSING", width=20, foreground="green")
                        progress_label[0].pack(side="left", padx=10, anchor="w")
                    else:
                        progress_label[0] = cal.Label(statusRoot_Frame, text="IN PROGRESS", width=20, foreground="blue")
                        progress_label[0].pack(side="left", padx=10, anchor="w")
                    pocketRoot_Frame.pack()
                    patient_idRoot_Frame.pack()
                    letfTimeRoot_Frame.pack()
                    statusRoot_Frame.pack()

    upperFrame.pack(pady=2)

    def refreshResultData():
        countsize = 1
        callData_Test_Number_1 = dbh.cursor()
        callData_Test_One_1 = dbh.cursor()
        dbh.commit()
        callData_Test_Number_1.execute("SELECT pocket_id FROM pocket_state  WHERE state = 0")
        for count_1Plus in callData_Test_Number_1.fetchall():
            countsize += 1
            pocket_stateCountNumber.set(count_1Plus[0])
            callData_Test_One_1.execute(
                "SELECT timestampdiff(second,now(),pd.endTime) as durationLeft,sa.accession_number,pd.dish_id,pd.sample_id FROM samples sa INNER JOIN petri_dish pd on sa.sample_id=pd.sample_id where pd.dish_id =" + str(
                    pocket_stateCountNumber.get()) + " and state =1 ")
            for cnt_1 in range(pocket_stateCount.get()):
                for countPlus, labelDict in zip(callData_Test_One_1.fetchall(), patient_Ids):
                    try:
                        patient_Ids[countsize]["text"] = str(countPlus[0])
                    except:
                        pass

    home_resultBtn = cal.Button(resultRoot, text="Go Back", padding=10, width=23, command=resultRoot.destroy)
    home_resultBtn.pack()


# noinspection PyUnusedLocal,PyShadowingNames
def scanPatientID():
    global scanPatientID_view
    scanPatientID_view = Toplevel(base)
    scanPatientID_view.title("Incubator ")
    scanPatientID_view.lift(base)
    cal.Label(scanPatientID_view, text="SCAN PATIENT BAR CODE", background="white").pack(pady=10)
    scan_frame = cal.Frame(scanPatientID_view, padding=20, relief=SOLID)
    scanPatientID_view.config(background="white")

    def clear_id():
        scan_entryField.delete(0, "end")
        scan_entryField.focus()

    def getscanned():
        dbh.commit()
        getBacteria.execute("select bacteria_name from bacteria")
        bacteria_list = getBacteria.fetchall()
        bacteria_list1.set(bacteria_list)

        list_sample = list()
        for row in bacteria_list:
            list_sample.append(str(row[0]))

        patient_id.set(scan_entryField.get()[:-1])
        if patient_id.get() == '':
            scan_entryField.focus()

        else:
            scan_entryField.delete(0, "end")
            scan_entryField.focus()
            global en_samplewindow
            global scanPatientID_view
            scanPatientID_view.destroy()
            en_samplewindow = Toplevel(base)
            en_samplewindow.title("Incubator")
            en_samplewindow.lift(base)
            en_samplewindow.config(background="white")
            frame_b1 = cal.Frame(en_samplewindow, padding=20, relief=SOLID)
            frame_b2 = cal.Frame(frame_b1)

            def isolate_selected(event):
                serch_1.delete(0, 'end')
                try:
                    serch_1.insert(0, event.widget.get(event.widget.curselection()))
                    isolate_name.set(event.widget.get(event.widget.curselection()))
                except:
                    pass

            # noinspection PyShadowingNames
            def serch_isolate(val):
                value = val.widget.get()
                value = value.strip().lower()
                if value == '':
                    data = list_sample

                else:
                    data = []
                    for item in list_sample:
                        if value in item.lower():
                            data.append(item)

                listbox_update(data)

            def listbox_update(data):
                isolate_list.delete(0, 'end')
                data = sorted(data, key=str.lower)
                for item in data:
                    isolate_list.insert('end', item)

            # noinspection PyGlobalUndefined
            def isolate_listUpdater():
                global listbox_update
                dbh.commit()
                getBacteria.execute("select bacteria_name from bacteria")
                bacteria_list = getBacteria.fetchall()
                bacteria_list1.set(bacteria_list)

                list_sample = list()
                for row in bacteria_list:
                    def listbox_update(data):
                        isolate_list.delete(0, 'end')
                        data = sorted(data, key=str.lower)
                        for item in data:
                            isolate_list.insert('end', item)

                    list_sample.append(str(row[0]))
                listbox_update(list_sample)

            def add_newBacteria():
                global addRoot
                addRoot = Toplevel(base, background="#FFF")
                top_head = cal.Label(addRoot, text="ADD NEW ISOLATE")
                top_head.pack(pady=20)
                addFrame = cal.Frame(addRoot, relief=SOLID, padding=30)
                add_value = StringVar()

                # noinspection PyShadowingNames
                def addQuery():
                    global counter
                    query = dbh.cursor()
                    add_value.set(addInput.get())
                    dbh.commit()
                    query.execute("SELECT COUNT(*) FROM bacteria WHERE bacteria_name='" + add_value.get() + "'")
                    for count in query.fetchall():
                        counter = count[0]
                    if counter == 0:
                        try:
                            query.execute("INSERT INTO bacteria (bacteria_name) VALUES ('" + add_value.get() + "')")
                            dbh.commit()
                            print("Bacteria added")
                            isolate_listUpdater()
                            getBacteria.execute("select bacteria_name from bacteria")
                            bacteria_list = getBacteria.fetchall()
                            bacteria_list1.set(bacteria_list)
                            top_head.config(text="[" + add_value.get() + "] HAS BEEN ADDED")
                            add_value.set("")

                        except:
                            dbh.rollback()
                            print("Faied to add")
                            top_head.config(text="PROCESS FAILED", foreground="red")

                    else:
                        print("Bacteria Aready exist")
                        top_head.config(text="[" + add_value.get() + "] ALREADY EXISTS IN THE SYSTEM")
                        add_value.set("")

                def clear_add_Input(e):
                    addInput.delete(0, 'end')

                addInput = cal.Entry(addFrame, width=32, font=("SEGOEUI", 15), justify="center")
                addInput.insert(0, "Enter isolate name here")
                addInput.bind("<FocusIn>", lambda event: clear_add_Input(event))
                addInput.pack(ipady=10)
                optFrame = cal.Frame(addFrame)
                cal.Button(optFrame, text="ADD", padding=15, width=12, command=addQuery).pack(pady=10, padx=10,
                                                                                              side=LEFT)
                cal.Button(optFrame, text="CANCEL", padding=15, width=12, command=addRoot.destroy).pack(pady=10,
                                                                                                        padx=10,
                                                                                                        side=LEFT)
                optFrame.pack()
                cal.Button(addFrame, text="CLEAR", padding=15, width=30, command=lambda: clear_add_Input(0)).pack()

                addFrame.pack()

            def petriDish_selection():
                if isolate_name.get() == '':
                    print()
                else:
                    global petri_dish_view
                    petri_dish_view = Toplevel(base, background="#FFF")
                    petri_dish_frame = cal.Frame(petri_dish_view, relief=SOLID, padding=20)
                    petri_dish_frameOpt = cal.Frame(petri_dish_frame)
                    cal.Label(petri_dish_view,
                              text="NUMBER OF PETRI DISHES | ID [" + patient_id.get() + "]").pack(
                        pady=10)

                    def dish_count_selected(param):
                        dbh.commit()
                        pocket_check = dbh.cursor()
                        pocket_check.execute("SELECT COUNT(*) FROM pocket_state WHERE state=1")
                        for count in pocket_check.fetchall():
                            pdishNumber.set(count[0])

                        if pdishNumber.get() < 1:
                            pdishNumber.set(0)
                            pockets_full = Toplevel(base, background="#FFF")
                            pockets_full_Frame = cal.Frame(pockets_full, padding=30, relief=SOLID)
                            Label(pockets_full_Frame,
                                  text="ALL POCKETS ARE CURRENTLY IN USE,\n  WAIT FOR ONE TEST TO FINISH.").pack(
                                pady=20)

                            cal.Button(pockets_full_Frame, text="Go Back", padding=20, width=20,
                                       command=pockets_full.destroy).pack()
                            pockets_full_Frame.pack(pady=10)

                        else:
                            imageFilename = None

                            def moveMotorToCameraPos(e):
                                global imageFilename

                                imageFilename = imglocationhome + "tryImg.png"
                                imgpath = coordinates = images = masks = None
                                waitTimer = 0
                                processBtnScanner.pack_forget()

                                def locadiscsRun():

                                    global waitTimer
                                    global imgpath, coordinates, images, masks, abx_result_dictionary
                                    imgpath, coordinates, images, masks = locatediscs(imageFilename)
                                    abx_result_dictionary = discsearcher(featurefinder(images, masks))

                                    waitTimer = 1

                                locadiscsThread = threading.Thread(target=locadiscsRun, daemon=True)
                                locadiscsThread.start()

                                def waitTimeRunner():
                                    base.after(1000, waitTimeRunner)
                                    if locadiscsThread.isAlive():
                                        pass
                                    else:
                                        try:
                                            process_label["text"] = "PROCESSING COMPLETED"
                                            discidentifierMethodThread = threading.Thread(target=discidentifierMethod)
                                            discidentifierMethodThread.start()
                                        except:
                                            pass

                                waitTimeRunner()

                                process_label["text"] = "WAIT A MOMENT WHILE PROCESSING"

                                def change_color():
                                    try:
                                        current_color = process_label.cget("foreground")
                                        next_color = "white" if current_color == "black" else "black"
                                        process_label.config(foreground=next_color)
                                        base.after(1000, change_color)
                                    except:
                                        pass

                                change_color()

                            def discidentifierMethod():
                                global dish_allocation, abx_result_dictionary
                                dish_allocation.destroy()
                                img_scanned.set(imgpath)
                                global imageDisplay
                                global imageDisplayScaled

                                imageDisplay = PhotoImage(file=img_scanned.get())
                                imageDisplayScaled = imageDisplay.subsample(1, 2)
                                global pocket_root

                                pocket_root = Toplevel(base, background="#FFF")
                                pocket_frame = cal.Frame(pocket_root, relief=SOLID, padding=10)
                                cal.Label(pocket_root,
                                          text="ANTIBIOTIC IDENTIFICATION | ID #[" + patient_id.get() + "]").pack(
                                    pady=10)
                                abx_list = dbh.cursor()
                                dbh.commit()
                                abx_list.execute("SELECT * FROM antibiotics")

                                def isolate_selectedToChange(param, param2):
                                    abx_name = StringVar()
                                    isolateNamePassed = StringVar()
                                    isolateNamePassed.set("")

                                    def abx_selected(event):
                                        try:
                                            serch_abx.delete(0, 'end')
                                            serch_abx.insert(0, event.widget.get(event.widget.curselection()))
                                            abx_name.set(event.widget.get(event.widget.curselection()))
                                        except:
                                            pass

                                    def serch_abxMethod(val):
                                        value_abx = val.widget.get()
                                        value_abx = value_abx.strip().lower()
                                        if value_abx == '':
                                            data = list_sample_abx

                                        else:
                                            data = []
                                            for item in list_sample_abx:
                                                if value_abx in item.lower():
                                                    data.append(item)

                                        listbox_update_abx(data)

                                    def listbox_update_abx(data):
                                        abx_list_Listbox.delete(0, 'end')
                                        data = sorted(data, key=str.lower)
                                        for item in data:
                                            abx_list_Listbox.insert('end', item)

                                    def bacteria_change():
                                        abx_root.destroy()
                                        param["text"] = "Disc " + str(param2) + "." + abx_name.get()
                                        if param2:
                                            abx_result_dictionary[param2] = abx_name.get().split("[")[0]
                                        else:
                                            abx_result_dictionary[param2] = "No matching antibiotics Discs found"

                                    abx_root = Toplevel(base, background="#FFF")
                                    abxFrame = cal.Frame(abx_root, relief=SOLID, padding=20)
                                    cal.Label(abx_root,
                                              text="CHOOSE ANTIBIOTIC FOR  DISK." + str(param2) + "").pack(
                                        pady=10)
                                    serch_abx = cal.Entry(abxFrame, width=30, font=("SEGOEUI", 18))
                                    serch_abx.pack(ipady=10, pady=10)
                                    abx_list_Listbox = Listbox(abxFrame, width=30, font=("SEGOEUI", 18))
                                    listbox_update_abx(list_sample_abx)
                                    abx_list_Listbox.bind("<<ListboxSelect>>", abx_selected)
                                    serch_abx.bind("<KeyRelease>", serch_abxMethod)
                                    abx_list_Listbox.pack()
                                    cal.Button(abxFrame, text="Change", width=30, padding=30,
                                               command=bacteria_change).pack(pady=10)
                                    cal.Button(abxFrame, text="Cancel", width=30, padding=30,
                                               command=abx_root.destroy).pack(pady=10)
                                    serch_abx.pack()
                                    abx_list_Listbox.pack()
                                    abxFrame.pack()

                                isolate_identification = {}
                                params = {}
                                for isolates in abx_result_dictionary:
                                    isolate_identification[isolates] = cal.Label(pocket_frame,
                                                                                 text="Disc " + str(
                                                                                     isolates) + "." +
                                                                                      abx_result_dictionary[
                                                                                          isolates])
                                    isolate_identification[isolates].pack(anchor='w')
                                    isolate_identification[isolates].bind("<Button-1>",
                                                                          lambda eventhandle, param=isolates,
                                                                                 param2=
                                                                                 isolate_identification[
                                                                                     isolates]: isolate_selectedToChange(
                                                                              param2, param))

                                def saveTestData():
                                    global pocket_root
                                    global imageFilename
                                    filelocationhome = "assets/antibiotics/"
                                    discwriter(abx_result_dictionary, featurefinder(images, masks),
                                               filelocationhome)
                                    global rootConfirm

                                    try:
                                        insert_into_patientsTable = dbh.cursor()
                                        insert_into_petri_dishTable = dbh.cursor()
                                        update_pocket_stateTable = dbh.cursor()
                                        add_abx_todiscsTable = dbh.cursor()
                                        time_stample = StringVar()
                                        timelimitcalled = IntVar()
                                        calltimelimit = dbh.cursor()
                                        calltimelimit.execute(
                                            "SELECT timelimit FROM bacteria WHERE bacteria_name = '" + str(
                                                isolate_name.get()) + "'")
                                        for timelimit in calltimelimit.fetchall():
                                            timelimitcalled.set(timelimit[0])
                                        finishDate = datetime.datetime.now() + datetime.timedelta(
                                            hours=timelimitcalled.get())
                                        time_stample.set(finishDate.strftime("%Y-%m-%d %H:%M:%S"))
                                        insert_into_patientsTable.execute(
                                            "INSERT INTO samples (accession_number,bacteria_id) VALUES (" + patient_id.get() + ",(SELECT bacteria_id FROM bacteria WHERE bacteria_name='" + isolate_name.get() + "'))")
                                        insert_into_petri_dishTable.execute(
                                            "INSERT INTO petri_dish (dish_id,sample_id,endTime) VALUES (" + pdishNumberSet.get() + ",(SELECT sample_id FROM samples WHERE accession_number='" + patient_id.get() + "' ),'" + time_stample.get() + "')")
                                        update_pocket_stateTable.execute(
                                            "UPDATE pocket_state SET state=0 WHERE  pocket_id =" + pdishNumberSet.get() + "")
                                        countAbx = 0
                                        for _ in abx_result_dictionary:
                                            countAbx += 1
                                            add_abx_todiscsTable.execute(
                                                "INSERT INTO discs (abx_id,dish_id,sample_id) VALUES ((SELECT abx_id FROM antibiotics WHERE abx_name ='" +
                                                abx_result_dictionary[
                                                    countAbx] + "')," + pdishNumberSet.get() + ",(SELECT sample_id FROM samples WHERE accession_number='" + patient_id.get() + "' ))")
                                        dbh.commit()

                                        sample_idcall = dbh.cursor()
                                        sample_idcall.execute(
                                            "SELECT sample_id FROM samples WHERE accession_number='" + str(
                                                patient_id.get()) + "' LIMIT 1")
                                        for myId in sample_idcall.fetchall():
                                            # noinspection PyTypeChecker
                                            shutil.copy(imageFilename, imglocationhome + str(myId[0]) + ".png")

                                        finishBtn["state"] = "disabled"
                                        finishBtn["text"] = "TEST IN PROGRESS ..."
                                        cancelBtn2["text"] = "Close"

                                        def closeProgress(param_):
                                            rootConfirm.destroy()
                                            pocket_root.destroy()

                                        cancelBtn2.bind("<Button-1>", closeProgress)

                                    except Exception:
                                        dbh.rollback()
                                        finishBtn["state"] = "disabled"
                                        finishBtn["text"] = "PROCESS EXECUTION FAILED"
                                        cancelBtn2["text"] = "RETRY"

                                        def closeProgress(param_):
                                            rootConfirm.destroy()
                                            pocket_root.destroy()

                                        cancelBtn2.bind("<Button-1>", closeProgress)

                                def confirm_button():
                                    global rootConfirm
                                    rootConfirm = Toplevel(base, background="#FFF")
                                    conformFrame = cal.Frame(rootConfirm, relief=SOLID, padding=30)
                                    cal.Label(rootConfirm,
                                              text="FINALISING PROCESS ON ID #[" + patient_id.get() + "]").pack(
                                        pady=10)
                                    cal.Label(conformFrame, text="Isolate Name : " + isolate_name.get()).pack(
                                        anchor="w")
                                    cal.Label(conformFrame, text="Antibiotics Chosen").pack(pady=1, anchor="w")
                                    abx_list_1 = dbh.cursor()
                                    dbh.commit()
                                    abx_list_1.execute("SELECT * FROM antibiotics")
                                    abxCounter = 0
                                    for _ in abx_result_dictionary:
                                        abxCounter += 1
                                        cal.Label(conformFrame, text=str(abxCounter) + "." + str(
                                            abx_result_dictionary[abxCounter])).pack(anchor='w')

                                    # cal.Label(conformFrame,   text="Start Time : " + datetime.datetime.now().strftime("%H:%M %p")).pack(anchor="w")

                                    # cal.Label(conformFrame,
                                    #       text="Start Time : " + datetime.date.today().strftime(
                                    #         "%B %W, %Y")+
                                    # " | " + datetime.datetime.now().strftime("%H:%M %p")).pack(anchor="w")
                                    global finishDateTime
                                    finishDateTime = datetime.datetime.now() + datetime.timedelta(hours=24)
                                    global finishBtn
                                    global cancelBtn2

                                    cal.Label(conformFrame,
                                              text="Finishes On : " + finishDateTime.strftime(
                                                  "%a, %B %d, %Y")).pack(
                                        anchor="w")

                                    # cal.Label(conformFrame, image=imageDisplayScaled).pack(pady=5)
                                    finishBtn = cal.Button(conformFrame, text="Finish", width=30, padding=20,
                                                           command=saveTestData
                                                           )
                                    finishBtn.pack(pady=10)
                                    cancelBtn2 = cal.Button(conformFrame, text="Cancel", width=30, padding=20,
                                                            command=rootConfirm.destroy)
                                    cancelBtn2.pack(pady=10)
                                    conformFrame.pack()

                                def antibioticsCheck():
                                    countDic = 0
                                    flagAbx = 0
                                    for _ in abx_result_dictionary:
                                        countDic += 1
                                        if abx_result_dictionary[countDic] == "No matching antibiotic Discs found":
                                            flagAbx = 1

                                    if flagAbx == 1:
                                        print("Invalid ABX")
                                        # proceedButton["text"] = "Invalid ABX"
                                    else:
                                        confirm_button()

                                imge = Image.open(img_scanned.get())
                                imge = imge.resize((400, 400), Image.ANTIALIAS)
                                imageDisplay = ImageTk.PhotoImage(imge)
                                img_scanned_label = cal.Label(pocket_frame, image=imageDisplay, compound=LEFT)
                                img_scanned_label.pack()

                                # print(ImagesPath.get() + patient_id.get() + patient_id.get() + ".jpg")
                                def gotopetriDish_selection():
                                    petriDish_selection()
                                    pocket_root.destroy()

                                bottom_confirm = cal.Frame(pocket_root)
                                proceedButton = cal.Button(bottom_confirm, text="Confirm", width=15, padding=11,
                                                           command=antibioticsCheck)
                                cancelBtn = cal.Button(bottom_confirm, text="Cancel",
                                                       command=gotopetriDish_selection,
                                                       width=15, padding=11)
                                # isolate_postion.pack(pady=10)
                                proceedButton.pack(pady=1, side=LEFT)
                                cancelBtn.pack(pady=1, side=LEFT)
                                pocket_frame.pack()
                                bottom_confirm.pack()

                            petri_dish_count.set(param)
                            pocket_number = dbh.cursor()
                            pocket_number.execute(
                                "SELECT pocket_id FROM pocket_state  WHERE state = 1 ORDER BY state DESC LIMIT 1")
                            for count_2 in pocket_number.fetchall():
                                pdishNumberSet.set(count_2[0])

                            global dish_allocation
                            global en_samplewindow
                            global petri_dish_view
                            en_samplewindow.destroy()
                            petri_dish_view.destroy()

                            dish_allocation = Toplevel(base, bg="#FFF")
                            petri_dish_all = cal.Frame(dish_allocation, padding=20, relief=SOLID)
                            cal.Label(dish_allocation,
                                      text="PLACE THE PETRI DISH INTO THE POCKET " + str(pdishNumberSet.get())).pack(
                                pady=10)

                            def gobackTopetriDish_selection():
                                petriDish_selection()
                                dish_allocation.destroy()

                            cal.Label(petri_dish_all, text="Patient ID #[" + patient_id.get() + "]").pack(
                                anchor="w", pady=2)
                            cal.Label(petri_dish_all, text="Bacteria [" + isolate_name.get() + "]").pack(anchor="w",
                                                                                                         pady=2)
                            petri_dish_all.pack()
                            processBtnScanner = cal.Button(petri_dish_all, text="Proceed", width=29, padding=17,
                                                           command=lambda: moveMotorToCameraPos(0))
                            processBtnScanner.pack(pady=3, padx=5)
                            cal.Button(petri_dish_all, text="Cancel", width=29, padding=17,
                                       command=gobackTopetriDish_selection).pack(pady=3, padx=5)
                            process_label = Label(petri_dish_all, text="", foreground="white",
                                                  background="#fff", font=("SEGOE UI", 15))
                            process_label.pack()
                        pass

                    cal.Button(petri_dish_frameOpt, text="1 PETRI DISH", width=13, padding=20,
                               command=lambda: dish_count_selected(1)).pack(pady=10, side=LEFT)
                    cal.Button(petri_dish_frameOpt, text="2 PETRI DISHES", state="disabled",
                               command=lambda: dish_count_selected(2), width=13, padding=20).pack(pady=10, side=LEFT)
                    petri_dish_frameOpt.pack()
                    cal.Button(petri_dish_frame, text="CANCEL", width=30, padding=20,
                               command=petri_dish_view.destroy).pack()
                    petri_dish_frame.pack()

            cal.Label(en_samplewindow, text="CHOOSE ISOLATE  | ID [" + patient_id.get() + "]").pack(pady=10)
            serch_1 = cal.Entry(frame_b1, width=35, font=("SEGOE UI", 15))
            serch_1.pack(ipady=10, pady=10)
            isolate_list = Listbox(frame_b1, width=35, font=("SEGOE UI", 15))
            listbox_update(list_sample)

            isolate_list.bind("<<ListboxSelect>>", isolate_selected)
            serch_1.bind("<KeyRelease>", serch_isolate)
            isolate_list.pack()

            def destroyIso():
                isolate_name.set("")
                en_samplewindow.destroy()

            cal.Button(frame_b2, text="CANCEL", padding=15, width=14, command=destroyIso).pack(pady=10, padx=10,
                                                                                               side=LEFT)
            cal.Button(frame_b2, text="PROCCED", padding=15, width=14, command=petriDish_selection).pack(pady=10,
                                                                                                         padx=10,
                                                                                                         side=LEFT)
            frame_b2.pack()
            cal.Button(frame_b1, text="ADD NEW ISOLATE", width=33, padding=15, command=add_newBacteria).pack()
            frame_b1.pack()

    scan_entryField = cal.Entry(scan_frame, textvariable=pa_id.get(), width=34, font=("SEGOEUI", 14), justify="center")
    scan_entryField.pack(ipady=9)
    scan_entryField.focus()
    optButtons = cal.Frame(scan_frame)
    cal.Button(optButtons, text="CANCEL", width=12, padding=20, command=scanPatientID_view.destroy).pack(padx=10,
                                                                                                         pady=10,
                                                                                                         side=LEFT)
    cal.Button(optButtons, text="PROCEED", width=12, padding=20, command=getscanned).pack(pady=10, padx=10, side=LEFT)

    optButtons.pack()
    cal.Button(scan_frame, text="CLEAR", width=30, padding=20, command=clear_id).pack()
    scan_frame.pack()


# noinspection PyUnusedLocal,PyShadowingNames
def compledTests():
    pocket_stateCount = IntVar()
    completedTestsRoot = Toplevel(base, background="#FFF")
    upperFrame = cal.Frame(completedTestsRoot, padding=5)
    test_in_progress = dbh.cursor()
    dbh.commit()
    test_in_progress.execute("SELECT COUNT(*) FROM petri_dish WHERE state=3")
    for count in test_in_progress.fetchall():
        pocket_stateCount.set(count[0])

    sample_dishes = IntVar()
    callData_Test_Number = dbh.cursor()
    callData_Test_One = dbh.cursor()
    assesionNumber = StringVar()

    if pocket_stateCount.get() == 0:

        pocketRoot_Frame = cal.Frame(upperFrame, padding=15, relief=SOLID)
        cal.Label(completedTestsRoot, text="NO COMPLETED TESTS AT THE MOMENT", padding=20, relief=SOLID).pack(
            pady=20)
        pocketRoot_Frame.pack()


    elif pocket_stateCount.get() > 0:

        completed_label = {}
        countDone = 0
        callData_Test_Number.execute("SELECT sample_id FROM petri_dish  WHERE state = 3")
        for count_1 in callData_Test_Number.fetchall():
            sample_dishes.set(count_1[0])
            callData_Test_One.execute(
                "SELECT sa.accession_number,pd.sample_id FROM samples sa INNER JOIN petri_dish pd on sa.sample_id=pd.sample_id where pd.sample_id =" + str(
                    sample_dishes.get()) + " and state =3")
            for count in callData_Test_One.fetchall():
                countDone += 1
                assesionNumber.set(str(count[1]))
                cal.Frame(upperFrame).pack(pady=5)
                pocketRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                patient_idRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                cal.Label(patient_idRoot_Frame, text="Assesion #").pack(side="left", padx=10,
                                                                                        anchor="w")
                cal.Label(patient_idRoot_Frame, text=str(count[0]),width=10).pack(side="left", padx=10, anchor="w")
                completed_label[countDone] = cal.Label(patient_idRoot_Frame, text="VIEW", width=5,
                                                       foreground="green")
                completed_label[countDone].pack(side="left", padx=10, anchor="w")

                # noinspection PyShadowingNames
                def singleTestProgressing(val):
                    sample_id.set(val)
                    newImageFile = None

                    global imageDisplayScaled
                    global imgDisplay

                    singleTestdbobject = dbh.cursor()
                    dbh.commit()
                    singleTestdbobject.execute(
                        "SELECT imagelocation FROM images WHERE state=3 AND sample_id= " + str(sample_id.get()))
                    for imgloc in singleTestdbobject.fetchall():
                        newImageFile = imgloc[0]

                    discs = {}
                    sampleBuild.execute("SELECT * from zones where sample_id =" + str(sample_id.get()))
                    count = 1
                    for a2 in sampleBuild.fetchall():
                        val = a2[1].split(",")[0]
                        val2 = a2[1].rsplit(",")[-1]
                        discs[count] = ((int(val[1:])), (int(val2[:-1])))

                        count += 1

                    imgDisplay = PhotoImage(file=newImageFile)
                    B_name = StringVar()
                    singleRoot = Toplevel(base, background="#FFF")
                    callId = dbh.cursor()
                    callId.execute(
                        "SELECT sa.accession_number, ba.bacteria_name FROM samples sa inner join bacteria ba on sa.bacteria_id = ba.bacteria_id where sa.sample_id=" + str(
                            sample_id.get()) )
                    for p_id in callId.fetchall():
                        cal.Label(singleRoot,
                                  text="PATIENT ID[" + str(p_id[0]) + "] BACTERIA [" + str(p_id[1]) + "]").pack(
                            pady=10)
                    frame_top = cal.Frame(singleRoot, padding=5, relief=SOLID)
                    cal.Label(frame_top, text="Antibiotics", width=21).pack(side="left", padx=3, anchor="w")
                    cal.Label(frame_top, text="Dose", width=5).pack(side="left", padx=3, anchor="w")
                    cal.Label(frame_top, text="MM", width=4).pack(side="left", padx=3, anchor="w")
                    cal.Label(frame_top, text="S>", width=4).pack(side="left", padx=3, anchor="w")
                    cal.Label(frame_top, text="R<", width=4).pack(side="left", padx=3, anchor="w")
                    cal.Label(frame_top, text="Inter", width=4).pack(side="left", padx=3, anchor="w")
                    frame_top.pack()

                    callData_TestDone = dbh.cursor()
                    dbh.commit()
                    abx_result_labelSwitch = {}
                    abx_result_labeldec = {}
                    callData_TestDone.execute(
                        "SELECT an.abx_name , an.abx_content, ds.diameter, an.sus, an.res , an.abx_code FROM samples sa INNER JOIN petri_dish pd INNER JOIN discs ds INNER JOIN antibiotics an on sa.sample_id=pd.sample_id and ds.abx_id = an.abx_id and sa.sample_id=ds.sample_id where sa.sample_id=" + str(
                            sample_id.get()) + " and state =3")
                    counter_abx = 0
                    for conterPlus in callData_TestDone.fetchall():
                        counter_abx += 1
                        B_name.set(conterPlus[0])
                        data_m = (B_name.get()[:12] + ".. ") if len(B_name.get()) > 12 else B_name.get()
                        frame_top = cal.Frame(singleRoot, padding=5, relief=SOLID)
                        abx_result_label[counter_abx] = cal.Label(frame_top,
                                                                  text=str(counter_abx) + ". " + str(
                                                                      data_m) + "[" + str(conterPlus[5]) + "]",
                                                                  width=21)
                        abx_result_label[counter_abx].pack(side="left", padx=3, anchor="w")
                        abx_result_label[counter_abx] = cal.Label(frame_top, text=str(conterPlus[1]), width=5)
                        abx_result_label[counter_abx].pack(side="left", padx=3, anchor="w")
                        abx_result_labelSwitch[counter_abx] = cal.Label(frame_top, text=str(conterPlus[2]),
                                                                        width=4)
                        abx_result_labelSwitch[counter_abx].pack(side="left", padx=3, anchor="w")
                        abx_result_label[counter_abx] = cal.Label(frame_top, text=str(conterPlus[3]), width=4)
                        abx_result_label[counter_abx].pack(side="left", padx=3, anchor="w")
                        abx_result_label[counter_abx] = cal.Label(frame_top, text=str(conterPlus[4]), width=4)
                        abx_result_label[counter_abx].pack(side="left", padx=3, anchor="w")
                        if conterPlus[2] >= conterPlus[3]:
                            abx_result_labeldec[counter_abx] = cal.Label(frame_top, text="S", width=4)
                            abx_result_labeldec[counter_abx].pack(side="left", padx=3, anchor="w")
                        elif conterPlus[2] < conterPlus[4]:
                            abx_result_labeldec[counter_abx] = cal.Label(frame_top, text="R", width=4)
                            abx_result_labeldec[counter_abx].pack(side="left", padx=3, anchor="w")
                        else:
                            abx_result_labeldec[counter_abx] = cal.Label(frame_top, text="I", width=4)
                            abx_result_labeldec[counter_abx].pack(side="left", padx=3, anchor="w")

                        frame_top.pack()

                    # print(abx_result_label)

                    def labelUpdate():
                        callData_TestDoneRefresh = dbh.cursor()
                        dbh.commit()
                        counter_abx_1 = 0
                        callData_TestDoneRefresh.execute(
                            "SELECT ds.diameter, an.sus, an.res FROM samples sa INNER JOIN petri_dish pd INNER JOIN discs ds INNER JOIN antibiotics an on sa.sample_id=pd.sample_id and ds.abx_id = an.abx_id and sa.sample_id=ds.sample_id where sa.sample_id=" + str(
                                sample_id.get()) + " and state =3")
                        for conterPlusPlus in callData_TestDoneRefresh.fetchall():
                            counter_abx_1 += 1
                            abx_result_labelSwitch[counter_abx_1]["text"] = str(conterPlusPlus[0])
                            if conterPlusPlus[0] >= conterPlusPlus[1]:
                                abx_result_labeldec[counter_abx_1]["text"] = "S"
                            elif conterPlusPlus[0] < conterPlusPlus[2]:
                                abx_result_labeldec[counter_abx_1]["text"] = "R"
                            else:
                                abx_result_labeldec[counter_abx_1]["text"] = "I"

                    # noinspection PyUnusedLocal,PyShadowingNames,PyTypeChecker
                    def editResult(a):

                        global imageDisplayScaled
                        global imgDisplay

                        editRoot = Toplevel(base, background="#FFF")
                        callId = dbh.cursor()
                        callId.execute(
                            "SELECT * FROM samples sa inner join bacteria ba on sa.bacteria_id = ba.bacteria_id where sa.sample_id=" + str(
                                sample_id.get()) + " limit 1")
                        for patient_id in callId.fetchall():
                            cal.Label(editRoot, text="EDIT RESULTS FOR PATIENT ID #[" + str(patient_id[1]) + "]").pack(
                                pady=10)

                        # noinspection PyShadowingNames
                        def circle_adjust(disc, plus_minus):

                            valInt = IntVar()
                            valInt.set(disc)

                            global _edit
                            global imgDisplayII
                            global edit_BoxValue
                            global imageDisplayScaled
                            inProgress = Toplevel(base)
                            cal.Label(inProgress, text="Executing please wait...").pack()
                            zone_distances = []
                            counter = 0
                            counterPlus = 1
                            dbh.commit()

                            singleTestdbobject.execute(
                                "SELECT diameter FROM discs WHERE sample_id= " + str(sample_id.get()))
                            for diam in singleTestdbobject.fetchall():
                                zone_distances.append(diam[0] / 0.0307692)
                                counter += 1
                                counterPlus += 1

                            old_img = imglocationhome + str(sample_id.get()) + ".png"
                            zone_distances = zoneadjuster(zone_distances, valInt.get(), plus_minus, 1)
                            circledrawer(old_img, zone_distances, discs)
                            # print(zone_distances)

                            arrayD = zone_distances.copy()
                            arrayDist = zone_distances.copy()

                            arrayDist[:] = [x * 0.0307692 for x in arrayD]
                            count = -1
                            count_12 = 0
                            vals = {}
                            insertIntoDiameter = dbh.cursor()
                            checkAbx = dbh.cursor()
                            checkAbx.execute(
                                "SELECT disc_id  FROM discs WHERE sample_id =" + str(sample_id.get()) + "")

                            for _ in arrayDist:
                                count += 1
                                count_12 += 1
                                arr = round(arrayDist[count])
                                vals[count_12] = arr

                            count_12 = 0
                            count = -1
                            valueInsert = StringVar()
                            for abx_sample_id, coount in zip(vals, checkAbx.fetchall()):
                                count_12 += 1
                                count += 1

                                valueInsert.set(str(vals[count_12]))

                                dbh.commit()
                                try:
                                    insertIntoDiameter.execute(
                                        "UPDATE discs set diameter=" + str(
                                            valueInsert.get()) + " WHERE sample_id=" + str(
                                            sample_id.get()) + " and disc_id =" + str(coount[0]) + "")
                                    dbh.commit()
                                except:
                                    print("Failed to insert")
                                    dbh.rollback()

                            inProgress.destroy()
                            shutil.copy(imglocationhome + "newzones" + str(sample_id.get()) + ".png",
                                        newImageFile)
                            imgDisplayII = PhotoImage(
                                file=imglocationhome + "newzones" + str(sample_id.get()) + ".png")
                            labelUpdate()
                            imageDisplayScaled = imgDisplayII.subsample(2, 2)
                            labelUpdate()
                            photo_edit.config(image=imgDisplayII)
                            _editLabel.config(image=imageDisplayScaled)

                        try:
                            imgDisplay = PhotoImage(file=imglocationhome + "newzones" + str(sample_id.get()) + ".png")
                        except:
                            imgDisplay = PhotoImage(file=imglocationhome + "zonesfound" + str(sample_id.get()) + ".png")
                        photo_edit = cal.Label(editRoot, image=imgDisplay)
                        photo_edit.pack()

                        # base.after(1000, increaing_circle_loop)
                        buttons_Frame = cal.Frame(editRoot)

                        increaseDistance = cal.Button(buttons_Frame, text="+", width=3)
                        increaseDistance.pack(side=LEFT, padx=2)
                        reduceDistance = cal.Button(buttons_Frame, text="-", width=3)
                        reduceDistance.pack(side=LEFT, padx=2)
                        buttons_Frame.pack()

                        discsValue = StringVar()

                        # print("we here" + str((abx_result_dictionary)))
                        if abx_result_dictionary_LengthGlobal.get() == 6:
                            discsValue.set("1 2 3 4 5 6")
                        else:
                            discsValue.set("1 2 3 4 5 6 7")

                        edit_BoxValue = cal.Combobox(editRoot, width=30, values=discsValue.get(),
                                                     state="readonly")
                        increaseDistance.bind("<Button-1>",
                                              lambda event: circle_adjust(edit_BoxValue.get(), True))
                        reduceDistance.bind("<Button-1>", lambda event: circle_adjust(edit_BoxValue.get(), False))
                        edit_BoxValue.current("1")

                        edit_BoxValue.pack(pady=10, ipady=3)

                        frame_edit = cal.Frame(editRoot, padding=3)
                        approveBtn_result = cal.Button(frame_edit, text="Confirm",
                                                       width=10, padding=10, command=editRoot.destroy)
                        cancelBtn_result = cal.Button(frame_edit, text="Cancel", width=10, padding=10,
                                                      command=editRoot.destroy)
                        approveBtn_result.pack(side=LEFT)
                        # cancelBtn_result.pack(side=LEFT)
                        frame_edit.pack()

                    imageDisplayScaled = imgDisplay.subsample(2, 2)
                    _editLabel = cal.Label(singleRoot, image=imageDisplayScaled)
                    _editLabel.bind("<Button-1>", editResult)
                    _editLabel.pack()
                    lower_frame = cal.Frame(singleRoot, padding=5)
                    approveBtn = cal.Button(lower_frame, text="Approve", command=singleRoot.destroy, padding=20,
                                            width=20)
                    cal.Button(lower_frame, text="Cancel", padding=20, command=singleRoot.destroy,
                               width=20)
                    approveBtn.pack()
                    lower_frame.pack()

                completed_label[countDone].bind("<Button-1>",
                                                lambda event, val=count[1]: singleTestProgressing(val))
                pocketRoot_Frame.pack()
                patient_idRoot_Frame.pack()
                upperFrame.pack(pady=2)

    home_resultBtn = cal.Button(completedTestsRoot, text="Go Back", padding=10, width=23,
                                command=completedTestsRoot.destroy)
    home_resultBtn.pack()


# noinspection PyUnusedLocal,PyShadowingNames
if __name__ == '__main__':
    base = Tk()
    # Database Connection
    # dbh = MySQLdb.connect(host="localhost", db="incubator", user="root", passwd="0000")

    getBacteria = dbh.cursor()
    saveToTable = dbh.cursor()

    # Global variables
    bacteria_list1 = StringVar()
    isolate_name = StringVar()
    patient_id = StringVar()
    pa_id = StringVar()
    petri_dish_count = IntVar()
    pdishNumber = IntVar()
    disc_found_value = IntVar()
    Disc_number_Count = IntVar()
    img_scanned = StringVar()
    pdishNumberSet = StringVar()
    sample_id = IntVar()
    abx_result_dictionary_LengthGlobal = StringVar()
    imglocationhome = "assets/img/"

    sampleBuild = dbh.cursor()
    val = None
    val2 = None
    diction = {}
    ListTup = []

    sampleBuild.execute("SELECT * from zones where sample_id = 6")
    count = 1
    for a2 in sampleBuild.fetchall():
        val = a2[1].split(",")[0]
        val2 = a2[1].rsplit(",")[-1]
        diction[count] = ((int(val[1:])), (int(val2[:-1])))

        # diction.setdefault(count, [])
        # diction[count].append((int(val[1:])))
        # diction[count].append(int(val2[:-1]))
        count += 1

    patient_Ids = {}
    abx_dose_label = {}
    abx_result_label = {}
    photo_edit = cal.Label()
    progress_label = {}
    processLabel = cal.Label()
    zonefinderInitializerQ = "SELECT timestampdiff(hour,pd.endTime,now()) as durationLeft,sa.accession_number,pd.dish_id, pd.sample_id, pd.dish_id , " + str(
        " ") + "ps.pocket_id FROM samples sa INNER JOIN petri_dish pd inner JOIN pocket_state ps on pd.dish_id=ps.pocket_id and " + str(
        " ") + "sa.sample_id=pd.sample_id where pd.state =1 and pd.exec_state = 0 Limit 1"

    edit_BoxValue = None
    abx_result_dictionary = {}
    _edit = None
    imageDisplayScaled = None
    imgDisplay = None
    imgDisplayII = None
    resultRoot = None
    resultRootBase = None
    scanPatientID_view = None
    rootConfirm = None
    en_samplewindow = None
    addRoot = None
    petri_dish_view = None
    pockets_full = None
    pocket_root = None
    abxRoot = None
    dish_allocation = None
    finishDateTime = None

    zone_distances = None
    newImageFile = None
    arrayDistances = None
    discs = None
    old_img = None

    bigfont = cal.Style()
    # base.protocol("WM_DELETE_WINDOW")
    # base.attributes("-fullscreen",True)
    # base.geometry("900x700+550+190")

    buttons_override = cal.Style()
    buttons_override.configure("TButton", foreground="#000", background="#fff", relief=SOLID, font=("SEGOE UI", 15))
    frame_override = cal.Style()
    frame_override.configure("TFrame", background="#fff")
    label_override = cal.Style()
    label_override.configure("TLabel", background="#fff", font=("SEGOE UI", 15))
    combobox_override = cal.Style()
    combobox_override.configure("TCombobox", background="#fff", font=("SEGOE UI", 15))
    entry_override = cal.Style()
    entry_override.configure("TEntry", font=("SEGOEUI", 15))
    lframe_override = cal.Style()
    lframe_override.configure("TLabelframe", background="#fff")
    base.config(background="white")
    base.title("New")

    get_all_abx = dbh.cursor()
    get_all_abx.execute("select * from antibiotics")
    abx_list1 = get_all_abx.fetchall()
    abx_list_ = StringVar()
    abx_list_.set(abx_list1)

    list_sample_abx = list()
    for row_abx in abx_list1:
        list_sample_abx.append(str(row_abx[1]) + " [" + str(row_abx[3]) + "]")


    def scanPatientRun():
        scanPatientThread = threading.Thread(target=scanPatientID, daemon=True, name="onStart")
        scanPatientThread.start()


    #   def onStart():     onBoot = threading.Thread(target=onStart, daemon=True)
    #     onBoot.start()

    titleBar = cal.Label(base, text="INCUBATOR UI DESIGN PROTOTYPE")
    titleBar.pack(pady=10)
    dash_frame = cal.Frame(base, relief=SOLID, padding=20)
    label_frame = cal.LabelFrame(dash_frame, relief=SOLID, padding=20, text="Notifications")
    cal.Button(dash_frame, text="NEW SAMPLE TEST", width=30, padding=20, command=scanPatientRun).pack(pady=5)
    cal.Button(dash_frame, text="TESTS IN PROGRESS", command=resultsInProgress, width=30, padding=20).pack(pady=5)
    cal.Button(dash_frame, text="COMPLETED TESTS", command=compledTests, width=30, padding=20).pack(pady=5)
    # cal.Button(dash_frame, text="TESTS REPORT", command=reportResults, width=30, padding=20).pack(pady=5)
    cal.Button(dash_frame, text="PRINT AGAR LABEL ", width=30, padding=20, command=printAgarLabel).pack(pady=5)
    notificationBtn = Label(label_frame, width=30, text="NO PROCESS RUNNING", font=("SEGOE UI", 15))
    notificationBtn["background"] = "#fff"
    notificationBtn.pack(pady=5, side=LEFT)
    label_frame.pack()
    dash_frame.pack()

    zonefinderInitializer()
    base.mainloop()
