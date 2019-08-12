import datetime
import faulthandler
import json
import os
import os.path
import shutil
import sqlite3
import threading
import time
import urllib
import urllib.request
from tkinter import *
from tkinter import ttk as cal
from tkinter.font import nametofont

import requests
from PIL import ImageTk

from openAMR import *

faulthandler.enable()


def clear_field(field):
    field.delete(0, "end")
    field.focus()


printpath = "sh /home/user/print.sh "


def printtext():
    def print_text(text, count=0):
        for _ in range(int(count)):
            f = open("pname.lbl", "w+")
            f.write('\nN\nWY\n')
            f.write('q305\n')
            f.write('Q101,022\n')
            f.write('A50,60,0,3,1,1,N,'),
            f.write('"' + str(text.replace("$", "")) + '"\n')
            f.write('P1\n')
            f.close()

            os.system(printpath)

    def print_barcode(code, count=0):
        for _ in range(int(count)):
            dateformat = datetime.datetime.strptime(str(datetime.datetime.now().date()), '%Y-%m-%d').strftime(
                '%d-%m-%Y')
            f = open("code.lbl", "w+")
            f.write('\nN\nWY\n')
            f.write('q305\n')
            f.write('Q101,022\n')
            f.write('B50,0,0,1,2,2,20,B,'),
            f.write('"' + str(code.replace("$", "")) + '"\n')
            f.write('A50,60,0,3,1,1,N,'),
            f.write('"' + str(dateformat) + '"\n')
            f.write('P1\n')
            f.close()
            os.system(printpath)

    # creating the print barcode and print label window
    agarRoot = Toplevel(base)
    set_window_icon_and_make_fullscreen(agarRoot)
    baseframe = cal.Frame(agarRoot, padding=20)
    agar_frame = cal.Frame(baseframe)
    f_left = cal.Frame(agar_frame, relief=SOLID, padding=10)
    f_right = cal.Frame(agar_frame, relief=SOLID, padding=10)

    cal.Label(f_left, text="Print Barcode ").pack(pady=10)
    lb = cal.LabelFrame(f_left, text="Scan Accession Number")
    en_barcode = cal.Entry(lb, width=25, justify="center")
    en_barcode.pack(ipady=10)
    en_barcode.bind("<FocusIn>", lambda _, field=en_barcode: clear_field(field))
    lb.pack()

    lb = cal.LabelFrame(f_left, text="Number of Labels")
    en_bnt = cal.Entry(lb, width=25, justify="center")
    en_bnt.pack(ipady=10)
    en_bnt.insert(0, "1")
    en_bnt.bind("<FocusIn>", lambda _, field=en_bnt: clear_field(field))
    lb.pack()

    bc_frame = cal.Frame(f_left)
    cal.Button(bc_frame, text="Print Barcode Label", padding=20, width=22,
               command=lambda: print_barcode(en_barcode.get(), en_bnt.get())).pack(pady=10, side=LEFT)
    bc_frame.pack()

    cal.Label(f_right, text="Print Label Text ").pack(pady=10)
    lb = cal.LabelFrame(f_right, text="Enter Label Text")
    en_lbl = cal.Entry(lb, width=25, justify="center")
    en_lbl.pack(ipady=10)
    # en_lbl.insert(0, "1234567890")
    en_lbl.bind("<FocusIn>", lambda _, field=en_lbl: clear_field(field))
    lb.pack()

    lb = cal.LabelFrame(f_right, text="Number of Labels")
    en_lcnt = cal.Entry(lb, width=25, justify="center")
    en_lcnt.pack(ipady=10)
    en_lcnt.insert(0, "1")
    en_lcnt.bind("<FocusIn>", lambda _, field=en_lcnt: clear_field(field))
    lb.pack()

    tl_frame = cal.Frame(f_right)
    cal.Button(tl_frame, text="Print Label Text", padding=20, width=22,
               command=lambda: print_text(en_lbl.get(), en_lcnt.get())).pack(pady=10,
                                                                             side=LEFT)  # callling the print barcode function on line 40
    tl_frame.pack()

    f_left.pack(side=LEFT)
    f_right.pack(side=LEFT, padx=20)
    agar_frame.pack()
    cal.Button(baseframe, padding=20, width=10, image=backImg, command=agarRoot.destroy).pack(side=LEFT, pady=10)
    baseframe.pack()


def sQLiteconnection():
    try:
        return sqlite3.connect("assets/sqlitedb/openamr.db").cursor()
    except Exception as e_db:
        print(e_db)


def sQLitInsert():
    while True:
        try:
            return sqlite3.connect("assets/sqlitedb/openamr.db")
        except Exception as e_db:
            print(e_db)


def sQLitQuery(sqlitequery):
    try:
        sQLiteconnection().execute(sqlitequery)
    except Exception as e_table:
        print(e_table)


def closewindows():
    global isolatewindow, valHolder
    isolatewindow.destroy()
    valHolder.destroy()


def sQLitQuery0(db, sqlitequery):
    try:
        db.execute(sqlitequery)
    except Exception as e_table:
        print(e_table)
    finally:
        db.close()


def clear_Input(entryfield):
    entryfield.delete(0, 'end')
    entryfield.focus()


def exceptionprint(name, e_name):
    pass


def returnTrue(filename, param):
    while True:
        try:
            _n1 = http_get_request(filename, param)
            if _n1.status_code == 200:
                for _i in _n1.text:
                    if _i == "1":
                        return True
            elif _n1.status_code != 200:
                transactionReset()
        except Exception as e_rt:
            exceptionprint("returnTrue", e_rt)


def http_request_return_json_or_boolean(file, param, return_data=True):
    while True:
        try:
            _n1 = http_get_request(file, param)
            if _n1.status_code == 200:
                if return_data:
                    return _n1
                elif not return_data:
                    for _i in _n1.text:
                        if _i == "1":
                            return True
                        elif _i != "1":
                            return False
            elif _n1.status_code != 200:
                if not return_data:
                    transactionReset()
        except Exception as e_rt:
            exceptionprint("http_request_return_json_or_boolean", e_rt)


def set_window_icon_and_make_fullscreen(window):
    # window.state("zoomed")
    # window.attributes('-fullscreen', True)
    try:
        window.iconbitmap(icoloc)
    except Exception as e_win:
        exceptionprint("set_window_icon_and_make_fullscreen", e_win)


# noinspection PyBroadException
def itemselected(event, entryfield, condition=None):
    global global_isolate_name, abxname, global_unique_code, global_sample_code
    entryfield.delete(0, 'end')
    try:
        entryfield.insert(0, event.widget.get(event.widget.curselection()))
        if condition == 1:
            global_isolate_name = event.widget.get(event.widget.curselection())
        elif not condition:
            abxname = event.widget.get(event.widget.curselection())
        elif condition == 2:
            global_sample_code = event.widget.get(event.widget.curselection())
        else:
            global_unique_code = event.widget.get(event.widget.curselection())
    except Exception as _:
        pass


def toListbox(val, listbox, mydata, sort=True):
    value_abx = val.widget.get()
    value_abx = value_abx.strip().lower()
    if value_abx == '':
        data = mydata

    else:
        data = []
        for item in mydata:
            if not sort:
                if value_abx in item:
                    data.append(item)
            elif sort:
                if value_abx in item.lower():
                    data.append(item)

    listboxupdate(data, listbox, False)


def listboxupdate(data, listbox, lower=True):
    listbox.delete(0, 'end')
    if not lower:
        for item in data:
            listbox.insert('end', item)
    elif lower:
        data = sorted(data, key=str.lower)
        for item in data:
            listbox.insert('end', item)


# noinspection PyUnresolvedReferences
def http_get_request(filename, param):
    while True:
        try:
            http_request = requests.post(domain + str(filename) + ".php", param, timeout=10)
            if http_request.status_code == 200:
                return http_request
        except Exception as e_net:
            exceptionprint("http_get_request", e_net)


def transactionReset():
    returnTrue("transactionTerminate", {})


