import datetime
import shutil
import urllib
import urllib.request
import urllib.request
from pathlib import Path

import cv2
import numpy as np
import requests
import openAMR as funcall


def exceptionprint(name, e_name):
    print(name, " : ", e_name)


def requestpost(filename, param):
    try:
        return requests.post(domain + str(filename) + ".php", param, timeout=None)
    except Exception as e_net:
        exceptionprint("requestpost", e_net)


# noinspection PyUnusedLocal
def set_test_phase(status, filename="setTestStatus", cond=False):
    value = "prog"
    if cond:
        returnTrue(filename, {"prog": status})
    if not cond:
        returnTrue(filename, {"status": status})


def transactionReset():
    while True:
        try:
            resetTransaction = requestpost("transactionTerminate", {})
            if resetTransaction.status_code == 200:
                return
        except Exception as e_res:
            exceptionprint("resetTransaction", e_res)


# noinspection PyGlobalUndefined
def get_test_id():
    global _id
    while True:
        try:
            get_id = requestpost("getTestId", {})
            if get_id.status_code != 200:
                transactionReset()
            elif get_id.status_code == 200:
                for d in get_id.json()["samples"]:
                    if d["sample_id"] is None:
                        _id = 0
                    else:
                        _id = int(d["sample_id"])
                return _id + 1
        except Exception as e_t:
            exceptionprint("get_id", e_t)


def new_abx_code(_id, newvalues):
    starttime = datetime.datetime.now()
    raw_dir = Path(r'' + imgbase + str(_id) + '/raw')  # raw input images
    raw_path = raw_dir / 'tryimg.png'
    discs_abx_dir = Path(r'' + imgbase + str(_id) + '/discs_abx')  # discs abx text as text files
    discs_abx_path = discs_abx_dir / f'{_id}.txt'
    rgb_img = funcall.crop_raw(raw_path)
    discs = funcall.find_discs(rgb_img)
    descriptors_dir = Path(r'descriptors')  # saved features used in abx_key
    abx_names = funcall.search_discs(rgb_img, discs)
    # new_abx = {}
    # val = _id
    val = "0" + str(_id) if _id < 10 else _id
    features_path = descriptors_dir / f'{val}.npz'
    filepath = "abx_key.txt"
    #
    # print(newvalues)dictionary_of_association_from_database[dt]["resistance"]
    # print(abx_names)

    createnumyarr = False
    new_abx = {}
    for d in abx_names:
        new_abx[d] = (newvalues[d], abx_names[d][1])
    for i in abx_names:
        if newvalues[i] != abx_names[i][0]:
            createnumyarr = True
            if createnumyarr:
                for i in abx_names:
                    with open(filepath, "a+") as file_handler:
                        file_handler.write(str(val) + '_' + str(i) + '  ' + newvalues[i] + '\n')
                        file_handler.close()
                funcall.save_abx_names(abx_names, discs_abx_path)
                features = funcall.find_features(rgb_img, discs)
                funcall.save_features(features, features_path)
                break
    createnumyarr = False

    print("New Match Duration", (datetime.datetime.now() - starttime).seconds, "sec")


def locatediscs(_id):
    shutil.move("tryimg.png", imgbase + str(_id) + "/raw/tryimg.png")
    rgb_dir = Path(r'' + imgbase + str(_id) + '/rgb')
    discs_dir = Path(r'' + imgbase + str(_id) + '/discs')
    discs_path = discs_dir / (str(_id) + '.txt')
    raw_dir = Path(r'' + imgbase + str(_id) + '/raw')  # raw input images
    raw_path = raw_dir / 'tryimg.png'
    rgb_path = rgb_dir / f'{_id}.png'
    discs_rgb_dir = Path(r'' + imgbase + str(_id) + '/discs_rgb')  # discs drawn on rgb image
    discs_rgb_path = discs_rgb_dir / f'{_id}.png'
    zones_dir = Path(r'' + imgbase + str(_id) + '/zones')
    zones_path = zones_dir / f'{_id}.txt'
    rgb_img = funcall.crop_raw(raw_path)
    funcall.save_image(rgb_img, rgb_path)
    discs = funcall.find_discs(rgb_img)
    funcall.save_discs(discs, discs_path)
    abx_names = funcall.search_discs(rgb_img, discs)
    funcall.get_disc_locations(discs)
    rgb_discs = funcall.load_image(rgb_path)
    funcall.draw_discs(rgb_discs, discs)
    funcall.save_image(rgb_discs, discs_rgb_path)
    zones = funcall.find_zones(rgb_img, discs)
    funcall.save_zones(zones, zones_path)
    return abx_names


