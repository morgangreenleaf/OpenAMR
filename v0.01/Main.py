from threading import Thread
from Core import *

zone_distances = None
newImageFile = None
arrayDistances = None
discs = None
old_img = None


def zonefinderInitializer():
    global newImageFile
    global arrayDistances
    global discs
    global old_img

    calledsample_id = StringVar()
    calledsample_img = StringVar()
    callzonefinder = dbh.cursor()
    dbh.commit()
    callzonefinder.execute(
        "SELECT timestampdiff(hour,pd.endTime,now()) as durationLeft,sa.accession_number,pd.dish_id,pd.sample_id," + str(
            " ") +
        "pd.dish_id FROM samples sa INNER JOIN petri_dish pd on sa.sample_id=pd.sample_id  where pd.state =1 Limit 1")
    for callerfinder in callzonefinder.fetchall():
        if callerfinder[0] == 0:
            old_img = "assets/img/" + str(callerfinder[3]) + ".png"
            calledsample_id.set(callerfinder[2])
            calledsample_img.set(callerfinder[4])
            try:
                newImageFile, arrayDistances, discs = zonefinder(old_img)
            except:
                pass

            arrayD = arrayDistances.copy()
            arrayDist = arrayDistances.copy()
            arrayDist[:] = [x * 0.0307692 for x in arrayD]
            # print((arrayDist))
            count = -1
            count_12 = 0
            arr = None
            vals = {}
            insertIntoDiameter = dbh.cursor()
            checkAbx = dbh.cursor()
            checkAbx.execute("SELECT disc_id  FROM discs WHERE sample_id =" + str(calledsample_id.get()) + "")

            for x in arrayDist:
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
                print(valueInsert.get())
                dbh.commit()
                try:
                    insertIntoDiameter.execute(
                        "UPDATE discs set diameter=" + str(
                            valueInsert.get()) + " WHERE sample_id=" + str(
                            calledsample_id.get()) + " and disc_id =" + str(coount[0]) + "")
                    # print("inserted" + str(vals[count_12]))
                    # print(coount[0])
                    dbh.commit()
                except:
                    print("Failed to insert")
                    dbh.rollback()
                dbh.rollback()


def printAgarLabel():
    agarRoot = Toplevel(base)
    agar_frame = cal.Frame(agarRoot, relief=SOLID, padding=10)
    agarRoot.config(background="#fff")

    def agar_input_Field(self):
        agar_input.delete(0, "end")

    def quantity_input_Field(self):
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