# noinspection PyShadowingNames
def downloadImg(global_sample_id_from_database, imgnameftp, imgname, condition, downfactor=.0):
    while True:
        try:

            imgurldown = url + "img/" + str(imgnameftp) + str(
                global_sample_id_from_database) + ".png"
            imgrequest = urllib.request.urlopen(imgurldown)
            downloadimg = np.asarray(bytearray(imgrequest.read()), dtype=np.uint8)
            downimg = cv2.imdecode(downloadimg, -1)

            if not condition:
                cv2.imwrite(imglocationhome + str(imgname) + str(global_sample_id_from_database) + ".png", downimg)
            if condition:
                cv2.imwrite(imglocationhome + str(imgname) + str(global_sample_id_from_database) + ".png",
                            cv2.resize(downimg, (0, 0), fx=downfactor, fy=downfactor))
            break
        except Exception as er_img:
            exceptionprint("downloadImg", er_img)


def setprogress(status, filename="setTestStatus"):
    while True:
        http_request_return_json_or_boolean(file=filename, param={"status": status}, return_data=False)
        return


def setlink(status, filename="setLinkStatus"):
    while True:
        if http_request_return_json_or_boolean(file=filename, param={"link": status}, return_data=False):
            return


threadInstance = None


def result_report():
    btns = {}

    # noinspection PyShadowingNames
    def singleTestProgressing(global_sample_id_from_database):
        global dictionary_of_discs_from_database, dictionary_of_association_from_database
        global global_top_window_tkinter, generalOpt, global_bacteria_id_from_database, global_unique_code, global_isolate_name, generals

        global_top_window_tkinter = Toplevel(base)
        set_window_icon_and_make_fullscreen(global_top_window_tkinter)
        cFrame = cal.Frame(global_top_window_tkinter, padding=5, relief=SOLID)

        cal.Label(global_top_window_tkinter,
                  text="ACCESSION # - " + str(global_unique_code) + "  |  BACTERIA -  " + str(
                      global_isolate_name)).pack(pady=10)
        generalOpt = cal.Frame(cFrame, padding=5, relief=SOLID)
        cal.Label(generalOpt, text="Antibiotics", width=20).pack(side="left", padx=3,
                                                                 anchor="w")
        cal.Label(generalOpt, text="Code", width=7).pack(side="left", padx=3, anchor="w")
        cal.Label(generalOpt, text="Dose", width=10).pack(side="left", padx=3, anchor="w")
        cal.Label(generalOpt, text="Zones (mm)", width=10).pack(side="left", padx=3, anchor="w")
        cal.Label(generalOpt, text="R<", width=5).pack(side="left", padx=3, anchor="w")
        cal.Label(generalOpt, text="S≥", width=5).pack(side="left", padx=3, anchor="w")
        cal.Label(generalOpt, text="Interpretation", width=15).pack(side="left", padx=3,
                                                                    anchor="w")
        generalOpt.pack()

        i = 0
        generalOpt = {}

        try:
            btns[0]["state"] = "enabled"
            btns[1]["state"] = "enabled"
        except Exception as _wd:
            exceptionprint("widgets", _wd)

        for dt in dictionary_of_discs_from_database:
            resultFrame = cal.Frame(cFrame, padding=5, relief=SOLID)
            cal.Label(resultFrame, width=20, text=str(i + 1) + ". " + str(
                dictionary_of_discs_from_database[dt][0][:18] + "... "
                if len(dictionary_of_discs_from_database[dt][0]) > 18 else
                dictionary_of_discs_from_database[dt][0])).pack(side="left",
                                                                padx=3,
                                                                anchor="w")

            cal.Label(resultFrame, text=str(dictionary_of_discs_from_database[dt][1]),
                      width=7).pack(
                side="left",
                padx=3,
                anchor="w")

            cal.Label(resultFrame, text=str(dictionary_of_discs_from_database[dt][2]),
                      width=10).pack(
                side="left",
                padx=3,
                anchor="w")
            generalOpt[i + 20] = cal.Label(resultFrame,
                                           text=str(dictionary_of_discs_from_database[dt][3]),
                                           width=10)
            generalOpt[i + 20].pack(side="left", padx=3, anchor="w")
            cal.Label(resultFrame, text=dictionary_of_association_from_database[dt]["resistance"],
                      width=5).pack(
                side="left",
                padx=3,
                anchor="w")
            cal.Label(resultFrame, text=str(dictionary_of_association_from_database[dt]["susceptible"]),
                      width=5).pack(
                side="left",
                padx=3,
                anchor="w")

            if int(dictionary_of_association_from_database[dt]["resistance"]) == 0 or int(
                    dictionary_of_association_from_database[dt]["resistance"] == 0):
                generalOpt[i + 10] = cal.Label(resultFrame, text="No Breakpoints", width=15)
            elif int(dictionary_of_association_from_database[dt]["resistance"]) != 0 or int(
                    dictionary_of_association_from_database[dt]["resistance"] != 0):
                if float(dictionary_of_discs_from_database[dt][3]) >= float(
                        dictionary_of_association_from_database[dt]["resistance"]):
                    generalOpt[i + 10] = cal.Label(resultFrame, text="Susceptible", width=15)
                elif float(dictionary_of_discs_from_database[dt][3]) < float(
                        dictionary_of_association_from_database[dt]["resistance"]):
                    generalOpt[i + 10] = cal.Label(resultFrame, text="Resistant", width=15)
                else:
                    generalOpt[i + 10] = cal.Label(resultFrame, text="Intermediate", width=15)
            generalOpt[i + 10].pack(side="left", padx=3, anchor="w")
            resultFrame.pack()
            i += 1

        global global_image, global_scale_image
        generals = {}

        def savedata():
            global global_top_window_tkinter
            global_top_window_tkinter.destroy()

        cal.Button(cFrame, image=okImg, padding=10, command=savedata).pack(side=RIGHT, pady=10)
        newzonead = str(global_sample_id_from_database) + "/zone_adj/" + str(global_sample_id_from_database) + ".png"
        newfoundad = imglocationhome + "zonesfoundIm" + str(global_sample_id_from_database) + ".png"
        global_image = Image.open(newzonead) if os.path.exists(newzonead) else Image.open(newfoundad)
        global_image = global_image.resize((300, 300), Image.ANTIALIAS)
        global_scale_image = ImageTk.PhotoImage(global_image)
        cal.Label(cFrame, image=global_scale_image).pack(pady=10)
        cFrame.pack()

    global global_top_window_tkinter, global_sample_code, r_widget, generals
    try:
        r_widget["text"] = "Please wait ..."
        r_widget["state"] = "disabled"
    except Exception as _wd:
        exceptionprint("widgets", _wd)

    d_tem, s_list = {}, []
    global_sample_code = None

    def get_info():
        global global_dictionary_of_completed_info, global_sample_code, global_unique_code, global_isolate_name
        m_code = 0

        if global_sample_code is None:
            return

        try:
            btns[0]["state"] = "disabled"
            btns[1]["state"] = "disabled"
        except Exception as _wd:
            exceptionprint("widgets", _wd)

        for _k, _id in d_tem.items():
            if int(global_sample_code.split("|")[0][:]) == _k:
                m_code = _id

        dictionary_of_discs_from_database.clear()
        dictionary_of_association_from_database.clear()

        a = 0
        global_unique_code = m_code[2]
        global_isolate_name = m_code[3]
        _test = {}
        _data = {"sample_id": m_code[0],
                 "bacteria_id": m_code[1]}

        getDisc = http_get_request("getCDiscs",
                                   {"sample_id": m_code[0]})
        if getDisc.status_code == 200:
            for dis in getDisc.json()["discId_num"]:

                # 0: (Chloramphenicol', 'C30', '30ug', 6, bacteria-12, abx-3')
                # noinspection PyTypeChecker
                dictionary_of_discs_from_database[a] = (
                    dis["abx_name"], dis["abx_code"],
                    dis["abx_content"],
                    round(float(dis["diameter"])), dis["bacteria_id"], dis["abx_id"])

                getAssoc = http_get_request("getAssociation", {
                    "abx_id": dictionary_of_discs_from_database[a][5],
                    "bacteria_id": dictionary_of_discs_from_database[a][4]})
                if getAssoc.status_code == 200:
                    double = 0
                    for assoc in getAssoc.json()["association"]:
                        if double == 0:
                            dictionary_of_association_from_database[a] = assoc
                            double = 1
                        else:
                            double = 1
                a += 1

        if not os.path.exists(str(m_code[0]) + "/zone_adj/" + str(m_code[0]) + ".png"):
            if not os.path.exists(imglocationhome + "zonesfoundIm" + str(m_code[0]) + ".png"):
                downloadImg(m_code[0], "_zonesfoundIm", "zonesfoundIm",
                            False)
        threading.Thread(target=singleTestProgressing, args=[m_code[0]]).start()
        return

    _c = 1
    _n = None
    generals = {}
    while True:
        try:
            for dtest in http_request_return_json_or_boolean(file="getSamples", param={}, return_data=True).json()[
                "_List"]:
                d_tem[_c] = (int(dtest["sample_id"]), int(dtest["bacteria_id"]), str(dtest["uniquecode"]),
                             str(dtest["bacteria_name"]))
                dateformat = datetime.datetime.strptime(str(dtest["test_on"]), '%Y-%m-%d').strftime('%d-%m-%Y')
                if _c < 10:
                    _n = "0" + str(_c)
                    s_list.append(str(_n) + " | " + str(dateformat) + " | " + str(dtest["uniquecode"]) + " | " + str(
                        dtest["bacteria_name"]))
                else:
                    s_list.append(str(_c) + " | " + str(dateformat) + " | " + str(dtest["uniquecode"]) + " | " + str(
                        dtest["bacteria_name"]))
                _c += 1
            break
        except Exception as _ehttp:
            if _ehttp.__doc__.__eq__("Inappropriate argument type."):
                r_widget["text"] = "No result at the moment"
                time.sleep(3)
                try:
                    r_widget["state"] = "enabled"
                    r_widget["text"] = "Result Report"
                except Exception as _wd:
                    exceptionprint("widgets", _wd)
                return
            exceptionprint("result", _ehttp)

    try:
        r_widget["state"] = "enabled"
        r_widget["text"] = "Result Report"
    except Exception as _wd:
        exceptionprint("widgets", _wd)
    global_top_window_tkinter = Toplevel(base)
    set_window_icon_and_make_fullscreen(global_top_window_tkinter)
    abxFrame = cal.Frame(global_top_window_tkinter, relief=SOLID, padding=20)
    cal.Label(global_top_window_tkinter, text="Result Report").pack(pady=10)
    anEntry = cal.Entry(abxFrame, width=dimensionPadding+3)
    anEntry.pack(ipady=10, pady=10)

    listViewFrame = cal.Frame(abxFrame)
    scrollbar = Scrollbar(listViewFrame)
    scrollbar.pack(side=RIGHT, fill=Y, ipadx=20)
    anListbox = Listbox(listViewFrame, width=dimensionPadding, height=10,
                        yscrollcommand=scrollbar.set)
    listboxupdate(s_list, anListbox, False)
    scrollbar.config(command=anListbox.yview)
    listViewFrame.pack()

    anEntry.bind("<KeyRelease>", lambda e, box=anListbox: toListbox(e, box, s_list, False))
    anListbox.bind("<<ListboxSelect>>", lambda event, efield=anEntry: itemselected(event, efield, 2))
    anListbox.bind("<Double-Button-1>", lambda e: threading.Thread(target=get_info).start())
    anListbox.bind("<Return>", lambda e: threading.Thread(target=get_info).start())
    anListbox.pack()
    btns[0] = cal.Button(abxFrame, image=backImg, padding=20, command=global_top_window_tkinter.destroy)
    btns[1] = cal.Button(abxFrame, image=proceedImg, padding=20,
                         command=lambda: threading.Thread(target=get_info).start())
    btns[0].pack(side=LEFT, pady=10)
    btns[1].pack(side=RIGHT, pady=10)
    abxFrame.pack()


