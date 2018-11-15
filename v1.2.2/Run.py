from assets.package.base import *


def clear_Input(entryfield):
    entryfield.delete(0, 'end')
    entryfield.focus()

#  window ?-alpha ?double?? ?-transparentcolor ?color?? ?-disabled ?bool?? ?-fullscreen ?bool?? ?-toolwindow ?bool?? ?-topmost ?bool??"


def iconset(value):
    value.attributes("-fullscreen", True)
    try:
        value.iconbitmap(icoloc)
    except:
        pass


def itemselected(event, entryfield, condition):
    global isolatename, abxname, uniquecode
    entryfield.delete(0, 'end')
    try:
        entryfield.insert(0, event.widget.get(event.widget.curselection()))
        if condition == 1:
            isolatename = event.widget.get(event.widget.curselection())
        elif not condition:
            abxname = event.widget.get(event.widget.curselection())
        else:
            uniquecode = event.widget.get(event.widget.curselection())
    except Exception as _:
        print()


def toListbox(val, listbox, mydata):
    value_abx = val.widget.get()
    value_abx = value_abx.strip().lower()
    if value_abx == '':
        data = mydata

    else:
        data = []
        for item in mydata:
            if value_abx in item.lower():
                data.append(item)

    listboxupdate(data, listbox)


def listboxupdate(data, listbox):
    listbox.delete(0, 'end')
    data = sorted(data, key=str.lower)
    for item in data:
        listbox.insert('end', item)


def stored_tests():
    # noinspection PyShadowingNames
    def cmptest():

        global topLevelWin, generalOpt, uniquecode
        topLevelWin = Toplevel(base)
        getCursor.execute("SELECT  sample_id FROM samples WHERE  uniquecode = '" + uniquecode + "' ORDER BY  sample_id ASC  LIMIT  1")
        for d in getCursor.fetchall():
            iconset(topLevelWin)
            cFrame = cal.Frame(topLevelWin, padding=5, relief=SOLID)
            generalOpt = None

            getCursor.execute(
                "SELECT sa.uniquecode, ba.bacteria_name FROM samples sa inner join bacteria" + str(" ")
                + " ba on sa.bacteria_id  = ba.bacteria_id where sa.sample_id= '" + str(d[0]) + "'")
            for Id in getCursor.fetchall():
                cal.Label(topLevelWin, text="unique code[" + str(Id[0]) + "] bacteria [" + str(
                    Id[1][:10] + ".. " if len(Id[1]) > 10 else Id[1]) + "]").pack(pady=10)
            generalOpt = cal.Frame(cFrame, padding=5, relief=SOLID)
            cal.Label(generalOpt, text="Antibiotics", width=15).pack(side="left", padx=3, anchor="w")
            cal.Label(generalOpt, text="Dose", width=4).pack(side="left", padx=3, anchor="w")
            cal.Label(generalOpt, text="MM", width=4).pack(side="left", padx=3, anchor="w")
            cal.Label(generalOpt, text="S>", width=3).pack(side="left", padx=3, anchor="w")
            cal.Label(generalOpt, text="R<", width=3).pack(side="left", padx=3, anchor="w")
            cal.Label(generalOpt, text="INTE", width=4).pack(side="left", padx=3, anchor="w")
            generalOpt.pack()

            dbh.commit()
            getCursor.execute(
                "SELECT an.abx_name , an.abx_content, ds.diameter, eu.susceptible , eu.resistance , an.abx_code FROM samples sa" + str(
                    " ") + " INNER JOIN discs ds INNER JOIN antibiotics an INNER JOIN eucast eu on  ds.abx_id = an.abx_id   " + str(
                    " ") + " and sa.sample_id=ds.sample_id and eu.abx_id=an.abx_id where sa.sample_id='" + str(d[0]) + "' ")

            generalOpt = {}

            for i, data in enumerate(getCursor.fetchall()):
                resultFrame = cal.Frame(cFrame, padding=5, relief=SOLID)
                cal.Label(resultFrame, text=str(i + 1) + ". " + str(
                    data[0][:12] + ".. " if len(data[0]) > 12 else data[0]) + "[" +
                                            str(data[5]) + "]", width=15).pack(side="left", padx=3, anchor="w")
                cal.Label(resultFrame, text=str(data[1]), width=4).pack(side="left", padx=3, anchor="w")
                generalOpt[i + 20] = cal.Label(resultFrame, text=str(data[2]), width=4)
                generalOpt[i + 20].pack(side="left", padx=3, anchor="w")
                cal.Label(resultFrame, text=str(data[3]), width=3).pack(side="left", padx=3, anchor="w")
                cal.Label(resultFrame, text=str(data[4]), width=3).pack(side="left", padx=3, anchor="w")
                if data[2] >= data[3]:
                    generalOpt[i + 10] = cal.Label(resultFrame, text="S", width=4)
                elif data[2] < data[4]:
                    generalOpt[i + 10] = cal.Label(resultFrame, text="R", width=4)
                else:
                    generalOpt[i + 10] = cal.Label(resultFrame, text="I", width=4)
                generalOpt[i + 10].pack(side="left", padx=3, anchor="w")
                resultFrame.pack()

            def edTest():
                global topLevelWin, imagefx, imagefxs, generals

                generals = {}
                g = 0

                topLevelWin = Toplevel(base)
                iconset(topLevelWin)
                eFrame = cal.Frame(topLevelWin, relief=SOLID, padding=20)

                if os.path.exists(imglocationhome + str(d[0]) + "/newzonesIm" + str(d[0]) + ".png"):
                    imagefx = Image.open(imglocationhome + str(d[0]) + "/newzonesIm" + str(d[0]) + ".png")
                else:
                    imagefx = Image.open(imglocationhome + str(d[0]) + "/zonesfoundIm" + str(d[0]) + ".png")

                imagefx = imagefx.resize((550, 500), Image.ANTIALIAS)
                imagefxs = ImageTk.PhotoImage(imagefx)
                generals[g + 1] = cal.Label(eFrame, image=imagefxs)
                generals[g + 1].pack()
                cal.Button(eFrame, image=okImg, padding=10,  command=topLevelWin.destroy).pack(pady=3)
                eFrame.pack()


            cal.Button(cFrame, image=backImg, padding=10, command=topLevelWin.destroy).pack(side=LEFT, pady=10)
            cal.Button(cFrame, image=photoImg, padding=10, command=edTest).pack(side=RIGHT, pady=10)

            cFrame.pack()

    compledlist = []
    getCursor.execute("SELECT uniquecode FROM samples")
    getAntiobiotic = getCursor.fetchall()
    for i in getAntiobiotic:
        compledlist.append(i[0])

    global topLevelWin
    topLevelWin = Toplevel(base)
    iconset(topLevelWin)
    abxFrame = cal.Frame(topLevelWin, relief=SOLID, padding=20)
    cal.Label(topLevelWin, text="approved tests").pack(pady=10)
    anEntry = cal.Entry(abxFrame, width=30,  justify="center")
    anEntry.pack(ipady=10, pady=10)
    anEntry.insert(0, "Enter test unique code here")
    anEntry.bind("<FocusIn>", lambda event: clear_Input(anEntry))
    cmpListbox = Listbox(abxFrame, width=30)
    listboxupdate(compledlist, cmpListbox)
    cmpListbox.bind("<<ListboxSelect>>", lambda event, efield=anEntry: itemselected(event, efield, event))
    anEntry.bind("<KeyRelease>", lambda e, box=cmpListbox: toListbox(e, box, compledlist))
    cmpListbox.bind("<Return>", lambda e: None if uniquecode is None else cmptest())
    cmpListbox.bind("<Double-Button-1>", lambda e: None if uniquecode is None else cmptest())
    cmpListbox.pack()
    cal.Button(abxFrame, image=backImg, padding=10, command=topLevelWin.destroy).pack(side=LEFT, pady=10)
    cal.Button(abxFrame, image=okImg, padding=10, command=None if uniquecode is None else cmptest).pack(side=RIGHT, pady=10)
    anEntry.pack()
    abxFrame.pack()