def returnTrue(filename, param):
    while True:
        try:
            _n1 = requestpost(filename, param)
            if _n1.status_code == 200:
                for _i in _n1.text:
                    if _i == "1":
                        return True
            elif _n1.status_code != 200:
                transactionReset()
        except Exception as e_rt:
            exceptionprint("returnTrue", e_rt)


def dowload_img():
    while True:
        try:
            imgrequest = urllib.request.urlopen(imgurl)
            downloadimg = np.asarray(bytearray(imgrequest.read()), dtype=np.uint8)
            downimg = cv2.imdecode(downloadimg, -1)
            cv2.imwrite("tryimg.png", downimg)
            return
        except Exception as e_im:
            exceptionprint("locateImgdisc", e_im)


# noinspection PyShadowingNames
def mkdirector(test_id):
    raw_dir = Path(r'' + imgbase + str(test_id) + '/raw')
    rgb_dir = Path(r'' + imgbase + str(test_id) + '/rgb')
    discs_dir = Path(r'' + imgbase + str(test_id) + '/discs')
    zones_dir = Path(r'' + imgbase + str(test_id) + '/zones')
    feat_dir = Path(r'' + imgbase + str(test_id) + '/feat')
    discs_rgb_dir = Path(r'' + imgbase + str(test_id) + '/discs_rgb')  # discs drawn on rgb image
    discs_abx_dir = Path(r'' + imgbase + str(test_id) + '/discs_abx')  # discs abx text as text files
    zones_rgb_dir = Path(r'' + imgbase + str(test_id) + '/zones_rgb')  # zones drawn on rgb image
    zones_adj_dir = Path(r'' + imgbase + str(test_id) + '/zones_adj')  # adjusted zones as text files
    zones_rgb_adj_dir = Path(r'' + imgbase + str(test_id) + '/zones_rgb_adj')  # adjusted zones draw on rgb img

    for d in [raw_dir,
              rgb_dir,
              discs_dir,
              discs_rgb_dir,
              discs_abx_dir,
              zones_dir,
              zones_rgb_dir,
              zones_adj_dir,
              feat_dir,
              zones_rgb_adj_dir]:
        d.mkdir(parents=True, exist_ok=True)


# noinspection PyUnboundLocalVariable,PyShadowingNames,SpellCheckingInspection
def locateImgdisc():
    print("================")
    print("Locate discs")
    starttime = datetime.datetime.now()
    global test_id
    dowload_img()
    test_id = get_test_id()

    mkdirector(test_id=test_id)
    discs = locatediscs(_id=test_id)

    antibioticfound = dict()
    for f, nm in discs.items():
        for k, name in enumerate(nm):
            if k == 0:
                antibioticfound[f] = name
    set_test_phase(0)
    print(len(discs), "discs found")
    shutil.copy(imgbase + str(test_id) + "/discs_rgb/" + str(test_id) + ".png",
                imglocationhome + "discsfound/discsfound.png")
    if returnTrue("emptyTempTable", {}):
        for _, val in antibioticfound.items():
            returnTrue("insertTempAntibiotic", {"temp_abx": val})
    set_test_phase(2)

    print("Duration", (datetime.datetime.now() - starttime).seconds, "sec")
    set_test_phase(1, cond=True)
    print("================")
    print()