# noinspection PyGlobalUndefined
def start_test():
    global threadInstance, isolate_list_from_database

    error = None
    global_sample_id_from_database = None

    # noinspection PyShadowingNames
    def proceedtophoto():
        try:

            global global_unique_code, error
            global_unique_code = entryField.get().upper().replace("$", "")
            # threading.Thread(target=setprogress, args=[1]).start()
            setprogress(1)
        except Exception as e_pro:
            exceptionprint("proceedtophoto", e_pro)

        def discabxConfirm():
            global list_of_antibiotic_match_with_isolate, dictionary_of_antibiotic_discs_from_database
            global global_image, global_scale_image, global_top_window_tkinter, global_isolate_name, valHolder, generals
            global_top_window_tkinter.destroy()
            valHolder = Toplevel(base)
            set_window_icon_and_make_fullscreen(valHolder)
            cal.Label(valHolder, text="Confirm discs  - Antibiotics for " + global_isolate_name).pack(pady=20)
            discabxFrame = cal.Frame(valHolder, relief=SOLID, padding=30)
            global_image = Image.open(imglocationhome + tmpdiscfoundimg + "discsfound.png")
            global_image = global_image.resize((600, 600), Image.ANTIALIAS)
            global_scale_image = ImageTk.PhotoImage(global_image)

            def anproceed():
                global dictionary_of_antibiotic_discs_from_database
                mycondition = False
                for b in dictionary_of_antibiotic_discs_from_database:
                    if dictionary_of_antibiotic_discs_from_database[b] == "No match found":
                        mycondition = True

                if not mycondition:
                    threading.Thread(target=testData).start()

            # noinspection PyShadowingNames
            def nomatchfound(data):
                for i in data:
                    if data[i] == "No match found":
                        generals[12]["state"] = "disabled"
                        break
                    else:
                        generals[12]["state"] = "enabled"
                        generals[12].bind("<Button-1>", lambda e: anproceed())

            # noinspection PyShadowingNames
            def change_antibiotic_name(antibiotic_name, dictionary_of_antibiotics):
                def bacteria_change():
                    global abxname, dictionary_of_antibiotic_discs_from_database
                    global_top_window_tkinter.destroy()
                    antibiotic_name["text"] = "Disc " + str(dictionary_of_antibiotics) + "." + abxname
                    if dictionary_of_antibiotics:
                        dictionary_of_antibiotic_discs_from_database[dictionary_of_antibiotics] = abxname
                        nomatchfound(dictionary_of_antibiotic_discs_from_database)
                    if not dictionary_of_antibiotics:
                        dictionary_of_antibiotic_discs_from_database[dictionary_of_antibiotics] = "No match found"

                matched = list()
                notmatched = list()
                for _, a in enumerate(list_of_antibiotic_match_with_isolate):
                    for _, _name in dictionary_of_antibiotic_discs_from_database.items():
                        if a == _name:
                            matched.append(a)
                        else:
                            notmatched.append(a)

                # noinspection PyShadowingNames
                global_top_window_tkinter = Toplevel(base)
                set_window_icon_and_make_fullscreen(global_top_window_tkinter)
                abxFrame = cal.Frame(global_top_window_tkinter, relief=SOLID, padding=20)
                cal.Label(global_top_window_tkinter,
                          text="Change antibiotic for  disk." + str(dictionary_of_antibiotics) + "").pack(pady=10)
                anEntry = cal.Entry(abxFrame, width=dimensionPadding+3)
                anEntry.pack(ipady=10, pady=10)
                listViewFrame = cal.Frame(abxFrame)
                scrollbar = Scrollbar(listViewFrame)
                anListbox = Listbox(listViewFrame, width=dimensionPadding, height=10,
                                    yscrollcommand=scrollbar.set)
                scrollbar.pack(side=RIGHT, fill=Y, ipadx=20)
                scrollbar.config(command=anListbox.yview)
                listboxupdate(list_of_antibiotic_match_with_isolate, anListbox)
                listViewFrame.pack()
                anEntry.bind("<KeyRelease>",
                             lambda e, box=anListbox: toListbox(e, box, list_of_antibiotic_match_with_isolate))
                anListbox.bind("<<ListboxSelect>>", lambda event, efield=anEntry: itemselected(event, efield, False))
                anListbox.bind("<Double-Button-1>", lambda e: bacteria_change())
                anListbox.bind("<Return>", lambda e: bacteria_change())
                anListbox.pack()
                cal.Button(abxFrame, image=backImg, padding=20, command=global_top_window_tkinter.destroy).pack(
                    side=LEFT, pady=10)
                cal.Button(abxFrame, image=okImg, padding=20, command=bacteria_change).pack(side=RIGHT,
                                                                                            pady=10)
                anEntry.pack()
                abxFrame.pack()

            discabxBox = cal.Frame(discabxFrame, relief=SOLID, padding=10)
            discabxL = cal.Frame(discabxBox)
            discabxR = cal.Frame(discabxBox)

            # Dictionary Label
            disclabeldict = generals = {}
            generals[10] = cal.Label(discabxFrame, image=global_scale_image)
            generals[10].pack(side=LEFT)
            # noinspection PyShadowingNames
            for i in dictionary_of_antibiotic_discs_from_database:
                disclabeldict[i] = cal.Label(discabxL, width=35,
                                             text="Disc " + str(i) + "." + dictionary_of_antibiotic_discs_from_database[
                                                 i])
                disclabeldict[i].pack(anchor='w', pady=0)
                disclabeldict[i].bind("<Double-Button-1>",
                                      lambda eventhandle, akey=i, aname=disclabeldict[i]: change_antibiotic_name(aname,

                                                                                                                 akey))
            discabxL.pack(side=LEFT, ipadx=5)
            discabxR.pack(side=RIGHT, ipadx=5)
            discabxBox.pack(pady=5)

            # noinspection PyShadowingNames,PyAssignmentToLoopOrWithParameter
            def testData():
                global generals, global_isolate_name, global_unique_code, global_top_window_tkinter, error, global_sample_id_from_database
                global_top_window_tkinter = Toplevel(base)
                set_window_icon_and_make_fullscreen(global_top_window_tkinter)
                generals = dict()
                generals[5] = cal.Frame(global_top_window_tkinter, padding=50)
                generals[6] = cal.Label(generals[5], width=50)
                generals[6].pack(pady=100)
                generals[5].pack(pady=100)
                generals[6]["text"] = "Preparing for zone detection please wait"

                global insertlist
                insertlist[:] = []

                for _, _a in dictionary_of_antibiotic_discs_from_database.items():
                    insertlist.append(_a.split(" -")[0])

                try:
                    if not http_request_return_json_or_boolean(file="insertTestData0",
                                                               param={"uniquecode": global_unique_code,
                                                                      "isolatename": global_isolate_name,
                                                                      "abx_discs": json.dumps(insertlist)},
                                                               return_data=False):
                        generals[6]["text"] = "Oops! Something went wrong please check isolate matches"
                        time.sleep(3)
                        global_top_window_tkinter.destroy()
                        return
                except Exception as _ehttp:
                    exceptionprint("insertTestData0", _ehttp)

                closewindows()
                threading.Thread(target=setprogress, args=[4]).start()

                # noinspection PyShadowingNames
                def singleTestProgressing(global_sample_id_from_database):
                    global global_top_window_tkinter, generalOpt, global_bacteria_id_from_database, global_unique_code, global_isolate_name
                    global_top_window_tkinter.destroy()
                    global_top_window_tkinter = Toplevel(base)
                    set_window_icon_and_make_fullscreen(global_top_window_tkinter)
                    cFrame = cal.Frame(global_top_window_tkinter, padding=5, relief=SOLID)

                    cal.Label(global_top_window_tkinter,
                              text="ACCESSION # - " + str(global_unique_code) + "  |  BACTERIA -  " + str(
                                  global_isolate_name)).pack(pady=10)
                    generalOpt = cal.Frame(cFrame, padding=5, relief=SOLID)
                    cal.Label(generalOpt, text="Antibiotics", width=20).pack(side="left", padx=3,
                                                                             anchor="w")
                    cal.Label(generalOpt, text="Code", width=7).pack(side="left", padx=3, anchor="w")
                    cal.Label(generalOpt, text="Dose", width=10).pack(side="left", padx=3, anchor="w")
                    cal.Label(generalOpt, text="Zones (mm)", width=10).pack(side="left", padx=3, anchor="w")
                    cal.Label(generalOpt, text="R<", width=5).pack(side="left", padx=3, anchor="w")
                    cal.Label(generalOpt, text="S≥", width=5).pack(side="left", padx=3, anchor="w")
                    cal.Label(generalOpt, text="Interpretation", width=15).pack(side="left", padx=3,
                                                                                anchor="w")
                    generalOpt.pack()

                    i = 0
                    generalOpt = {}

                    global dictionary_of_discs_from_database, dictionary_of_association_from_database

                    for dt in dictionary_of_discs_from_database:
                        resultFrame = cal.Frame(cFrame, padding=5, relief=SOLID)
                        cal.Label(resultFrame, width=20, text=str(i + 1) + ". " + str(
                            dictionary_of_discs_from_database[dt][0][:18] + "... "
                            if len(dictionary_of_discs_from_database[dt][0]) > 18 else
                            dictionary_of_discs_from_database[dt][0])).pack(side="left",
                                                                            padx=3,
                                                                            anchor="w")

                        cal.Label(resultFrame, text=str(dictionary_of_discs_from_database[dt][1]),
                                  width=7).pack(
                            side="left",
                            padx=3,
                            anchor="w")

                        cal.Label(resultFrame, text=str(dictionary_of_discs_from_database[dt][2]),
                                  width=10).pack(
                            side="left",
                            padx=3,
                            anchor="w")
                        generalOpt[i + 20] = cal.Label(resultFrame,
                                                       text=str(dictionary_of_discs_from_database[dt][3]),
                                                       width=10)
                        generalOpt[i + 20].pack(side="left", padx=3, anchor="w")
                        cal.Label(resultFrame, text=dictionary_of_association_from_database[dt]["resistance"],
                                  width=5).pack(
                            side="left",
                            padx=3,
                            anchor="w")
                        cal.Label(resultFrame, text=str(dictionary_of_association_from_database[dt]["susceptible"]),
                                  width=5).pack(
                            side="left",
                            padx=3,
                            anchor="w")

                        if int(dictionary_of_association_from_database[dt]["resistance"]) == 0 or int(
                                dictionary_of_association_from_database[dt]["resistance"] == 0):
                            generalOpt[i + 10] = cal.Label(resultFrame, text="No Breakpoints", width=15)
                        elif int(dictionary_of_association_from_database[dt]["resistance"]) != 0 or int(
                                dictionary_of_association_from_database[dt]["resistance"] != 0):
                            if float(dictionary_of_discs_from_database[dt][3]) >= float(
                                    dictionary_of_association_from_database[dt]["resistance"]):
                                generalOpt[i + 10] = cal.Label(resultFrame, text="Susceptible", width=15)
                            elif float(dictionary_of_discs_from_database[dt][3]) < float(
                                    dictionary_of_association_from_database[dt]["resistance"]):
                                generalOpt[i + 10] = cal.Label(resultFrame, text="Resistant", width=15)
                            else:
                                generalOpt[i + 10] = cal.Label(resultFrame, text="Intermediate", width=15)
                        generalOpt[i + 10].pack(side="left", padx=3, anchor="w")
                        resultFrame.pack()
                        i += 1

                    global global_image, global_scale_image, generals
                    generals = {}

                    # noinspection PyShadowingNames
                    def adjustTest():
                        global global_top_window_tkinter, imagefx, imagefxs, generals, global_sample_id_from_database
                        generals = {}
                        global_top_window_tkinter.destroy()
                        global_top_window_tkinter = Toplevel(base)
                        set_window_icon_and_make_fullscreen(global_top_window_tkinter)
                        baseFrame = cal.Frame(global_top_window_tkinter)
                        eFrame = cal.Frame(baseFrame, relief=SOLID, padding=20)

                        list_distances = []

                        # noinspection PyShadowingNames
                        def cAdjust(amount, dics_number, condition):
                            # noinspection PyShadowingNames,PyBroadException
                            def background_adjust_thread(dsc, amount, cond):
                                global imagefx, imagefxs, generals, global_scale_image, global_image
                                global incount, global_sample_id_from_database, zones_adj, zones

                                if str(dsc).__eq__("Disc to edit") or str(amount).__eq__("Amount"):
                                    return

                                mm = 1 if cond else -1
                                try:
                                    generals[3]["state"] = "disabled"
                                    generals[4]["state"] = "disabled"
                                except Exception as _:
                                    pass

                                # noinspection PyShadowingNames
                                discsTest = {}

                                zone_distances, dist = [], {}

                                j = 1
                                getdiscs = sQLiteconnection().execute("SELECT disc FROM zones WHERE sample_id = ?  ",
                                                                      (str(global_sample_id_from_database),))
                                for disc in getdiscs.fetchall():
                                    discsTest[j] = (
                                        (int(disc[0].split(",")[0][1:])), (int(disc[0].rsplit(",")[-1][:-1])))
                                    j += 1
                                incount = True

                                getzone = sQLiteconnection().execute("SELECT diameter FROM discs WHERE sample_id = ?  ",
                                                                     (str(global_sample_id_from_database),))
                                for diam in getzone.fetchall():
                                    zone_distances.append(float(diam[0]))

                                rgb_dir = Path(r'' + imgbase + str(global_sample_id_from_database) + '/rgb')
                                zones_dir = Path(r'' + imgbase + str(global_sample_id_from_database) + '/zones')
                                zadjs_dir = Path(r'' + imgbase + str(global_sample_id_from_database) + '/zones_adj')
                                zadj_dir = Path(r'' + imgbase + str(global_sample_id_from_database) + '/zone_adj')

                                rgb_path = rgb_dir / (str(global_sample_id_from_database) + '.png')
                                zones_path = zones_dir / (str(global_sample_id_from_database) + '.txt')
                                zadjs_path = zadjs_dir / (str(global_sample_id_from_database) + '.txt')
                                zadj_path = zadj_dir / (str(global_sample_id_from_database) + '.png')

                                if os.path.exists(imgbase + str(global_sample_id_from_database) + "/zones_adj/" + str(
                                        global_sample_id_from_database) + ".txt"):
                                    zones = load_zones(zadjs_path)
                                    zones_adj = adjust_zones(zones, int(dsc) - 1, mm * int(amount))
                                    save_zones(zones_adj, zadjs_path)

                                elif not os.path.exists(imgbase + str(global_sample_id_from_database) + "/zones_adj/" + str(
                                        global_sample_id_from_database) + ".txt"):
                                    zones = load_zones(zones_path)
                                    zones_adj = adjust_zones(zones, int(dsc) - 1, mm * int(amount))
                                    save_zones(zones_adj, zadjs_path)

                                # draw new adjusted zones
                                rgb_zones = load_image(rgb_path)
                                draw_zones(rgb_zones, zones_adj)
                                save_image(rgb_zones, zadj_path)

                                for z in zones:
                                    for k, i in enumerate(zones[z]):
                                        if k == 3:
                                            list_distances.append(float("{0: .2f}".format(i)))

                                def sQLitComit(sql, args=None):
                                    sQLit = sQLitInsert()
                                    if args is None:
                                        with sQLit:
                                            sQLit.execute(sql)
                                    elif args is not None:
                                        with sQLit:
                                            sQLit.execute(sql, args)

                                # noinspection PyShadowingNames
                                for g, l in enumerate(list_distances):
                                    dist[g] = l
                                getdiscs0 = sQLiteconnection().execute(
                                    "SELECT * FROM discs WHERE sample_id =  " + str(global_sample_id_from_database))
                                for (_, di), disc_id in zip(dist.items(), getdiscs0.fetchall()):
                                    try:
                                        param = (str(round(float(di))), str(disc_id[0]))
                                        sQLitComit(
                                            ''' UPDATE discs set diameter= ?  WHERE disc_id = ? ''',
                                            param)
                                    except Exception as e_updsc:
                                        exceptionprint("update discs", e_updsc)

                                list_distances[:] = []

                                newzonead = imgbase + str(global_sample_id_from_database) + "/zone_adj/" + str(
                                    global_sample_id_from_database) + ".png"
                                newfoundad = imglocationhome + "zonesfoundIm" + str(
                                    global_sample_id_from_database) + ".png"
                                imagefx = Image.open(newzonead) if os.path.exists(newzonead) else Image.open(newfoundad)

                                imagefx = imagefx.resize((500, 500), Image.ANTIALIAS)
                                imagefxs = ImageTk.PhotoImage(imagefx)
                                try:
                                    generals[1]["image"] = imagefxs
                                    generals[3]["state"] = "enabled"
                                    generals[4]["state"] = "enabled"
                                except Exception as _:
                                    pass

                            threading.Thread(target=background_adjust_thread,
                                             args=[dics_number, amount, condition]).start()

                        newzonead = imgbase + str(global_sample_id_from_database) + "/zone_adj/" + str(
                            global_sample_id_from_database) + ".png"
                        newfoundad = imglocationhome + "zonesfoundIm" + str(global_sample_id_from_database) + ".png"
                        imagefx = Image.open(newzonead) if os.path.exists(newzonead) else Image.open(newfoundad)

                        g = 0
                        imagefx = imagefx.resize((500, 500), Image.ANTIALIAS)
                        imagefxs = ImageTk.PhotoImage(imagefx)
                        imframe = cal.Frame(eFrame)
                        generals[g + 1] = cal.Label(imframe, image=imagefxs)
                        generals[g + 1].pack()
                        combodropList = []
                        combodropList[:] = range(1, len(dictionary_of_antibiotic_discs_from_database) + 1)
                        combodropAmount = [x for x in range(1, 9)]
                        bFrame = cal.Frame(baseFrame)
                        generals[g + 5] = cal.Combobox(bFrame, width=20, values=combodropList, state="readonly")
                        generals[g + 5].set("Disc to edit")
                        generals[g + 5].pack(padx=2)
                        generals[g + 2] = cal.Combobox(bFrame, width=20, values=combodropAmount, state="readonly")
                        generals[g + 2].set("Amount")
                        generals[g + 3] = cal.Button(bFrame, image=plusImg, width=20, padding=20)
                        generals[g + 3].bind("<Button-1>",
                                             lambda event: cAdjust(generals[g + 2].get(), generals[g + 5].get(), True))
                        generals[g + 4] = cal.Button(bFrame, image=minusImg, width=20, padding=20)
                        generals[g + 4].bind("<Button-1>",
                                             lambda event: cAdjust(generals[g + 2].get(), generals[g + 5].get(), False))
                        generals[g + 4].pack(side=LEFT, padx=2)
                        generals[g + 2].pack(pady=10, ipady=3, padx=20, side=LEFT)
                        generals[g + 3].pack(side=LEFT, padx=2)
                        imframe.pack(side=LEFT)
                        bFrame.pack(side=RIGHT)

                        # noinspection PyShadowingNames
                        def callback():
                            global dictionary_of_discs_from_database, global_sample_id_from_database
                            getzone = sQLiteconnection().execute("SELECT diameter FROM discs WHERE sample_id = ?  ",
                                                                 (str(global_sample_id_from_database),))
                            for _d, di in zip(dictionary_of_discs_from_database, getzone.fetchall()):
                                l = list(dictionary_of_discs_from_database[_d])
                                l[3] = di[0]
                                dictionary_of_discs_from_database[_d] = tuple(l)

                            global_top_window_tkinter.destroy()
                            threading.Thread(target=singleTestProgressing,
                                             args=[global_sample_id_from_database]).start()

                        eFrame.pack()
                        cal.Button(baseFrame, image=okImg, width=20, padding=20, command=callback).pack(
                            pady=3)
                        baseFrame.pack()

                    def savedata():
                        global global_top_window_tkinter, incount
                        global_top_window_tkinter.destroy()

                        # noinspection PyShadowingNames
                        def finish():
                            global global_sample_id_from_database
                            shutil.copy(imgbase + str(global_sample_id_from_database) + "/zone_adj/" + str(
                                global_sample_id_from_database) + ".png",
                                        imglocationhome + "zonesfoundIm" + str(global_sample_id_from_database) + ".png")
                            getdiscs0 = sQLiteconnection().execute(
                                "SELECT disc_id FROM discs WHERE sample_id =  " + global_sample_id_from_database)
                            getzone = sQLiteconnection().execute(
                                "SELECT diameter FROM discs WHERE sample_id = ?  ",
                                (str(global_sample_id_from_database),))
                            for dis, dia in zip(getdiscs0.fetchall(), getzone.fetchall()):

                                disc_update_info = {"disc_num": dis[0], "sample_id": global_sample_id_from_database,
                                                    "distances": round(float(dia[0]))}
                                while True:
                                    try:
                                        if http_request_return_json_or_boolean(file="updateDisc",
                                                                               param=disc_update_info,
                                                                               return_data=False):
                                            break
                                    except Exception as _ehttp:
                                        exceptionprint("finish", _ehttp)
                            print("Update complete")

                        if incount:
                            threading.Thread(target=finish).start()

                    cal.Button(cFrame, image=okImg, padding=10, command=savedata).pack(side=RIGHT, pady=10)

                    modify = cal.Button(cFrame, image=editImg, padding=10, state="disabled", command=adjustTest)
                    modify.pack(side=LEFT, pady=10)

                    newzonead = imgbase + str(global_sample_id_from_database) + "/zone_adj/" + str(
                        global_sample_id_from_database) + ".png"
                    newfoundad = imglocationhome + "zonesfoundIm" + str(global_sample_id_from_database) + ".png"

                    def imgdown():
                        while True:
                            try:
                                if os.path.exists(imgbase + str(global_sample_id_from_database) + "/rgb/" + str(
                                        global_sample_id_from_database) + ".png"):
                                    modify["state"] = "enabled"
                                    break
                            except Exception as _:
                                break

                    threading.Thread(target=imgdown).start()

                    global_image = Image.open(newzonead) if os.path.exists(newzonead) else Image.open(newfoundad)
                    global_image = global_image.resize((300, 300), Image.ANTIALIAS)
                    global_scale_image = ImageTk.PhotoImage(global_image)

                    cal.Label(cFrame, image=global_scale_image).pack(pady=10)
                    cFrame.pack()

                # noinspection PyShadowingNames,PyBroadException
                def progressposition():
                    global global_sample_id_from_database, global_bacteria_id_from_database

                    while True:
                        try:
                            getsampleId = http_get_request("getdiscsId", {"uniquecode": global_unique_code})
                            if getsampleId.status_code == 200:
                                for Ld in getsampleId.json()["idcalled"]:
                                    global_sample_id_from_database = Ld["sample_id"]
                                break
                        except Exception as e_ge:
                            exceptionprint("getsampleId", e_ge)

                    try:
                        while True:
                            c_data = http_get_request("getCompletedTestData",
                                                      {"sample_id": global_sample_id_from_database})
                            if c_data.status_code == 200:
                                for Id in c_data.json()["samples"]:
                                    global_bacteria_id_from_database = Id["bacteria_id"]
                                break
                    except Exception as e_b:
                        exceptionprint("getbacteria_id", e_b)
                    while True:
                        try:
                            getTestStarted = http_get_request("getTestStatus", {})
                            if getTestStarted.status_code == 200:
                                for started in getTestStarted.json()["teststatus"]:
                                    if started["prog"] == "1":
                                        generals[6]["text"] = "Working on zone detection, this takes a moment."
                                    elif started["prog"] == "2":
                                        generals[6]["text"] = "We are almost done please hold on a moment"
                                    elif started["prog"] == "3":
                                        generals[6]["text"] = "Taking care of a few things before we are done"
                                    elif started["prog"] == "4":
                                        generals[6]["text"] = "Zone detection is now complete, wait a moment "
                                        break
                        except Exception as _:
                            break

                threadInstance = threading.Thread(target=progressposition)
                threadInstance.setName("threadInstance")
                threadInstance.start()

                # noinspection PyShadowingNames
                def preparing_to_display_completed_test():
                    global global_sample_id_from_database, global_bacteria_id_from_database, incount
                    global dictionary_of_discs_from_database, dictionary_of_association_from_database
                    global_dictionary_of_completed_info.clear()
                    dictionary_of_discs_from_database.clear()
                    dictionary_of_association_from_database.clear()
                    cond = True
                    while cond:
                        try:
                            for j in http_request_return_json_or_boolean(file="getTestStatus", param={},
                                                                         return_data=True).json()["teststatus"]:
                                if j["status"] == "6":
                                    threading.Thread(target=setprogress, args=[7]).start()

                                    # downloadImg(global_sample_id_from_database, "_zonesfoundIm", "zonesfoundIm",
                                    #             False)

                                    rgb_dir = Path(r'' + imgbase + str(global_sample_id_from_database) + '/rgb')
                                    zone_dir = Path(r'' + imgbase + str(global_sample_id_from_database) + '/zone')
                                    zones_dir = Path(r'' + imgbase + str(global_sample_id_from_database) + '/zones')
                                    zadjs_dir = Path(r'' + imgbase + str(global_sample_id_from_database) + '/zones_adj')
                                    zadj_dir = Path(r'' + imgbase + str(global_sample_id_from_database) + '/zone_adj')

                                    for d in [rgb_dir,
                                              zone_dir,
                                              zones_dir,
                                              zadjs_dir,
                                              zadj_dir]:
                                        d.mkdir(parents=True, exist_ok=True)

                                    # wget.download(
                                    #     domain + "img/_zonesfor" + str(global_sample_id_from_database) + ".txt",
                                    #     str(global_sample_id_from_database) + "/zones/" + str(
                                    #         global_sample_id_from_database) + ".txt")

                                    d_tem = {}
                                    c = 0
                                    a = 0
                                    getDisc = http_get_request("getCDiscs",
                                                               {"sample_id": global_sample_id_from_database})
                                    if getDisc.status_code == 200:
                                        for dis in getDisc.json()["discId_num"]:

                                            # 0: (Chloramphenicol', 'C30', '30ug', 6, bacteria-12, abx-3')

                                            # noinspection PyTypeChecker
                                            dictionary_of_discs_from_database[a] = (
                                                dis["abx_name"], dis["abx_code"],
                                                dis["abx_content"],
                                                round(float(dis["diameter"])), dis["bacteria_id"], dis["abx_id"])

                                            getAssoc = http_get_request("getAssociation", {
                                                "abx_id": dictionary_of_discs_from_database[a][5],
                                                "bacteria_id": dictionary_of_discs_from_database[a][4]})
                                            if getAssoc.status_code == 200:
                                                double = 0
                                                for assoc in getAssoc.json()["association"]:
                                                    if double == 0:
                                                        dictionary_of_association_from_database[a] = assoc
                                                        double = 1
                                                    else:
                                                        double = 1
                                            a += 1

                                    while True:
                                        try:
                                            for dtest in \
                                                    http_request_return_json_or_boolean(file="getCompletedTestResults",
                                                                                        param={
                                                                                            "sample_id": global_sample_id_from_database,
                                                                                            "bacteria_id": global_bacteria_id_from_database},
                                                                                        return_data=True).json()[
                                                        "samples"]:
                                                d_tem[c] = (dtest["abx_name"], dtest["abx_code"],
                                                            dtest["abx_content"], round(float(dtest["diameter"])),
                                                            dtest["susceptible"], dtest[
                                                                "resistance"])
                                                c += 1
                                            break
                                        except Exception as _:
                                            print()

                                    for _k, _v in d_tem.items():

                                        if _v not in global_dictionary_of_completed_info.values():
                                            global_dictionary_of_completed_info[_k] = _v

                                    def imdown():
                                        global global_sample_id_from_database

                                        def sQLitComit(sql, args=None):
                                            sQLit = sQLitInsert()
                                            if args is None:
                                                with sQLit:
                                                    sQLit.execute(sql)
                                            elif args is not None:
                                                with sQLit:
                                                    sQLit.execute(sql, args)

                                        sQLitComit('''DELETE FROM zones''')
                                        sQLitComit('''DELETE FROM discs''')

                                        while True:
                                            try:
                                                for discl in http_request_return_json_or_boolean(file="getCZone",
                                                                                                 param={
                                                                                                     "sample_id": str(
                                                                                                         global_sample_id_from_database)},
                                                                                                 return_data=True).json()[
                                                    "zone_num"]:
                                                    param = (str(discl["disc"]), global_sample_id_from_database)
                                                    sQLitComit(
                                                        '''INSERT INTO zones (disc,sample_id) VALUES (?,?)''',
                                                        param)

                                                for l in http_request_return_json_or_boolean(file="getCDiscs",
                                                                                             param={"sample_id": str(
                                                                                                 global_sample_id_from_database)},
                                                                                             return_data=True).json()[
                                                    "discId_num"]:
                                                    param = (str(l["disc_id"]), str(round(float(l["diameter"]))),
                                                             str(l["sample_id"]))
                                                    sQLitComit(
                                                        ''' INSERT INTO discs (disc_id,diameter,sample_id) VALUES  (?,?,?) ''',
                                                        param)
                                                break
                                            except Exception as _ee:
                                                exceptionprint("discl", _ee)

                                        # downloadImg(global_sample_id_from_database, "_", "Im", False)
                                        #
                                        # shutil.move(
                                        #     imglocationhome + "Im" + str(global_sample_id_from_database) + ".png",
                                        #     str(global_sample_id_from_database) + "/rgb/" + str(
                                        #         global_sample_id_from_database) + ".png")

                                    incount = False
                                    threading.Thread(target=imdown).start()
                                    threading.Thread(target=singleTestProgressing,
                                                     args=[global_sample_id_from_database]).start()
                                    cond = False
                        except Exception as e_wait:
                            exceptionprint("preparing_to_display_completed_test", e_wait)

                preparing_to_display_completed_test()

            def brightImg():
                global global_image, global_scale_image
                # Code Below is roughly optimized for brightness and contrast
                brightness = 94
                contrast = 56
                img = np.int16(cv2.imread(imglocationhome + "/discsfound/discsfound.png"))
                img = img * (contrast / 127 + 1) - contrast + brightness
                img = np.clip(img, 0, 255)
                cv2.imwrite(imglocationhome + "/discsfound/discsfound_bright.png", np.uint8(img))
                global_image = Image.open(imglocationhome + "/discsfound/discsfound_bright.png")
                global_image = global_image.resize((600, 600), Image.ANTIALIAS)
                global_scale_image = ImageTk.PhotoImage(global_image)
                generals[10]["image"] = global_scale_image

            discOptFrame = cal.Frame(discabxFrame)
            cal.Button(discOptFrame, image=backImg, padding=20, command=valHolder.destroy).pack(pady=10, padx=20,
                                                                                                side=LEFT)
            cal.Button(discOptFrame, text="Brighten Image", padding=20,
                       command=lambda: threading.Thread(target=brightImg).start()).pack(pady=10, side=LEFT)

            # noinspection PyTypeChecker
            generals[12] = cal.Button(discOptFrame, image=proceedImg, padding=20, state="disabled")
            generals[12].pack(pady=10, padx=20, side=LEFT)
            nomatchfound(dictionary_of_antibiotic_discs_from_database)
            discabxFrame.pack()
            discOptFrame.pack()

        def imageprocessdone():
            global threadInstance
            generalOpt[1].pack_forget()
            generalOpt[i].pack_forget()
            generalOpt[2].pack(pady=10)
            isolateListBox.unbind("<Return>")
            isolateListBox.unbind("<Double-Button-1>")
            generalOpt[2]["text"] = "Taking care of a few things, wait a moment..."

            def bgthreadimg():
                # noinspection PyShadowingNames
                listTemp = []
                global list_of_antibiotic_match_with_isolate, dictionary_of_antibiotic_discs_from_database
                list_of_antibiotic_match_with_isolate.clear()
                dictionary_of_antibiotic_discs_from_database.clear()
                while True:
                    try:
                        for _value in http_request_return_json_or_boolean(file="getAntibiotics",
                                                                          param={"isolatename": global_isolate_name},
                                                                          return_data=True).json()["isolatename"]:
                            listTemp.append(_value["abx_code"])
                        list_of_antibiotic_match_with_isolate = list(set(listTemp))

                        i = 1
                        for x in http_request_return_json_or_boolean(file="getTempAntibiotics", return_data=True,
                                                                     param={}).json()[
                            "temp_abx"]:
                            dictionary_of_antibiotic_discs_from_database[i] = x["abx_name"]
                            i += 1
                        break

                    except Exception as _eg:
                        if _eg.__doc__ == "Inappropriate argument type.":
                            generalOpt[2]["text"] = "No data found for " + str(global_isolate_name)
                            time.sleep(3)
                            generalOpt[2].pack_forget()
                            generalOpt[0].pack(pady=10, side=LEFT)
                            generalOpt[1].pack(pady=10, side=RIGHT)
                            generalOpt[1].bind("<Button-1>",
                                               lambda
                                                   e: None if global_isolate_name is None else imageprocessdone())
                            isolateListBox.bind("<Double-Button-1>",
                                                lambda
                                                    e: None if global_isolate_name is None else imageprocessdone())
                            isolateListBox.bind("<Return>",
                                                lambda
                                                    e: None if global_isolate_name is None else imageprocessdone())
                            break
                        exceptionprint("bgthreadimg", _eg)
                if len(listTemp) > 0 and len(dictionary_of_antibiotic_discs_from_database) > 0:
                    matched = dict()
                    for k, _name in dictionary_of_antibiotic_discs_from_database.items():
                        for _, namelist in enumerate(list_of_antibiotic_match_with_isolate):
                            if _name.__eq__(namelist):
                                matched[k] = _name
                                break
                            elif _name == "":
                                matched[k] = "No match found"
                            elif _name != namelist:
                                matched[k] = _name + " - No breakpoints found"

                    dictionary_of_antibiotic_discs_from_database.clear()
                    dictionary_of_antibiotic_discs_from_database = matched.copy()

                    matched.clear()
                    discabxConfirm()

                    generalOpt[2].pack_forget()
                    generalOpt[0].pack(pady=10, side=LEFT)
                    generalOpt[1].pack(pady=10, side=RIGHT)
                    generalOpt[1].bind("<Button-1>",
                                       lambda
                                           e: None if global_isolate_name is None else imageprocessdone())
                    isolateListBox.bind("<Double-Button-1>",
                                        lambda
                                            e: None if global_isolate_name is None else imageprocessdone())
                    isolateListBox.bind("<Return>",
                                        lambda
                                            e: None if global_isolate_name is None else imageprocessdone())

            threadInstance = threading.Thread(target=bgthreadimg)
            threadInstance.setName("threadInstance")
            threadInstance.start()

        # noinspection PyShadowingNames
        def bgProccessThread():

            def imagefound():
                isolateListBox.unbind("<Return>")
                isolateListBox.unbind("<Double-Button-1>")
                generalOpt[i + 2].pack(pady=10)
                generalOpt[i].pack_forget()
                generalOpt[1].pack_forget()
                generalOpt[2]["text"] = "Wait a moment..."
                threading_value = True
                while threading_value:
                    try:
                        for state in http_request_return_json_or_boolean(file="getTestStatus", param={},
                                                                         return_data=True).json()[
                            "teststatus"]:
                            if state["status"] == "2":
                                while True:
                                    if os.path.exists(imglocationhome + tmpdiscfoundimg + "discsfound.png"):
                                        imageprocessdone()
                                        threading_value = False
                                        break
                    except Exception as e_df:
                        exceptionprint("discsfound image", e_df)

            generalOpt[2].pack_forget()
            generalOpt[i].pack(pady=10, side=LEFT)
            generalOpt[1].pack(pady=10, side=RIGHT)
            generalOpt[1].bind("<Button-1>",
                               lambda
                                   e: None if global_isolate_name is None else threading.Thread(
                                   target=imagefound).start())
            isolateListBox.bind("<Double-Button-1>",
                                lambda
                                    e: None if global_isolate_name is None else threading.Thread(
                                    target=imagefound).start())
            isolateListBox.bind("<Return>",
                                lambda
                                    e: None if global_isolate_name is None else threading.Thread(
                                    target=imagefound).start())

        global global_top_window_tkinter, generalOpt, isolatewindow, global_top_window_tkinter_sp
        i = 0
        global_top_window_tkinter_sp.destroy()
        isolatewindow = Toplevel(base)
        set_window_icon_and_make_fullscreen(isolatewindow)
        cal.Label(isolatewindow, text="Choose isolate").pack(pady=20)
        isoSelectFrame = cal.Frame(isolatewindow, relief=SOLID, padding=30)
        isolateEntry = cal.Entry(isoSelectFrame, width=dimensionPadding+3, justify="center")
        isolateEntry.insert(0, "Enter isolate name here")
        isolateEntry.bind("<FocusIn>", lambda event: clear_Input(isolateEntry))
        isolateEntry.pack(ipady=10)
        listViewFrame = cal.Frame(isoSelectFrame)
        scrollbar = Scrollbar(listViewFrame)
        scrollbar.pack(side=RIGHT, fill=Y, ipadx=20)
        isolateListBox = Listbox(listViewFrame, width=dimensionPadding,
                                 yscrollcommand=scrollbar.set)
        listboxupdate(isolate_list_from_database, isolateListBox)
        scrollbar.config(command=isolateListBox.yview)
        listViewFrame.pack(pady=10)
        isolateEntry.bind("<KeyRelease>", lambda e, box=isolateListBox: toListbox(e, box, isolate_list_from_database))
        isolateListBox.bind("<<ListboxSelect>>", lambda event, efield=isolateEntry: itemselected(event, efield, True))
        isolateListBox.pack()
        generalOpt = {i: cal.Button(isoSelectFrame, image=backImg, padding=10, command=isolatewindow.destroy),
                      i + 1: cal.Button(isoSelectFrame, image=proceedImg, padding=10),
                      i + 2: Label(isoSelectFrame, text="Preparing for zone detection"),
                      i + 3: cal.Button(isoSelectFrame, image=okImg, padding=10, command=proceedtophoto),
                      i + 4: cal.Button(isoSelectFrame, image=backImg, padding=10,
                                        command=global_top_window_tkinter.destroy)
                      }
        generalOpt[i + 2].pack(pady=10)
        isoSelectFrame.pack()
        threadInstance = threading.Thread(target=bgProccessThread)
        threadInstance.setName("threadInstance")
        threadInstance.start()

    widgets = {}

    def picamera():
        setlink(3)
        loop_back = 1
        while loop_back:
            try:
                for state in \
                        http_request_return_json_or_boolean(file="getTestStatus", param={}, return_data=True).json()[
                            "teststatus"]:
                    if state["link"] == "2":
                        loop_back = 0
                        setlink(0)
                        proceedtophoto()
            except Exception as _es:
                exceptionprint("picamera", _es)

    def wait_for_image_capture():
        global global_top_window_tkinter
        global_top_window_tkinter.destroy()
        global generalOpt, threadInstance
        widgets[0].pack_forget()
        widgets[1].pack_forget()
        widgets[3].pack(padx=10, pady=10, side=LEFT)
        widgets[3]["text"] = "Hold on a moment..."
        widgets[2].pack_forget()
        entryField["state"] = "disabled"

        def getBacteriaList():
            global isolate_list_from_database
            while True:
                try:
                    for _b in \
                            http_request_return_json_or_boolean(file="getBacteriaList", param={},
                                                                return_data=True).json()[
                                "bacteria"]:
                        listTemp.append(_b["bacteria_name"])
                    isolate_list_from_database = list(set(listTemp))

                    #  Skip Pi camera trigger
                    proceedtophoto()

                    # Pi camera trigger
                    # threading.Thread(target=picamera).start()

                    break
                except Exception as e_:
                    print(e_)

        threading.Thread(target=getBacteriaList).start()

    global global_top_window_tkinter_sp
    global_top_window_tkinter_sp = Toplevel(base)
    global_top_window_tkinter_sp.lift(base)
    set_window_icon_and_make_fullscreen(global_top_window_tkinter_sp)
    cal.Label(global_top_window_tkinter_sp, text="Scan accession number").pack(pady=10)
    startTestFrame = cal.Frame(global_top_window_tkinter_sp, padding=20, relief=SOLID)
    entryField = Entry(startTestFrame, width=dimensionWidth, justify="center")

    entryField.pack(ipady=9)
    entryField.focus()
    optButtons = cal.Frame(startTestFrame)
    widgets[0] = cal.Button(optButtons, image=backImg, padding=20,
                            command=global_top_window_tkinter_sp.destroy)
    widgets[1] = cal.Button(optButtons, text="CLEAR", width=20, padding=20)
    widgets[2] = cal.Button(optButtons, image=proceedImg, padding=20)

    def place_image_remainder():
        global global_top_window_tkinter
        global_top_window_tkinter = Toplevel(base)
        global_top_window_tkinter.lift(base)
        set_window_icon_and_make_fullscreen(global_top_window_tkinter)
        remainder_frame = cal.Frame(global_top_window_tkinter, padding=20)
        cal.Label(remainder_frame, text="Place petri dish in the instrument then proceed").pack(pady=40)
        cal.Button(remainder_frame, padding=20,
                   image=proceedImg, command=wait_for_image_capture).pack()
        remainder_frame.pack()

    def checkFieldInput():
        if entryField.get() != "":
            widgets[2]["state"] = "enabled"
        else:
            widgets[2]["state"] = "disabled"

    entryField.bind("<Key>", lambda e: checkFieldInput())
    widgets[2]["state"] = "disabled"
    widgets[2].bind("<Button-1>",
                    lambda e: place_image_remainder() if entryField.get() != "" else lambda e,
                                                                                            event=entryField: clear_Input(
                        event))
    widgets[1].bind("<Button-1>", lambda e, event=entryField: clear_Input(event))
    widgets[3] = cal.Label(optButtons)
    widgets[0].pack(padx=10, pady=10, side=LEFT)
    widgets[1].pack(padx=10, pady=10, side=LEFT)
    widgets[2].pack(padx=10, pady=10, side=LEFT)
    optButtons.pack()
    startTestFrame.pack()