def scanPatientID():
    global scanPatientID_view
    scanPatientID_view = Toplevel(base)
    scanPatientID_view.title("Incubator ")
    scanPatientID_view.lift(base)
    scan_frame = cal.Frame(scanPatientID_view, padding=20, relief=SOLID)
    scanPatientID_view.config(background="white")

    def clear_id():
        scan_entryField.delete(0, "end")
        scan_entryField.focus()

    def getscanned():
        dbh.commit()
        get_all_bacterial.execute("select bacteria_name from bacteria")
        bacteria_list = get_all_bacterial.fetchall()
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

            def isolate_selected(event):
                serch_1.delete(0, 'end')
                try:
                    serch_1.insert(0, event.widget.get(event.widget.curselection()))
                    isolate_name.set(event.widget.get(event.widget.curselection()))
                except:
                    pass

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

            def add_newBacteria():
                global addRoot
                addRoot = Toplevel(base, background="#FFF")
                top_head = cal.Label(addRoot, text="ADD NEW BACTERIA")
                top_head.pack(pady=20)
                addFrame = cal.Frame(addRoot, relief=SOLID, padding=30)
                add_value = StringVar()

                def addQuery():
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
                            get_all_bacterial.execute("select bacteria_name from bacteria")
                            bacteria_list = get_all_bacterial.fetchall()
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

                def clear_add_Input(event):
                    addInput.delete(0, 'end')

                addInput = cal.Entry(addFrame, width=35, font=("SEGOEUI", 15), justify="center")
                addInput.insert(0, "Enter bacteria name here")
                addInput.bind("<FocusIn>", clear_add_Input)
                add_Button = cal.Button(addFrame, text="Add Bacteria", padding=20, width=30, command=addQuery)
                cancel_btn1 = cal.Button(addFrame, text="Cancel", padding=20, width=30, command=addRoot.destroy)
                addInput.pack(ipady=10)
                add_Button.pack(pady=10)
                cancel_btn1.pack(pady=10)
                addFrame.pack()

            def petriDish_selection():
                if isolate_name.get() == '':
                    print()
                else:
                    global petri_dish_view
                    petri_dish_view = Toplevel(base, background="#FFF")
                    petri_dish_frame = cal.Frame(petri_dish_view, relief=SOLID, padding=20)
                    cal.Label(petri_dish_view,
                              text="NUMBER OF PETRI DISHES FOR ID #[" + patient_id.get() + "]").pack(
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
                            cal.Label(pockets_full_Frame,
                                                         text="ALL POCKETS ARE CURRENTLY IN USE,\n  WAIT FOR ONE TEST TO FINISH.").pack(
                                pady=20)
                            cal.Button(pockets_full_Frame, text="Go Back", padding=20, width=20,
                                       command=pockets_full.destroy).pack()
                            pockets_full_Frame.pack(pady=10)

                        else:

                            def moveMotorToCameraPos(val):

                                process_label["text"] = "WAIT A MOMENT WHILE PROCESSING ..."
                                imageFilename = imglocationhome + "for.png"
                                imgpath =None
                                imgpath =None
                                coordinates =None
                                masks =None


                                def locatediscsMethod():
                                    imgpath, coordinates, images, masks = locatediscs(imageFilename)
                                    img_scanned.set(imgpath)
                                    print(1)

                                locatediscsThread: Thread = threading.Thread(target=locatediscsMethod,name='Outside')
                                locatediscsThread.start()

                                imgpath, coordinates, images, masks = locatediscs(imageFilename)
                                img_scanned.set(imgpath)




                                global imageDisplay
                                global imageDisplayScaled
                                imageDisplay = PhotoImage(file=img_scanned.get())
                                imageDisplayScaled = imageDisplay.subsample(1, 2)

                                global pocket_root
                                global dish_allocation
                                dish_allocation.destroy()
                                pocket_root = Toplevel(base, background="#FFF")

                                pocket_frame = cal.Frame(pocket_root, relief=SOLID, padding=10)

                                cal.Label(pocket_root,
                                          text="ANTIBIOTIC IDENTIFICATION | ID #[" + patient_id.get() + "]").pack(
                                    pady=10)
                                abx_result_dictionary = discsearcher(featurefinder(images, masks))




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
                                            abx_result_dictionary[param2] = abx_name.get()
                                            print(abx_result_dictionary)
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


                                '''isolate_identification={}

                                for isolates in abx_result_dictionary:
                                    print(isolates)
                                    isolate_identification[isolates] = cal.Label(pocket_frame,  text="Disc " + str(isolates) + "." + abx_result_dictionary[isolates])
                                    isolate_identification[isolates].pack(anchor='w')
                                    isolate_identification[isolates].bind("<Button-1>", lambda value: isolate_selectedToChange(isolate_identification[isolates], isolates))

                                print(isolate_identification)
                                '''

                                abx_result_dictionary_LengthGlobal.set(len(abx_result_dictionary))
                                abx_result_dictionary_Length = len(abx_result_dictionary)

                                isolate_identification_1 = cal.Label(pocket_frame, text="Disc " + str(1) + "." +
                                                                                        abx_result_dictionary[1])
                                isolate_identification_2 = cal.Label(pocket_frame, text="Disc " + str(2) + "." +
                                                                                        abx_result_dictionary[2])
                                isolate_identification_3 = cal.Label(pocket_frame, text="Disc " + str(3) + "." +
                                                                                        abx_result_dictionary[3])
                                isolate_identification_4 = cal.Label(pocket_frame, text="Disc " + str(4) + "." +
                                                                                        abx_result_dictionary[4])
                                isolate_identification_5 = cal.Label(pocket_frame, text="Disc " + str(5) + "." +
                                                                                        abx_result_dictionary[5])
                                isolate_identification_6 = cal.Label(pocket_frame, text="Disc " + str(6) + "." +
                                                                                        abx_result_dictionary[6])

                                isolate_identification_1.pack(anchor='w')
                                isolate_identification_2.pack(anchor='w')
                                isolate_identification_3.pack(anchor='w')
                                isolate_identification_4.pack(anchor='w')
                                isolate_identification_5.pack(anchor='w')
                                isolate_identification_6.pack(anchor='w')

                                if abx_result_dictionary_Length > 6:
                                    isolate_identification_7 = cal.Label(pocket_frame, text="Disc " + str(7) + "." +
                                                                                            abx_result_dictionary[7])
                                    isolate_identification_7.pack(anchor='w')
                                    isolate_identification_7.bind("<Button-1>", lambda value: isolate_selectedToChange(
                                        isolate_identification_7, 7))

                                isolate_identification_1.bind("<Button-1>", lambda value: isolate_selectedToChange(
                                    isolate_identification_1, 1))
                                isolate_identification_2.bind("<Button-1>", lambda value: isolate_selectedToChange(
                                    isolate_identification_2, 2))
                                isolate_identification_3.bind("<Button-1>", lambda value: isolate_selectedToChange(
                                    isolate_identification_3, 3))
                                isolate_identification_4.bind("<Button-1>", lambda value: isolate_selectedToChange(
                                    isolate_identification_4, 4))
                                isolate_identification_5.bind("<Button-1>", lambda value: isolate_selectedToChange(
                                    isolate_identification_5, 5))
                                isolate_identification_6.bind("<Button-1>", lambda value: isolate_selectedToChange(
                                    isolate_identification_6, 6))




                                def saveTestData():
                                    global finishBtn
                                    global cancelBtn2
                                    global pocket_root
                                    filelocationhome = "assets/antibiotics/"
                                    discwriter(abx_result_dictionary, featurefinder(images, masks),filelocationhome)
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
                                              text="Finishes On : " + finishDateTime.strftime("%a, %B %d, %Y")).pack(
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

                                # ImageSet  = ""

                                '''try:
                                    ImageSet = PhotoImage(
                                        file=ImagesPath.get() + patient_id.get() + patient_id.get() + ".jpg")
                                    cal.Label(pocket_frame, image=ImageSet, compound=LEFT).pack()
                                except:
                                    print("Image not found")'''

                                img_scanned_label = cal.Label(pocket_frame, image=imageDisplayScaled, compound=LEFT)
                                img_scanned_label.pack()

                                # print(ImagesPath.get() + patient_id.get() + patient_id.get() + ".jpg")
                                def gotopetriDish_selection():
                                    petriDish_selection()
                                    pocket_root.destroy()

                                bottom_confirm = cal.Frame(pocket_root)
                                proceedButton = cal.Button(bottom_confirm, text="Confirm", width=15, padding=11,
                                                           command=antibioticsCheck)

                                cancelBtn = cal.Button(bottom_confirm, text="Cancel", command=gotopetriDish_selection,
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
                            processBtn = cal.Button(petri_dish_all, text="Proceed", width=29, padding=17,
                                                    command=lambda: moveMotorToCameraPos(0)).pack(pady=3, padx=5)
                            cal.Button(petri_dish_all, text="Cancel", width=29, padding=17,
                                       command=gobackTopetriDish_selection).pack(pady=3, padx=5)
                            process_label = cal.Label(petri_dish_all, text="", foreground="green")
                            process_label.pack()
                        pass

                    pdish_btn1 = cal.Button(petri_dish_frame, text="1 Petri Dish", width=30, padding=30,
                                            command=lambda: dish_count_selected(1))
                    pdish_btn2 = cal.Button(petri_dish_frame, text="2 Petri Dishes", state="disabled",
                                            command=lambda: dish_count_selected(2), width=30, padding=30)
                    cancelButton = cal.Button(petri_dish_frame, text="Cancel", width=30, padding=30,
                                              command=petri_dish_view.destroy)
                    pdish_btn1.pack(pady=10)
                    pdish_btn2.pack(pady=10)
                    cancelButton.pack(pady=10)
                    petri_dish_frame.pack()

            cal.Label(en_samplewindow, text="CHOOSE ISOLATE FOR  ID #[" + patient_id.get() + "]").pack(pady=10)
            serch_1 = cal.Entry(frame_b1, width=35, font=("SEGOE UI", 15))
            serch_1.pack(ipady=10, pady=10)
            isolate_list = Listbox(frame_b1, width=35, font=("SEGOE UI", 15))
            listbox_update(list_sample)
            isolate_list.bind("<<ListboxSelect>>", isolate_selected)
            serch_1.bind("<KeyRelease>", serch_isolate)
            isolate_list.pack()
            cal.Button(frame_b1, text="Proceed", width=33, padding=15, command=petriDish_selection).pack(pady=10)
            cal.Button(frame_b1, text="Add Bacteria", width=33, padding=15, command=add_newBacteria).pack(pady=10)
            cal.Button(frame_b1, text="Cancel", width=33, padding=15, command=en_samplewindow.destroy).pack(pady=10)

            frame_b1.pack()

    scan_entryField = cal.Entry(scan_frame, textvariable=pa_id.get(), width=35,
                                font=("SEGOEUI", 15), justify="center")
    proceed_btn = cal.Button(scan_frame, text="Proceed", width=30, padding=30, command=getscanned)
    clear_btn = cal.Button(scan_frame, text="Clear", width=30, padding=30, command=clear_id)
    cancel_btn = cal.Button(scan_frame, text="Cancel", width=30, padding=30,
                            command=scanPatientID_view.destroy)
    cal.Label(scanPatientID_view, text="SCAN PATIENT CODE", background="white").pack(pady=10)
    scan_entryField.pack(ipady=10)
    scan_entryField.focus()
    proceed_btn.pack(pady=10)
    clear_btn.pack(pady=10)
    cancel_btn.pack(pady=10)
    scan_frame.pack()


def singleTestProgressing(val):
    sample_idprocess = StringVar()
    sample_idprocess.set(val)
    print(sample_idprocess.get())

    arrayDistancescalled = {}
    discscalled = {}
    ImageFile = StringVar()

    retrievedataimg = dbh.cursor()
    retrievedataimg.execute("SELECT imagelocation FROM images  WHERE sample_id = " + str(sample_idprocess.get()) + "")
    for imgCalled in retrievedataimg.fetchall():
        ImageFile.set(imgCalled[0])

    counterDia = 1
    retrievedatadiscs = dbh.cursor()
    retrievedatadiscs.execute(
        "SELECT disc FROM discszonefinder  WHERE sample_id = " + str(sample_idprocess.get()) + "")
    for imgCalled_ in retrievedatadiscs.fetchall():
        discscalled[counterDia] = (imgCalled_[0])[1:-1]
        counterDia += 1

    print(discscalled)

    retrievedataarrayDistances = dbh.cursor()
    retrievedataarrayDistances.execute(
        "SELECT diameter FROM discs  WHERE  sample_id = " + str(sample_idprocess.get()) + "")
    counterDia = 1
    for arrayDia in retrievedataarrayDistances.fetchall():
        arrayDistancescalled[counterDia] = arrayDia[0]
        counterDia += 1

    global zone_distances
    global imageDisplayScaled
    global imgDisplay

    listDict = []
    for key, value in arrayDistancescalled.items():
        listDict.append(value)

    zone_distances = listDict.copy()

    imgDisplay = PhotoImage(file=ImageFile.get())
    B_name = StringVar()
    callData = dbh.cursor()
    patient_fetched_id = StringVar()
    singleRoot = Toplevel(base, background="#FFF")

    callData.execute(
        "SELECT sa.accession_number , ba.bacteria_name FROM samples sa INNER JOIN petri_dish pd INNER JOIN discs ds INNER JOIN antibiotics an INNER JOIN bacteria ba on sa.sample_id=pd.sample_id and ds.abx_id = an.abx_id and sa.sample_id=ds.sample_id and ba.bacteria_id= sa.bacteria_id where sa.sample_id=" + str(
            sample_id.get()) + " and state =1 limit 1")

    for conterPlus in callData.fetchall():
        patient_fetched_id.set(conterPlus[0])
        cal.Label(singleRoot, text="PATIENT ID[" + str(conterPlus[0]) + "] BACTERIA [" + str(
            conterPlus[1]) + "]").pack(
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
    abx_result_labelSwitchInter = {}
    callData_TestDone.execute(
        "SELECT * FROM samples sa INNER JOIN petri_dish pd INNER JOIN discs ds INNER JOIN antibiotics an on sa.sample_id=pd.sample_id and ds.abx_id = an.abx_id and sa.sample_id=ds.sample_id where sa.sample_id=" + str(
            sample_idprocess.get()) + " and state =3")
    counter_abx = 0
    for conterPlus in callData_TestDone.fetchall():
        counter_abx += 1
        B_name.set(conterPlus[16])
        data_m = (B_name.get()[:20] + "...") if len(B_name.get()) > 20 else B_name.get()
        frame_top = cal.Frame(singleRoot, padding=5, relief=SOLID)
        abx_result_label[1] = cal.Label(frame_top, text=str(counter_abx) + ". " + str(data_m),
                                        width=21)
        abx_result_label[1].pack(side="left", padx=3, anchor="w")
        abx_result_label[2] = cal.Label(frame_top, text=str(conterPlus[17]), width=5)
        abx_result_label[2].pack(side="left", padx=3, anchor="w")
        abx_result_labelSwitch[counter_abx] = cal.Label(frame_top, text=str(conterPlus[12]),
                                                        width=4)
        abx_result_labelSwitch[counter_abx].pack(side="left", padx=3, anchor="w")
        abx_result_label[4] = cal.Label(frame_top, text=str(conterPlus[19]), width=4)
        abx_result_label[4].pack(side="left", padx=3, anchor="w")
        abx_result_label[5] = cal.Label(frame_top, text=str(conterPlus[20]), width=4)
        abx_result_label[5].pack(side="left", padx=3, anchor="w")
        abx_result_labelSwitchInter[counter_abx] = cal.Label(frame_top, text="S", width=4)
        abx_result_labelSwitchInter[counter_abx].pack(side="left", padx=3, anchor="w")
        frame_top.pack()

    # print(abx_result_labelSwitch)

    def labelUpdate():
        callData_TestDoneRefresh = dbh.cursor()
        dbh.commit()
        counter_abx_1 = 0
        callData_TestDoneRefresh.execute(
            "SELECT * FROM samples sa INNER JOIN petri_dish pd INNER JOIN discs ds INNER JOIN antibiotics an on sa.sample_id=pd.sample_id and ds.abx_id = an.abx_id and sa.sample_id=ds.sample_id where sa.sample_id=" + str(
                sample_id.get()) + " and state =1")
        for conterPlusPlus in callData_TestDoneRefresh.fetchall():
            counter_abx_1 += 1
            abx_result_labelSwitch[counter_abx_1]["text"] = str(conterPlusPlus[12])

    def editResult(a):
        global imageDisplayScaled
        global imgDisplay

        editRoot = Toplevel(base, background="#FFF")
        cal.Label(editRoot, text="EDIT RESULTS FOR PATIENT ID #[" + str(
            patient_fetched_id.get()) + "]").pack(pady=10)

        def increasing_circle_loop(val_reduced):
            valInt = IntVar()
            valInt.set(val_reduced)

            global _edit
            global imgDisplayII
            global edit_BoxValue
            inProgress = Toplevel(base)
            cal.Label(inProgress, text="Executing please wait...").pack()
            print("Button +")
            global zone_distances
            zone_distances = zoneadjuster(zone_distances, valInt.get(), True, 1)
            circledrawer(ImageFile.get(), zone_distances, discscalled)

            arrayD = zone_distances.copy()
            arrayDist = zone_distances.copy()
            arrayDist[:] = [x * 0.0307692 for x in arrayD]
            count = -1
            count_12 = 0
            arr = None
            vals = {}
            insertIntoDiameter = dbh.cursor()
            checkAbx = dbh.cursor()
            checkAbx.execute(
                "SELECT disc_id  FROM discs WHERE sample_id =" + str(sample_id.get()) + "")

            for x in arrayDist:
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
            shutil.copy(imglocationhome + "newzones" + str(sample_id.get()) + ".png", ImageFile.get())
            imgDisplayII = PhotoImage(file=imglocationhome + "newzones" + str(sample_id.get()) + ".png")
            labelUpdate()
            photo_edit.config(image=imgDisplayII)
            _editLabel.config(image=imgDisplayII)

        def imageResfresh():
            editRoot.destroy()
            global imgDisplayII
            global photo_edit
            shutil.copy(imglocationhome + "newzones" + str(sample_id.get()) + ".png", ImageFile.get())
            imgDisplayII = PhotoImage(file=imglocationhome + "newzones" + str(sample_id.get()) + ".png")
            labelUpdate()
            _editLabel.config(image=imgDisplayII)

        def reducing_circle_loop(val_reduced):
            print(discscalled)
            valInt = IntVar()
            valInt.set(val_reduced)

            global _edit
            global imgDisplayII
            global edit_BoxValue
            inProgress = Toplevel(base)
            cal.Label(inProgress, text="Executing please wait...").pack()
            print("Button -")
            global zone_distances
            zone_distances = zoneadjuster(zone_distances, valInt.get(), False, 1)
            circledrawer(ImageFile.get(), zone_distances, discscalled)
            # print(zone_distances)

            arrayD = zone_distances.copy()
            arrayDist = zone_distances.copy()
            arrayDist[:] = [x * 0.0307692 for x in arrayD]

            count = -1
            count_12 = 0
            arr = None
            vals = {}
            insertIntoDiameter = dbh.cursor()
            checkAbx = dbh.cursor()
            checkAbx.execute(
                "SELECT disc_id  FROM discs WHERE sample_id =" + str(sample_id.get()) + "")

            for x in arrayDist:
                count += 1
                count_12 += 1
                arr = round(arrayDist[count])
                vals[count_12] = arr
                # print(arr)

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
            shutil.copy(imglocationhome + "newzones" + str(sample_id.get()) + ".png", ImageFile.get())
            imgDisplayII = PhotoImage(file=imglocationhome + "newzones" + str(sample_id.get()) + ".png")
            labelUpdate()
            photo_edit.config(image=imgDisplayII)
            _editLabel.config(image=imgDisplayII)

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
        if abx_result_dictionary_LengthGlobal.get() == 6:
            discsValue.set("1 2 3 4 5 6")
        else:
            discsValue.set("1 2 3 4 5 6 7")

        edit_BoxValue = cal.Combobox(editRoot, width=30, values=discsValue.get(),
                                     state="readonly")
        increaseDistance.bind("<Button-1>",
                              lambda val: increasing_circle_loop(edit_BoxValue.get()))
        reduceDistance.bind("<Button-1>", lambda val: reducing_circle_loop(edit_BoxValue.get()))
        edit_BoxValue.current("1")

        edit_BoxValue.pack(pady=10, ipady=3)

        frame_edit = cal.Frame(editRoot, padding=3)
        approveBtn_result = cal.Button(frame_edit, text="Confirm", command=imageResfresh,
                                       width=10, padding=10)
        cancelBtn_result = cal.Button(frame_edit, text="Cancel", width=10, padding=10,
                                      command=editRoot.destroy)
        approveBtn_result.pack(side=LEFT)
        # cancelBtn_result.pack(side=LEFT)
        frame_edit.pack()

    _editLabel = cal.Label(singleRoot, image=imgDisplay)
    _editLabel.bind("<Button-1>", editResult)
    _editLabel.pack()
    lower_frame = cal.Frame(singleRoot, padding=5)
    approveBtn = cal.Button(lower_frame, text="Approve", padding=20, width=20)
    cancelBtn = cal.Button(lower_frame, text="Cancel", padding=20, width=20)
    approveBtn.pack(side=LEFT)
    cancelBtn.pack(side=LEFT)
    approveBtn.bind("<Button-1>", editResult)
    lower_frame.pack()


def compledTests():
    pocket_stateCount = IntVar()
    completedTestsRoot = Toplevel(base, background="#FFF")
    upperFrame = cal.Frame(completedTestsRoot, padding=5)
    test_in_progress = dbh.cursor()
    dbh.commit()
    test_in_progress.execute("SELECT COUNT(*) FROM petri_dish WHERE state=3")
    for count in test_in_progress.fetchall():
        pocket_stateCount.set(count[0])
    print(pocket_stateCount.get())

    pocket_stateCountNumber = IntVar()
    callData_Test_Number = dbh.cursor()
    callData_Test_One = dbh.cursor()
    assesionNumber = StringVar()

    def completeResult():
        pass

    if pocket_stateCount.get() == 0:
        pocketRoot_Frame = cal.Frame(upperFrame, padding=15, relief=SOLID)
        cal.Label(completedTestsRoot, text="NO COMPLETED TESTS AT THE MOMENT", padding=20, relief=SOLID).pack(
            pady=20)
        pocketRoot_Frame.pack()


    elif pocket_stateCount.get() > 0:
        completed_label = {}
        countDone = 0
        callData_Test_Number.execute("SELECT dish_id FROM petri_dish  WHERE state = 3")
        for count_1 in callData_Test_Number.fetchall():
            pocket_stateCountNumber.set(count_1[0])
            # print(pocket_stateCountNumber.get())
            callData_Test_One.execute(
                "SELECT timestampdiff(hour,pd.endTime,now()) as durationLeft,sa.accession_number,pd.dish_id,pd.sample_id FROM samples sa INNER JOIN petri_dish pd on sa.sample_id=pd.sample_id where pd.dish_id =" + str(
                    pocket_stateCountNumber.get()) + " and state =3 and pd.dish_id=1 limit 1 ")
            for cnt in range(pocket_stateCount.get()):
                for count in callData_Test_One.fetchall():
                    countDone += 1
                    assesionNumber.set(str(count[1]))
                    cal.Frame(upperFrame).pack(pady=5)
                    pocketRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    patient_idRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    cal.Label(patient_idRoot_Frame, text="Assesion Number ", width=20).pack(side="left", padx=10,
                                                                                            anchor="w")
                    cal.Label(patient_idRoot_Frame, text=str(count[1]), width=20).pack(side="left", padx=10, anchor="w")
                    completed_label[countDone] = cal.Label(patient_idRoot_Frame, text="VIEW", width=10,
                                                           foreground="green")
                    completed_label[countDone].pack(side="left", padx=10, anchor="w")
                    completed_label[countDone].bind("<Button-1>", lambda val: singleTestProgressing(count[3]))
                    pocketRoot_Frame.pack()
                    patient_idRoot_Frame.pack()
                    upperFrame.pack(pady=2)

        countDone = 0
        dbh.commit()
        callData_Test_Number.execute("SELECT dish_id FROM petri_dish  WHERE state = 3")
        for count_1 in callData_Test_Number.fetchall():
            pocket_stateCountNumber.set(count_1[0])
            # print(pocket_stateCountNumber.get())
            callData_Test_One.execute(
                "SELECT timestampdiff(hour,pd.endTime,now()) as durationLeft,sa.accession_number,pd.dish_id,pd.sample_id FROM samples sa INNER JOIN petri_dish pd on sa.sample_id=pd.sample_id where pd.dish_id =" + str(
                    pocket_stateCountNumber.get()) + " and (state =3 and pd.dish_id=2) ")
            for cnt in range(pocket_stateCount.get()):
                for countPlus in callData_Test_One.fetchall():
                    countDone += 1
                    assesionNumber.set(str(countPlus[1]))
                    cal.Frame(upperFrame).pack(pady=5)
                    pocketRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    patient_idRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    cal.Label(patient_idRoot_Frame, text="Assesion Number ", width=20).pack(side="left", padx=10,
                                                                                            anchor="w")
                    cal.Label(patient_idRoot_Frame, text=str(countPlus[1]), width=20).pack(side="left", padx=10,
                                                                                           anchor="w")
                    completed_label2 = cal.Label(patient_idRoot_Frame, text="VIEW", width=10, foreground="green")
                    completed_label2.pack(side="left", padx=10, anchor="w")
                    completed_label2.bind("<Button-1>", lambda val: singleTestProgressing(countPlus[3]))
                    pocketRoot_Frame.pack()
                    patient_idRoot_Frame.pack()
                    upperFrame.pack(pady=2)

        countDone = 0
        dbh.commit()
        callData_Test_Number.execute("SELECT dish_id FROM petri_dish  WHERE state = 3")
        for count_1 in callData_Test_Number.fetchall():
            pocket_stateCountNumber.set(count_1[0])
            # print(pocket_stateCountNumber.get())
            callData_Test_One.execute(
                "SELECT timestampdiff(hour,pd.endTime,now()) as durationLeft,sa.accession_number,pd.dish_id,pd.sample_id FROM samples sa INNER JOIN petri_dish pd on sa.sample_id=pd.sample_id where pd.dish_id =" + str(
                    pocket_stateCountNumber.get()) + " and (state =3 and pd.dish_id=3) ")
            for cnt in range(pocket_stateCount.get()):
                for countPlus2 in callData_Test_One.fetchall():
                    countDone += 1
                    assesionNumber.set(str(countPlus2[1]))
                    cal.Frame(upperFrame).pack(pady=5)
                    pocketRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    patient_idRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    cal.Label(patient_idRoot_Frame, text="Assesion Number ", width=20).pack(side="left", padx=10,
                                                                                            anchor="w")
                    cal.Label(patient_idRoot_Frame, text=str(countPlus2[1]), width=20).pack(side="left", padx=10,
                                                                                            anchor="w")
                    completed_label2 = cal.Label(patient_idRoot_Frame, text="VIEW", width=10, foreground="green")
                    completed_label2.pack(side="left", padx=10, anchor="w")
                    completed_label2.bind("<Button-1>", lambda val: singleTestProgressing(countPlus2[3]))
                    pocketRoot_Frame.pack()
                    patient_idRoot_Frame.pack()
                    upperFrame.pack(pady=2)

        countDone = 0
        dbh.commit()
        callData_Test_Number.execute("SELECT dish_id FROM petri_dish  WHERE state = 3")
        for count_1 in callData_Test_Number.fetchall():
            pocket_stateCountNumber.set(count_1[0])
            # print(pocket_stateCountNumber.get())
            callData_Test_One.execute(
                "SELECT timestampdiff(hour,pd.endTime,now()) as durationLeft,sa.accession_number,pd.dish_id,pd.sample_id FROM samples sa INNER JOIN petri_dish pd on sa.sample_id=pd.sample_id where pd.dish_id =" + str(
                    pocket_stateCountNumber.get()) + " and (state =3 and pd.dish_id=3) ")
            for cnt in range(pocket_stateCount.get()):
                for countPlus3 in callData_Test_One.fetchall():
                    countDone += 1
                    assesionNumber.set(str(countPlus3[1]))
                    cal.Frame(upperFrame).pack(pady=5)
                    pocketRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    patient_idRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    cal.Label(patient_idRoot_Frame, text="Assesion Number ", width=20).pack(side="left", padx=10,
                                                                                            anchor="w")
                    cal.Label(patient_idRoot_Frame, text=str(countPlus3[1]), width=20).pack(side="left", padx=10,
                                                                                            anchor="w")
                    completed_label2 = cal.Label(patient_idRoot_Frame, text="VIEW", width=10, foreground="green")
                    completed_label2.pack(side="left", padx=10, anchor="w")
                    completed_label2.bind("<Button-1>", lambda val: singleTestProgressing(countPlus3[3]))
                    pocketRoot_Frame.pack()
                    patient_idRoot_Frame.pack()
                    upperFrame.pack(pady=2)

    home_resultBtn = cal.Button(completedTestsRoot, text="Go Back", padding=10, width=23,
                                command=completedTestsRoot.destroy)
    home_resultBtn.pack()


def resultReport():
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
                "SELECT timestampdiff(hour,now(),pd.endTime) as durationLeft,sa.accession_number,pd.dish_id,pd.sample_id FROM samples sa INNER JOIN petri_dish pd on sa.sample_id=pd.sample_id where pd.dish_id =" + str(
                    pocket_stateCountNumber.get()) + " and state =1 ")
            for cnt in range(pocket_stateCount.get()):
                for count in callData_Test_One.fetchall():
                    countsize += 1
                    assesionNumber.set(str(count[1]))
                    # print(assesionNumber.get())
                    cal.Frame(upperFrame).pack(pady=5)
                    pocketRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)

                    cal.Label(pocketRoot_Frame, text="    POCKET  NUMBER " + str(count[2]) + "", width=20).pack(
                        side="left", padx=10, anchor="w")
                    patient_idRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    cal.Label(patient_idRoot_Frame, text="Assesion #", width=20).pack(side="left", padx=10, anchor="w")
                    patient_Ids[countsize] = cal.Label(patient_idRoot_Frame, text=str(count[1]), width=20)
                    patient_Ids[countsize].pack(side="left", padx=10, anchor="w")
                    letfTimeRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    cal.Label(letfTimeRoot_Frame, text="Time Left", width=20).pack(side="left", padx=10, anchor="w")
                    timeLeftDifference.set(count[0])
                    patient_Ids[countsize] = cal.Label(letfTimeRoot_Frame,
                                                       text=str(timeLeftDifference.get()) + " Hours", width=20)
                    patient_Ids[countsize].pack(side="left", padx=10, anchor="w")
                    statusRoot_Frame = cal.Frame(upperFrame, padding=5, relief=SOLID)
                    cal.Label(statusRoot_Frame, text="Status", width=20).pack(side="left", padx=10, anchor="w")

                    if timeLeftDifference.get() == 0:

                        def singleTestProgress(val):
                            sample_id.set(val)

                            arrayD = arrayDistances.copy()
                            arrayDist = arrayDistances.copy()
                            arrayDist[:] = [x * 0.0307692 for x in arrayD]
                            # print((arrayDist))
                            count = -1
                            count_12 = 0
                            arr = None
                            vals = {}
                            insertIntoDiameter = dbh.cursor()
                            checkAbx = dbh.cursor()
                            checkAbx.execute("SELECT disc_id  FROM discs WHERE sample_id =" + str(sample_id.get()) + "")

                            for x in arrayDist:
                                count += 1
                                count_12 += 1
                                arr = round(arrayDist[count])
                                vals[count_12] = arr
                                # print("New array "+str(arr))

                            count_12 = 0
                            count = -1
                            valueInsert = StringVar()
                            for abx_sample_id, coount in zip(vals, checkAbx.fetchall()):
                                count_12 += 1
                                count += 1
                                valueInsert.set(str(vals[count_12]))
                                print(valueInsert.get())
                                dbh.commit()
                                try:
                                    insertIntoDiameter.execute(
                                        "UPDATE discs set diameter=" + str(
                                            valueInsert.get()) + " WHERE sample_id=" + str(
                                            sample_id.get()) + " and disc_id =" + str(coount[0]) + "")
                                    # print("inserted" + str(vals[count_12]))
                                    # print(coount[0])
                                    dbh.commit()
                                except:
                                    print("Failed to insert")
                                    dbh.rollback()

                                    # print("This is the dictionary of discs "+str(vals))

                            global zone_distances
                            global imageDisplayScaled
                            global imgDisplay
                            #                            global arrayDistances
                            zone_distances = arrayDistances
                            imgDisplay = PhotoImage(file=newImageFile)
                            B_name = StringVar()
                            singleRoot = Toplevel(base, background="#FFF")
                            callId = dbh.cursor()
                            callId.execute(
                                "SELECT * FROM samples sa inner join bacteria ba on sa.bacteria_id = ba.bacteria_id where sa.sample_id=" + str(
                                    sample_id.get()) + " limit 1")
                            for id in callId.fetchall():
                                cal.Label(singleRoot,
                                          text="PATIENT ID[" + str(id[1]) + "] BACTERIA [" + str(id[5]) + "]").pack(
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
                                    sample_id.get()) + " and state =1")
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

                            def labelUpdate():
                                callData_TestDoneRefresh = dbh.cursor()
                                dbh.commit()
                                counter_abx_1 = 0
                                callData_TestDoneRefresh.execute(
                                    "SELECT * FROM samples sa INNER JOIN petri_dish pd INNER JOIN discs ds INNER JOIN antibiotics an on sa.sample_id=pd.sample_id and ds.abx_id = an.abx_id and sa.sample_id=ds.sample_id where sa.sample_id=" + str(
                                        sample_id.get()) + " and state =1")
                                for conterPlusPlus in callData_TestDoneRefresh.fetchall():
                                    counter_abx_1 += 1
                                    abx_result_labelSwitch[counter_abx_1]["text"] = str(conterPlusPlus[12])
                                    if conterPlusPlus[12] >= conterPlusPlus[19]:
                                        abx_result_labeldec[counter_abx_1]["text"] = "S"
                                    elif conterPlusPlus[12] < conterPlusPlus[20]:
                                        abx_result_labeldec[counter_abx_1]["text"] = "R"
                                    else:
                                        abx_result_labeldec[counter_abx_1]["text"] = "I"

                            def editResult(a):

                                global imageDisplayScaled
                                global imgDisplay

                                editRoot = Toplevel(base, background="#FFF")
                                callId = dbh.cursor()
                                callId.execute(
                                    "SELECT * FROM samples sa inner join bacteria ba on sa.bacteria_id = ba.bacteria_id where sa.sample_id=" + str(
                                        sample_id.get()) + " limit 1")
                                for id in callId.fetchall():
                                    cal.Label(editRoot, text="EDIT RESULTS FOR PATIENT ID #[" + str(id[1]) + "]").pack(
                                        pady=10)

                                def increasing_circle_loop(val_reduced):
                                    valInt = IntVar()
                                    valInt.set(val_reduced)

                                    global _edit
                                    global imgDisplayII
                                    global edit_BoxValue
                                    global imageDisplayScaled
                                    inProgress = Toplevel(base)
                                    cal.Label(inProgress, text="Executing please wait...").pack()
                                    print("Button +")
                                    global zone_distances
                                    zone_distances = zoneadjuster(zone_distances, valInt.get(), True, 1)
                                    circledrawer(old_img, zone_distances, discs)
                                    # print(zone_distances)

                                    arrayD = zone_distances.copy()
                                    arrayDist = zone_distances.copy()

                                    arrayDist[:] = [x * 0.0307692 for x in arrayD]
                                    # print("New array")
                                    # print((arrayDist))
                                    count = -1
                                    count_12 = 0
                                    arr = None
                                    vals = {}
                                    insertIntoDiameter = dbh.cursor()
                                    checkAbx = dbh.cursor()
                                    checkAbx.execute(
                                        "SELECT disc_id  FROM discs WHERE sample_id =" + str(sample_id.get()) + "")

                                    for x in arrayDist:
                                        count += 1
                                        count_12 += 1
                                        arr = math.floor(arrayDist[count])
                                        vals[count_12] = arr
                                        # print(arr)

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
                                            # print("inserted" + str(vals[count_12]))
                                            # print(coount[0])
                                            dbh.commit()
                                        except:
                                            print("Failed to insert")
                                            dbh.rollback()

                                            # print(vals)

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

                                def reducing_circle_loop(val_reduced):
                                    valInt = IntVar()
                                    valInt.set(val_reduced)

                                    global _edit
                                    global imgDisplayII
                                    global edit_BoxValue
                                    global imageDisplayScaled
                                    inProgress = Toplevel(base)
                                    cal.Label(inProgress, text="Executing please wait...").pack()
                                    print("Button +")
                                    global zone_distances
                                    zone_distances = zoneadjuster(zone_distances, valInt.get(), False, 1)
                                    circledrawer(old_img, zone_distances, discs)
                                    # print(zone_distances)

                                    arrayD = zone_distances.copy()
                                    arrayDist = zone_distances.copy()
                                    arrayDist[:] = [x * 0.0307692 for x in arrayD]
                                    # print("New array")
                                    # print((arrayDist))
                                    count = -1
                                    count_12 = 0
                                    arr = None
                                    vals = {}
                                    insertIntoDiameter = dbh.cursor()
                                    checkAbx = dbh.cursor()
                                    checkAbx.execute(
                                        "SELECT disc_id  FROM discs WHERE sample_id =" + str(sample_id.get()) + "")

                                    for x in arrayDist:
                                        count += 1
                                        count_12 += 1
                                        arr = math.floor(arrayDist[count])
                                        vals[count_12] = arr
                                        # print(arr)

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
                                            # print("inserted" + str(vals[count_12]))
                                            # print(coount[0])
                                            dbh.commit()
                                        except:
                                            print("Failed to insert")
                                            dbh.rollback()

                                            # print(vals)

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
                                    shutil.copy(imgDisplay,
                                                imglocationhome + "newzones" + str(sample_id.get()) + ".png")
                                    imgDisplay = PhotoImage(file=imgDisplay)
                                    photo_edit = cal.Label(editRoot, image=imgDisplay)
                                    photo_edit.pack()
                                except:
                                    pass
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
                                if abx_result_dictionary_LengthGlobal.get() == 6:
                                    discsValue.set("1 2 3 4 5 6")
                                else:
                                    discsValue.set("1 2 3 4 5 6 7")

                                edit_BoxValue = cal.Combobox(editRoot, width=30, values=discsValue.get(),
                                                             state="readonly")
                                increaseDistance.bind("<Button-1>",
                                                      lambda val: increasing_circle_loop(edit_BoxValue.get()))
                                reduceDistance.bind("<Button-1>", lambda val: reducing_circle_loop(edit_BoxValue.get()))
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
                            cancelBtn = cal.Button(lower_frame, text="Cancel", padding=20, command=singleRoot.destroy,
                                                   width=20)
                            approveBtn.pack()
                            lower_frame.pack()

                        progress_label[1] = cal.Label(statusRoot_Frame, text="COMPLETED", width=20, foreground="green")
                        progress_label[1].pack(side="left", padx=10, anchor="w")
                        progress_label[1].bind("<Button-1>", lambda val: singleTestProgress(str(count[3])))



                    else:
                        progress_label[1] = cal.Label(statusRoot_Frame, text="IN PROGRESS", width=20, foreground="blue")
                        progress_label[1].pack(side="left", padx=10, anchor="w")

                    pocketRoot_Frame.pack()
                    patient_idRoot_Frame.pack()
                    letfTimeRoot_Frame.pack()
                    statusRoot_Frame.pack()

    upperFrame.pack(pady=2)

    home_resultBtn = cal.Button(resultRoot, text="Go Back", padding=10, width=23, command=resultRoot.destroy)
    home_resultBtn.pack()