def process_img():
    global test_id
    test_id, discs = get_test_id(), {}
    set_test_phase(1, cond=True)
    set_test_phase(5)
    test_id -= 1
    print("================")
    starttime = datetime.datetime.now()
    print(test_id)
    getTestant = requestpost("getAntibioticsToProcess", {"sample_id": test_id})
    if getTestant.status_code != 200:
        transactionReset()
    elif getTestant.status_code == 200:
        for _k, ant in enumerate(getTestant.json()["abx_name_obj"]):
            discs[_k] = ant["abx_code"]

    print("Find zones")
    new_abx_code(test_id, discs)

    raw_dir = Path(r'' + imgbase + str(test_id) + '/raw')
    zones_dir = Path(r'' + imgbase + str(test_id) + '/zones')

    raw_path = raw_dir / (str(file) + '.png')
    zones_path = zones_dir / (str(file) + '.txt')
    rgb_dir = Path(r'' + imgbase + str(test_id) + '/rgb')
    zones_rgb_dir = Path(r'' + imgbase + str(test_id) + '/zones_rgb')  # zones drawn on rgb image
    zones_rgb_path = zones_rgb_dir / f'{test_id}.png'
    rgb_path = rgb_dir / f'{test_id}.png'

    rgb_img = funcall.crop_raw(raw_path)
    disks = funcall.find_discs(rgb_img)
    funcall.get_disc_locations(disks)

    zones = funcall.find_zones(rgb_img, disks)
    funcall.save_zones(zones, zones_path)

    # draw zones on rgb image
    rgb_zones = funcall.load_image(rgb_path)
    discloc = funcall.draw_discs(rgb_zones, disks)

    newdis = funcall.draw_zones(rgb_zones, zones)
    funcall.save_image(rgb_zones, zones_rgb_path)

    dists = {}

    set_test_phase(2, cond=True)

    if returnTrue("deleteZoneIfFound", {"sample_id": test_id}):
        for a in discloc:
            returnTrue("insertTestZone",
                       {"discs": str(discloc[a]),
                        "sample_id": test_id})
    for _d in newdis:
        dists[_d] = newdis[_d]

    while True:
        getTestdisc = requestpost("getDiscId", {"sample_id": test_id})
        if getTestdisc.status_code == 200:
            for dis, disc_num in zip(dists,
                                     getTestdisc.json()["discs"]):
                updateDiscdata = {"distances": (dists[dis]),
                                  "sample_id": test_id,
                                  "disc_num": disc_num["disc_id"]}
                returnTrue("updateDisc", updateDiscdata)
            break
        elif getTestdisc.status_code != 200:
            transactionReset()

    shutil.copy(imgbase+str(test_id) + "/zones_rgb/" + str(test_id) + ".png",
                imglocationhome + "zonesfoundIm" + str(test_id) + ".png")
    set_test_phase(3, cond=True)
    set_test_phase(6)
    set_test_phase(4, cond=True)
    print("Duration", (datetime.datetime.now() - starttime).seconds, "sec")
    print("================")
    print()


if __name__ == '__main__':

    imglocationhome = "assets/img/"
    url = "http://localhost:8085/open-amr/"
    cwdpath = "php-scripts/"
    domain = url + cwdpath
    imgurl = url + "img/tryimg.png"
    set_test_phase(4)
    test_id = 0
    imgbase = "assets/testfiles/"
    file = "tryimg"
    while True:
        try:
            getStatus = requestpost("getTestStatus", {})
            if getStatus.status_code == 200:
                for state in getStatus.json()["teststatus"]:
                    if state["status"] == "1":
                        locateImgdisc()
                    elif state["status"] == "4":
                        process_img()
        except Exception as e_start:
            exceptionprint("Main process", e_start)