if __name__ == '__main__':
    isolate_list_from_database = listTemp = b_idTemp = list_of_antibiotic_match_with_isolate = []
    dimensionWidth, dimensionPadding = 30, 40
    global_bacteria_id_from_database = incount = unique_code = None
    global_dictionary_of_completed_info = {}
    dictionary_of_antibiotic_discs_from_database = {}
    global_sample_code = None

    # Globals
    global_image = global_isolate_name = global_scale_image = global_top_window_tkinter = global_unique_code = generalOpt = None
    imagefx = imagefxs = generals = showIm = valHolder = None
    isolatewindow = None
    global_top_window_tkinter_sp = None
    insertlist = []

    dictionary_of_discs_from_database = {}
    dictionary_of_association_from_database = {}

    cwdpath = "php-scripts/"
    url = "http://localhost:8085/open-amr/"
    domain = url + cwdpath
    imgurl = domain + "img/_discsfound_tryimg.png"
    discs_table = """ CREATE TABLE IF NOT EXISTS discs (
                                    disc_id integer PRIMARY KEY,
                                    diameter text NOT NULL,
                                    sample_id integer NOT NULL
                                ); """
    zones_table = """ CREATE TABLE IF NOT EXISTS zones (
                                    zone_id integer AUTO_INCREMENT PRIMARY KEY,
                                    disc TEXT NOT NULL,
                                    sample_id integer NOT NULL
                                ); """

    sQLitQuery(discs_table)
    sQLitQuery(zones_table)

    base = Tk()
    base.title("Open-AMR Susceptibility Testing - Debug")
    font = nametofont("TkDefaultFont")
    font.configure(size=20)
    base.option_add("*Font", font)

    # Image home directory
    imglocationhome = "assets/img/"
    tmpdiscfoundimg = "discsfound/"
    imgbase = "assets/testfiles/"

    # Images [Icons]
    icolocation = "assets/ico/"
    icoloc = icolocation + "icon.ico"

    backImg = PhotoImage(file=icolocation + "back.png")
    okImg = PhotoImage(file=icolocation + "ok.png")
    proceedImg = PhotoImage(file=icolocation + "proceed.png")
    editImg = PhotoImage(file=icolocation + "edit.png")
    plusImg = PhotoImage(file=icolocation + "plus.png")
    minusImg = PhotoImage(file=icolocation + "minus.png")

    set_window_icon_and_make_fullscreen(base)

    # UI - Main window
    cal.Label(base, text="OpenAMR Main Menu").pack(pady=10)
    mainFrame = cal.Frame(base, relief=SOLID, padding=20)
    cal.Button(mainFrame, text="Start a Test", command=start_test, width=dimensionWidth,
               padding=dimensionPadding).pack(pady=5)
    cal.Button(mainFrame, text="Print Label ", width=dimensionWidth, padding=dimensionPadding, command=printtext).pack(
        pady=5)
    r_widget = cal.Button(mainFrame, text="Result Report", width=dimensionWidth, padding=dimensionPadding,
                          command=lambda: threading.Thread(target=result_report).start())
    r_widget.pack(pady=5)
    cal.Button(mainFrame, text="Quit", width=dimensionWidth, command=base.destroy,
               padding=dimensionPadding).pack(pady=5)
    mainFrame.pack()
    base.mainloop()