def start_test():

    def locateImgdisc():
        global imgpath, coordinates, images, masks, antiobioticsDis, imageFilename, myflag
        myflag = True
        try:
            imageFilename = imglocationhome + "tryImg.png"
            imgscr = cv2.imread(imageFilename)
            gLenght, avalue, cLength = 0, 0, dict()

            for ai in range(1, 10):
                _, threshphoto = cv2.threshold(cv2.GaussianBlur(cv2.cvtColor(imgscr, cv2.COLOR_BGR2GRAY), (125, 125), 0),
                                               ai, 255, cv2.THRESH_BINARY)
                _, contours, _ = cv2.findContours(threshphoto, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                cLength[ai] = len(contours)
            thresh = min(cLength, key=lambda a: cLength[a])

            for dl, ln in cLength.items():
                if ln <= thresh:
                    thresh = ln
                    avalue = dl

            _, threshphoto = cv2.threshold(cv2.GaussianBlur(cv2.cvtColor(imgscr, cv2.COLOR_BGR2GRAY), (125, 125), 0),
                                           avalue, 255, cv2.THRESH_BINARY)
            _, contours, _ = cv2.findContours(threshphoto, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            os.remove(imageFilename)

            for e, c in enumerate(contours):
                if cv2.arcLength(c, True) > gLenght:
                    gLenght = cv2.arcLength(c, True)
                    xAxis, yAxix, width, hieght = cv2.boundingRect(c)
                    cv2.imwrite(imageFilename, cv2.resize(imgscr[yAxix:yAxix + hieght, xAxis:xAxis + width], (0, 0), fx=2.20_3, fy=2.20_2))

            imgpath, coordinates, images, masks = locatediscs(imageFilename)
            antiobioticsDis = discsearcher(featurefinder(images, masks))
        except Exception as IMG_NOT_FOUND:
            print(IMG_NOT_FOUND)
            myflag = False



    def clear_field():
        entryField.delete(0, "end")
        entryField.focus()

    isolateList = []
    getCursor.execute("SELECT bacteria_name FROM bacteria ")
    getIsoList = getCursor.fetchall()
    for isolate in getIsoList:
        isolateList.append(isolate[0])

    def proceedtophoto():
        global uniquecode
        try:
            uniquecode = entryField.get().upper()
        except Exception as _:
            pass

        # noinspection PyShadowingNames
        def discabxConfirm():
            global imgpath, images, antiobioticsDis, imagedis, imageScale, topLevelWin, isolatename, valHolder
            topLevelWin.destroy()
            topLevelWin = Toplevel(base)
            valHolder = topLevelWin
            iconset(topLevelWin)
            cal.Label(topLevelWin, text="Confirm discs content - Antibiotics").pack(pady=20)
            discabxFrame = cal.Frame(topLevelWin, relief=SOLID, padding=30)


            imagedis = PhotoImage(file=imgpath)
            imageScale = imagedis.subsample(2, 2)

            antiobioticlist = []
            getCursor.execute(
                "SELECT an.abx_name , an.abx_code FROM eucast eu INNER JOIN  antibiotics an "+str(" ")
                + " INNER JOIN bacteria ab on ab.bacteria_id = eu.bacteria_id AND an.abx_id = eu.abx_id "+str(" ")
                + "WHERE eu.bacteria_id = (SELECT bacteria_id FROM bacteria WHERE bacteria_name='" + str(isolatename) + "')")
            getAntiobiotic = getCursor.fetchall()
            # noinspection PyShadowingNames
            for i in getAntiobiotic:
                antiobioticlist.append(i[0] + " [" + i[1] + "]")

            def abToChange(abname, abdisc):

                def bacteria_change():
                    global abxname
                    topLevelWin.destroy()
                    abname["text"] = "Disc " + str(abdisc) + "." + abxname
                    if abdisc:
                        antiobioticsDis[abdisc] = abxname.split("[")[0]
                    if not abdisc:
                        antiobioticsDis[abdisc] = "No match found"

                global topLevelWin
                topLevelWin = Toplevel(base)
                iconset(topLevelWin)
                abxFrame = cal.Frame(topLevelWin, relief=SOLID, padding=20)
                cal.Label(topLevelWin,  text="Change antibiotic for  disk." + str(abdisc) + "").pack(pady=10)
                anEntry = cal.Entry(abxFrame, width=30)
                anEntry.pack(ipady=10, pady=10)
                anListbox = Listbox(abxFrame, width=30)
                listboxupdate(antiobioticlist, anListbox)
                anEntry.bind("<KeyRelease>", lambda e, box=anListbox: toListbox(e, box, antiobioticlist))
                anListbox.bind("<<ListboxSelect>>", lambda event, efield=anEntry: itemselected(event, efield, False))
                anListbox.bind("<Double-Button-1>", lambda e: bacteria_change())
                anListbox.bind("<Return>", lambda e: bacteria_change())
                anListbox.pack()
                cal.Button(abxFrame, image=cancelImg, padding=10, command=topLevelWin.destroy).pack(side=LEFT, pady=10)
                cal.Button(abxFrame, image=okImg, padding=10, command=bacteria_change).pack(side=RIGHT, pady=10)
                anEntry.pack()
                abxFrame.pack()

            discabxBox = cal.Frame(discabxFrame, relief=SOLID, padding=10)
            discabxL = cal.Frame(discabxBox)
            discabxR = cal.Frame(discabxBox)

            #Dictionary Label
            disclabeldict = {}
            cal.Label(discabxFrame, image=imageScale).pack()
            for i in antiobioticsDis:
                #disclabeldict[i] = cal.Label(discabxL, text="Disc " + str(i) + "." + antiobioticsDis[i][:10]+"..." if len(antiobioticsDis[i]) > 10 else antiobioticsDis[i])
                disclabeldict[i] = cal.Label(discabxL, text="Disc " + str(i) + "." + antiobioticsDis[i])
                disclabeldict[i].pack(anchor='w', pady=0)
                disclabeldict[i].bind("<Button-1>", lambda eventhandle, akey=i, aname=disclabeldict[i]: abToChange(aname, akey))
                if i > 3:
                    disclabeldict[i].pack_forget()
                    disclabeldict[i] = cal.Label(discabxR, text="Disc " + str(i) + "." + antiobioticsDis[i][:10] + "..." if len(antiobioticsDis[i]) > 10 else antiobioticsDis[i])
                    disclabeldict[i].pack(anchor='w', pady=0)
                    disclabeldict[i].bind("<Button-1>", lambda eventhandle, akey=i, aname=disclabeldict[i]: abToChange(aname, akey))
            discabxL.pack(side=LEFT, ipadx=5)
            discabxR.pack(side=RIGHT, ipadx=5)
            discabxBox.pack(pady=5)

            def testData():

                global images, masks, antiobioticsDis, generalOpt, imgpath, isolatename, uniquecode, imageFilename, myflag
                # noinspection PyShadowingNames
                i = 1
                for a in range(1, 4):
                    generalOpt[a].pack_forget()
                generalOpt[i + 4] = cal.LabelFrame(generalOpt[i + 3], relief=SOLID, padding=20, text="Test progress")
                generalOpt[i + 5] = Label(generalOpt[i + 4], width=29, text="Executing please wait")
                generalOpt[i + 5].pack(pady=5, side=LEFT)
                generalOpt[i + 4].pack()

                def blinker():
                    global generalOpt
                    try:
                        c = generalOpt[i + 5].cget("foreground")
                        n = "#f0f0f0" if c == "black" else "black"
                        generalOpt[i + 5]["foreground"] = n
                        generalOpt[1 + 6] = base.after(1000, blinker)
                    except Exception as ERR_BL:
                        print("ERR_BL: " + str(ERR_BL))

                blinker()

                discwriter(antiobioticsDis, featurefinder(images, masks), "assets/antibiotics/")
                generalOpt[i + 5]["text"] = "Storing data collected"
                try:
                    getCursor.execute(
                        "INSERT INTO samples (uniquecode,bacteria_id) VALUES ('" + str(uniquecode)
                        + "',(SELECT bacteria_id FROM bacteria WHERE bacteria_name='" + str(isolatename) + "'))")
                    dbh.commit()
                except pymysql.Error as _:
                    dbh.rollback()

                for a in antiobioticsDis:
                    try:
                        getCursor.execute(
                            "INSERT INTO discs (abx_id,sample_id) VALUES ((SELECT abx_id FROM antibiotics WHERE abx_name ='" +
                            str(antiobioticsDis[a]) + "'),(SELECT sample_id FROM samples WHERE uniquecode='" + str(
                                uniquecode) + "' ))")
                        dbh.commit()
                    except pymysql.Error as ERR_D:
                        print(ERR_D)
                        dbh.rollback()

                generalOpt[i + 5]["text"] = "Preparing working directory"
                time.sleep(2)
                getCursor.execute("SELECT sample_id FROM samples WHERE uniquecode='" + str(uniquecode) + "' ")
                for d in getCursor.fetchall():
                    try:
                        os.mkdir("assets/img/" + str(d[0]))
                        try:
                            generalOpt[i + 5]["text"] = "Moving images"
                            time.sleep(2)
                            os.rename(imgpath, "assets/img/" + str(d[0]) + "/discsforcode" + str(d[0]) + ".png")
                            os.rename(imageFilename, "assets/img/" + str(d[0]) + "/Im" + str(d[0]) + ".png")
                        except Exception as ERR_M:
                            print(ERR_M)
                    except Exception as ERR_L:
                        print(ERR_L)

                    myflag = True
                    global newImageFile, arrayDistances, discs

                    try:
                        if PhotoImage(file="assets/img/" + str(d[0]) + "/Im" + str(d[0]) + ".png"):
                            generalOpt[i + 5]["text"] = "Ready to start process"
                            time.sleep(1)
                            generalOpt[i + 5]["text"] = "Processing image please wait"
                            newImageFile, arrayDistances, discs = zonefinder("assets/img/" + str(d[0]) + "/Im" + str(d[0]) + ".png")
                            generalOpt[i + 5]["text"] = "Processing image completed"
                            time.sleep(2)
                            myflag = False
                    except Exception as ERR_IM:
                        print(ERR_IM)

                    def waitFor():
                        bL = base.after(1000, waitFor)
                        if not myflag:
                            global iflag
                            iflag = True
                            base.after_cancel(bL)
                            generalOpt[i + 5]["text"] = "Saving data"

                            time.sleep(2)

                            list_distance = []
                            list_distance[:] = [x * 0.0307692 for x in arrayDistances]

                            try:
                                dbh.cursor().execute("DELETE FROM zones WHERE sample_id='" + str(d[0]) + "'")
                                dbh.commit()
                            except pymysql.Error as ERR_DEL:
                                print("ERR_DEL : " + str(ERR_DEL))
                                dbh.rollback()

                            # noinspection PyShadowingNames
                            for a in discs:
                                dbh.commit()
                                try:
                                    dbh.cursor().execute(
                                        "INSERT INTO zones (disc,sample_id) VALUES ('" + str(discs[a]) + "','" + str(
                                            d[0]) + "')")
                                    dbh.commit()
                                except pymysql.Error as ERR_INS:
                                    print("ERR_INS :" + str(ERR_INS))
                                    dbh.rollback()

                            # noinspection PyUnusedLocal
                            distanceDict = {}
                            getCursor.execute("SELECT disc_id  FROM discs WHERE sample_id ='" + str(d[0]) + "'")
                            for ai, distance in enumerate(list_distance):
                                distanceToarrary = math.floor(distance)
                                distanceDict[ai + 1] = distanceToarrary

                            for (_, distances), disc_num in zip(distanceDict.items(), getCursor.fetchall()):
                                try:
                                    dbh.cursor().execute(
                                        "UPDATE discs set diameter=" + str(distances) + " WHERE sample_id='" + str(
                                            d[0]) + "' and disc_id =" + str(disc_num[0]))
                                    dbh.commit()
                                except pymysql.Error as ERR_UPD:
                                    print("ERR_UPD :" + str(ERR_UPD))
                                    dbh.rollback()

                            try:
                                dbh.cursor().execute(
                                    "INSERT INTO images (state,imagelocation,sample_id) VALUES (3,'" + str(
                                        imglocationhome + str(d[0]) + "/zonesfoundIm" + str(
                                            d[0]) + ".png") + "','" + str(d[0]) + "')")
                                dbh.commit()
                            except pymysql.Error as ERR_INS_I:
                                print("ERR_INS_I :" + str(ERR_INS_I))
                                dbh.rollback()
                            #generalOpt[i + 5]["text"] =  "
                            iflag = False

                    waitFor()

                    # noinspection PyShadowingNames
                    def singleTestProgressing():

                        global topLevelWin, generalOpt

                        base.after_cancel(generalOpt[1 + 6])
                        topLevelWin.destroy()

                        topLevelWin = Toplevel(base)
                        iconset(topLevelWin)
                        cFrame = cal.Frame(topLevelWin, padding=5, relief=SOLID)

                        generalOpt = None

                        getCursor.execute(
                            "SELECT sa.uniquecode, ba.bacteria_name FROM samples sa inner join bacteria" + str(" ")
                            + " ba on sa.bacteria_id  = ba.bacteria_id where sa.sample_id= '" + str(d[0]) + "'")

                        for Id in getCursor.fetchall():
                            cal.Label(topLevelWin, text="unique code[" + str(Id[0]) + "] bacteria [" + str(
                                Id[1][:10] + ".. " if len(Id[1]) > 10 else Id[1]) + "]").pack(pady=10)
                        generalOpt = cal.Frame(cFrame, padding=5, relief=SOLID)
                        cal.Label(generalOpt, text="Antibiotics", width=15).pack(side="left", padx=3, anchor="w")
                        cal.Label(generalOpt, text="Dose", width=4).pack(side="left", padx=3, anchor="w")
                        cal.Label(generalOpt, text="MM", width=4).pack(side="left", padx=3, anchor="w")
                        cal.Label(generalOpt, text="S>", width=3).pack(side="left", padx=3, anchor="w")
                        cal.Label(generalOpt, text="R<", width=3).pack(side="left", padx=3, anchor="w")
                        cal.Label(generalOpt, text="INTE", width=4).pack(side="left", padx=3, anchor="w")
                        generalOpt.pack()

                        dbh.commit()
                        getCursor.execute(
                            "SELECT an.abx_name , an.abx_content, ds.diameter, eu.susceptible , eu.resistance , an.abx_code FROM samples sa" + str(
                                " ") + " INNER JOIN discs ds INNER JOIN antibiotics an INNER JOIN eucast eu on  ds.abx_id = an.abx_id   " + str(
                                " ") + " and sa.sample_id=ds.sample_id and eu.abx_id=an.abx_id where sa.sample_id='" + str(
                                d[0]) + "' ")

                        generalOpt = {}

                        for i, data in enumerate(getCursor.fetchall()):
                            resultFrame = cal.Frame(cFrame, padding=5, relief=SOLID)
                            cal.Label(resultFrame, text=str(i + 1) + ". " + str(
                                data[0][:12] + ".. " if len(data[0]) > 12 else data[0]) + "[" +
                                                        str(data[5]) + "]", width=15).pack(side="left", padx=3, anchor="w")
                            cal.Label(resultFrame, text=str(data[1]), width=4).pack(side="left", padx=3, anchor="w")
                            generalOpt[i + 20] = cal.Label(resultFrame, text=str(data[2]), width=4)
                            generalOpt[i + 20].pack(side="left", padx=3, anchor="w")
                            cal.Label(resultFrame, text=str(data[3]), width=3).pack(side="left", padx=3, anchor="w")
                            cal.Label(resultFrame, text=str(data[4]), width=3).pack(side="left", padx=3, anchor="w")
                            if data[2] >= data[3]:
                                generalOpt[i + 10] = cal.Label(resultFrame, text="S", width=4)
                            elif data[2] < data[4]:
                                generalOpt[i + 10] = cal.Label(resultFrame, text="R", width=4)
                            else:
                                generalOpt[i + 10] = cal.Label(resultFrame, text="I", width=4)
                            generalOpt[i + 10].pack(side="left", padx=3, anchor="w")
                            resultFrame.pack()

                        def edTest():
                            global topLevelWin, imagefx, imagefxs, generals

                            generals = {}
                            g = 0

                            topLevelWin = Toplevel(base)
                            # topLevelWin.attributes("-fullscreen", True)
                            iconset(topLevelWin)
                            eFrame = cal.Frame(topLevelWin, relief=SOLID, padding=20)

                            getCursor.execute(
                                "SELECT * FROM samples sa inner join bacteria ba on sa.bacteria_id = ba.bacteria_id where sa.sample_id= '" + str(
                                    d[0]) + "'")

                            # for l in getCursor.fetchall():cal.Label(eFrame, text="EDIT RESULTS FOR PATIENT ID #[" + str(l[1]) + "]").pack(pady=10)

                            # noinspection PyShadowingNames
                            def cAdjust(dsc, cond):
                                discs = {}
                                getCursor.execute("SELECT disc from zones where sample_id ='" + str(d[0]) + "'")
                                for a, disc in enumerate(getCursor.fetchall()):
                                    discs[a + 1] = ((int(disc[0].split(",")[0][1:])), (int(disc[0].rsplit(",")[-1][:-1])))

                                global imagefx, imagefxs, generals, imageScale, imagedis

                                zone_distances, list_distances, dist = [], [], {}

                                getCursor.execute("SELECT diameter FROM discs WHERE sample_id= '" + str(d[0]) + "'")
                                for diam in getCursor.fetchall():
                                    zone_distances.append(diam[0] / 0.0307692)

                                oimg = imglocationhome + str(d[0]) + "/Im" + str(d[0]) + ".png"
                                zone_distances = zoneadjuster(zone_distances, int(dsc), cond, 1)
                                circledrawer(oimg, zone_distances, discs)
                                list_distances[:] = [x * 0.0307692 for x in zone_distances]

                                getCursor.execute("SELECT disc_id  FROM discs WHERE sample_id ='" + str(d[0]) + "'")

                                for g, l in enumerate(list_distances):
                                    dist[g] = round(l)

                                for (_, di), disc_id in zip(dist.items(), getCursor.fetchall()):
                                    try:
                                        dbh.cursor().execute(
                                            "UPDATE discs set diameter=" + str(di) + " WHERE sample_id='" + str(d[0]) +
                                            "'  and disc_id =" + str(disc_id[0]) + "")
                                        dbh.commit()
                                    except pymysql.Error as e:
                                        print(e)
                                        dbh.rollback()

                                getCursor.execute(
                                    "SELECT imagelocation FROM images WHERE state=3 AND sample_id= '" + str(d[0]) + "'")
                                for im in getCursor.fetchall():
                                    shutil.copy(imglocationhome + str(d[0]) + "/newzonesIm" + str(d[0]) + ".png", im[0])
                                    imagefx = Image.open(im[0])
                                    imagefx = imagefx.resize((550, 500), Image.ANTIALIAS)
                                    imagefxs = ImageTk.PhotoImage(imagefx)
                                    imagedis = PhotoImage(file=im[0])
                                    imageScale = imagedis.subsample(2, 2)

                                getCursor.execute(
                                    "SELECT ds.diameter, eu.susceptible , eu.resistance  FROM samples sa  INNER JOIN discs ds " + str(
                                        " ") + "INNER  JOIN antibiotics an INNER  JOIN eucast eu on  ds.abx_id = an.abx_id and " + str(
                                        " ") + "sa.sample_id=ds.sample_id and eu.abx_id=an.abx_id where sa.sample_id='" + str(
                                        d[0]) + "' ")
                                # noinspection PyShadowingNames
                                for i, a in enumerate(getCursor.fetchall()):
                                    generalOpt[i + 20]["text"] = a[0]
                                    if a[0] >= a[1]:
                                        generalOpt[i + 10]["text"] = "S"
                                    elif a[0] < a[2]:
                                        generalOpt[i + 10]["text"] = "R"
                                    else:
                                        generalOpt[i + 10]["text"] = "I"

                                # Onpause
                                generals[1 + 0]["image"] = imagefxs
                                showIm["image"] = imageScale

                            if os.path.exists(imglocationhome + str(d[0]) + "/newzonesIm" + str(d[0]) + ".png"):
                                imagefx = Image.open(imglocationhome + str(d[0]) + "/newzonesIm" + str(d[0]) + ".png")
                            else:
                                imagefx = Image.open(imglocationhome + str(d[0]) + "/zonesfoundIm" + str(d[0]) + ".png")

                            imagefx = imagefx.resize((550, 500), Image.ANTIALIAS)
                            imagefxs = ImageTk.PhotoImage(imagefx)
                            generals[g + 1] = cal.Label(eFrame, image=imagefxs)
                            generals[g + 1].pack()
                            combodropList = []
                            combodropList[:] = range(1, len(antiobioticsDis) + 1)
                            bFrame = cal.Frame(eFrame)
                            generals[g + 2] = cal.Combobox(bFrame, width=10, values=combodropList, state="readonly")
                            generals[g + 2].current(0)
                            generals[g + 3] = cal.Button(bFrame, text="+", width=3, )
                            generals[g + 3].bind("<Button-1>", lambda event: cAdjust(generals[g + 2].get(), True))
                            generals[g + 3].pack(side=LEFT, padx=2)
                            generals[g + 2].pack(pady=10, ipady=3, padx=20, side=LEFT)
                            generals[g + 4] = cal.Button(bFrame, text="-", width=3)
                            generals[g + 4].bind("<Button-1>", lambda event: cAdjust(generals[g + 2].get(), False))
                            generals[g + 4].pack(side=LEFT, padx=2)
                            bFrame.pack()
                            cal.Button(eFrame, text="Confirm", padding=3, width=10, command=topLevelWin.destroy).pack(
                                pady=3)
                            eFrame.pack()

                        global imagedis, imageScale, generals
                        generals = {}
                        cal.Button(cFrame, image=okImg, padding=10, command=topLevelWin.destroy).pack(side=RIGHT,
                                                                                                      pady=10)
                        cal.Button(cFrame, image=editImg, padding=10, command=edTest).pack(side=LEFT, pady=10)
                        getCursor.execute(
                            "SELECT imagelocation FROM images WHERE state=3 AND sample_id= '" + str(d[0]) + "'")
                        for imgloc in getCursor.fetchall():
                            imagedis = PhotoImage(file=imgloc[0])
                            imageScale = imagedis.subsample(2, 2)
                            # Image to  display when completed
                            showIm = cal.Label(cFrame, image=imageScale)
                            showIm.bind("<Button-1>", lambda e: edTest())
                            showIm.pack()
                        cFrame.pack()

                    def waitTo():
                        global iflag
                        T = base.after(1000, waitTo)
                        if not iflag:
                            base.after_cancel(T)
                            singleTestProgressing()

                    waitTo()


            def datacollectionDone():
                    global topLevelWin, isolatename, antiobioticsDis, imagedis, imageScale, uniquecode, generalOpt, valHolder
                    # noinspection PyShadowingNames
                    try:
                        valHolder.destory()
                    except:
                        pass
                    # noinspection PyShadowingNames
                    i = 0
                    topLevelWin = Toplevel(base)
                    iconset(topLevelWin)
                    conFrame = cal.Frame(topLevelWin, relief=SOLID, padding=20)
                    cal.Label(conFrame, text="Isolate : " + str(isolatename)).pack(pady=1, anchor="w")
                    cal.Label(conFrame, text="Antibiotics").pack(pady=1, anchor="w")

                    for ab in antiobioticsDis:
                        cal.Label(conFrame, text=str(ab) + "." + str(antiobioticsDis[ab])).pack(anchor='w')
                    imagedis = PhotoImage(file=imgpath)
                    imageScale = imagedis.subsample(2, 2)
                    generalOpt = {i + 1: cal.Label(conFrame, image=imageScale), i + 4: conFrame,
                                  i + 2: cal.Button(conFrame, image=okImg,  padding=10, command=threading.Thread(target=testData).start),
                                  i + 3: cal.Button(conFrame, image=cancelImg,  padding=10, command=topLevelWin.destroy)}
                    generalOpt[i + 1].pack(anchor='w')
                    generalOpt[i + 2].pack(pady=5, side=RIGHT),
                    generalOpt[i + 3].pack(pady=5, side=LEFT),
                    conFrame.pack()

            def anproceed():
                global generalOpt
                generalOpt = False
                for b in antiobioticsDis:
                    if antiobioticsDis[b] == "No match found":
                        generalOpt = True

                if not generalOpt:
                    global topLevelWin
                    topLevelWin.destroy()
                    datacollectionDone()

            discOptFrame = cal.Frame(discabxFrame)
            cal.Button(discOptFrame, image=backImg, padding=10, command=topLevelWin.destroy).pack(pady=10, padx=20, side=LEFT)
            cal.Button(discOptFrame, text="ENLARGE", padding=20).pack(pady=10, side=LEFT)
            cal.Button(discOptFrame, image=proceedImg, padding=10, command=anproceed).pack(pady=10, padx=20, side=LEFT)
            discabxFrame.pack()
            discOptFrame.pack()

        if os.path.exists(imglocationhome + "discsfoundtryImg.png"):
            os.remove(imglocationhome + "discsfoundtryImg.png")

        inBackground = threading.Thread(target=locateImgdisc)
        inBackground.start()


        def bgProccessThread():
            global generalOpt, isolatename, myflag
            nL = base.after(1000, bgProccessThread)
            if not inBackground.isAlive():
                if myflag:
                    generalOpt[i].pack(pady=10, side=LEFT)
                    generalOpt[i + 1].pack(pady=10, side=RIGHT)
                    generalOpt[i + 1].bind("<Button-1>", lambda e: None if isolatename is None else discabxConfirm())
                    isolateListBox.bind("<Double-Button-1>", lambda e: None if isolatename is None else discabxConfirm())
                    isolateListBox.bind("<Return>", lambda e: None if isolatename is None else discabxConfirm())
                    generalOpt[i + 2].pack_forget()

                if not myflag:
                    generalOpt[i + 2].pack_forget()
                    #generalOpt[i + 2]["text"] = "Image not found"
                    #generalOpt[i + 2].pack(pady=10)
                    generalOpt[i + 3].pack(pady=10, side=RIGHT)
                    generalOpt[i + 4].pack(pady=10, side=LEFT)
                    generalOpt[i].pack_forget()
                    generalOpt[i + 1].pack_forget()
                base.after_cancel(nL)
        bgProccessThread()



        global topLevelWin, generalOpt
        i = 0
        topLevelWin.destroy()
        topLevelWin = Toplevel(base)
        iconset(topLevelWin)
        cal.Label(topLevelWin, text="Choose isolate").pack(pady=20)
        isoSelectFrame = cal.Frame(topLevelWin, relief=SOLID, padding=30)
        isolateEntry = cal.Entry(isoSelectFrame, width=35, justify="center")
        isolateEntry.insert(0, "Enter isolate name here")
        isolateEntry.bind("<FocusIn>", lambda event: clear_Input(isolateEntry))
        isolateEntry.pack(ipady=10)
        isolateListBox = Listbox(isoSelectFrame, width=35)
        listboxupdate(isolateList, isolateListBox)
        isolateEntry.bind("<KeyRelease>", lambda e, box=isolateListBox: toListbox(e, box, isolateList))
        isolateListBox.bind("<<ListboxSelect>>", lambda event, efield=isolateEntry: itemselected(event, efield, True))
        isolateListBox.pack(pady=10)
        generalOpt = {i: cal.Button(isoSelectFrame, image=backImg, padding=10, command=topLevelWin.destroy),
                      i + 1: cal.Button(isoSelectFrame, image=proceedImg, padding=10),
                      i + 2: Label(isoSelectFrame, text="Proccessing image please wait"),
                      i + 3: cal.Button(isoSelectFrame, image=reloadImg, padding=10, command=proceedtophoto),
                      i + 4: cal.Button(isoSelectFrame, image=cancelImg, padding=10, command=topLevelWin.destroy)
                      }
        generalOpt[i+2].pack(pady=10)
        isoSelectFrame.pack()

    # start test Window
    global topLevelWin, generalOpt
    topLevelWin = Toplevel(base)
    topLevelWin.lift(base)
    #topLevelWin.attributes("-fullscreen", True)
    iconset(topLevelWin)
    cal.Label(topLevelWin, text="Enter test unique code").pack(pady=10)
    startTestFrame = cal.Frame(topLevelWin, padding=20, relief=SOLID)
    entryField = Entry(startTestFrame, width=33, justify="center")
    entryField.bind("<Return>", lambda e: proceedtophoto() if entryField.get() != "" else lambda event: clear_Input(entryField))
    entryField.pack(ipady=9)
    entryField.focus()
    optButtons = cal.Frame(startTestFrame)
    cal.Button(optButtons, image=backImg, padding=10, command=topLevelWin.destroy).pack(padx=10, pady=10, side=LEFT)
    cal.Button(optButtons, text="CLEAR", width=10, padding=20, command=clear_field).pack(padx=10, pady=10, side=LEFT)
    generalOpt = cal.Button(optButtons, image=proceedImg, padding=10)
    generalOpt.bind("<Button-1>", lambda e: proceedtophoto() if entryField.get() != "" else lambda event: clear_Input(entryField))
    generalOpt.pack(padx=10, pady=10, side=LEFT)
    optButtons.pack()
    startTestFrame.pack()


if __name__ == '__main__':
    base = Tk()
    base.title("User flow for validation testing")

    # Image home directory
    imglocationhome = "assets/img/"

    # Images [Icons]
    icolocation = "assets/ico/"
    backImg = PhotoImage(file=icolocation + "back.png")
    okImg = PhotoImage(file=icolocation + "ok.png")
    cancelImg = PhotoImage(file=icolocation + "cancel.png")
    proceedImg = PhotoImage(file=icolocation + "proceed.png")
    editImg = PhotoImage(file=icolocation + "edit.png")
    photoImg = PhotoImage(file=icolocation + "photo.png")
    reloadImg = PhotoImage(file=icolocation + "reload.png")


    icoloc = icolocation+"icon.ico"


    font = nametofont("TkDefaultFont")
    font.configure(size=15)
    base.option_add("*Font", font)
    iconset(base)
    # UI - Main window
    cal.Label(base, text="New user flow for validation testing").pack(pady=10)
    mainFrame = cal.Frame(base, relief=SOLID, padding=20)
    cal.Button(mainFrame, text="start a test", command=start_test, width=20, padding=40).pack(pady=5)
    cal.Button(mainFrame, text="approved tests", width=20, command=stored_tests, padding=40).pack(pady=5)
    cal.Button(mainFrame, text="Quit", width=20, command=base.destroy, padding=40).pack(pady=5)
    mainFrame.pack()
    base.mainloop()