if __name__ == '__main__':
    base = Tk()
    # base.attributes("-fullscreen",True)

    # Database Connection
    # dbh = MySQLdb.connect(host="localhost", db="incubator", user="root", passwd="0000")

    get_all_bacterial = dbh.cursor()
    save_to_table = dbh.cursor()

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
    #  zonefinderInitializer()

    patient_Ids = {}
    abx_dose_label = {}
    abx_result_label = {}
    photo_edit = cal.Label()
    progress_label = {}
    processLabel = cal.Label()
    edit_BoxValue = None
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
    base.config(background="white")
    base.title("New")

    get_all_abx = dbh.cursor()
    get_all_abx.execute("select * from antibiotics")
    abx_list1 = get_all_abx.fetchall()
    abx_list_ = StringVar()
    abx_list_.set(abx_list1)

    list_sample_abx = list()
    for row_abx in abx_list1:
        list_sample_abx.append(str(row_abx[1]))

    titleBar = cal.Label(base, text="INCUBATOR UI DESIGN PROTOTYPE")
    titleBar.pack(pady=10)

    dash_frame = cal.Frame(base, relief=SOLID, padding=20)

    cal.Button(dash_frame, text="New Sample Test", width=30, padding=30, command=scanPatientID).pack(pady=15)
    cal.Button(dash_frame, text="Result Progress", command=resultReport, width=30, padding=30).pack(pady=15)
    cal.Button(dash_frame, text="Completed Tests", command=compledTests, width=30, padding=30).pack(pady=15)
    cal.Button(dash_frame, text="Print agar Label ", width=30, padding=30, command=printAgarLabel).pack(pady=15)
    exit_system = cal.Button(dash_frame, text=" Exit System", width=30, padding=30, command=base.destroy).pack(pady=15)

    finishDateTime = datetime.datetime.now() + datetime.timedelta(hours=20)
    timeStample = finishDateTime.fromtimestamp(time.time()).strftime("%A")

    timeNow = cal.Button(dash_frame, text="Processing please wait...", width=30, padding=30)
    dash_frame.pack()


    def timeLoop():
        titleBar["text"] = "LAB INCUBATOR DASHBOARD - " + datetime.datetime.today().strftime("%T")
        base.after(100, timeLoop)


    timeLoop()

    base.mainloop()