#! /usr/bin/env python

# todo
#   recalibrate mmppx after discs found; discs = 6mm, dish ~ 80 - 100 mm
#   adjust label positions to avoid overlap
#   add debug flag to save intermediate images

from collections import defaultdict
from pathlib import Path
from PIL import Image
from scipy import stats, ndimage, signal
import numpy as np
import math
import cv2


def save_image(img, f):
    Image.fromarray(img).save(f)


def load_image(f):
    return np.array(Image.open(f))


def rescale_image(img, factor=1.0):
    m, n = img.shape
    md, nd = round(m * factor), round(n * factor)
    return cv2.resize(img, (nd, md), interpolation=cv2.INTER_LANCZOS4)


def rescale_image_shape(img, shape):
    return cv2.resize(img, shape, interpolation=cv2.INTER_LANCZOS4)


def extract_bg(img, window=10):
    rows, cols = img.shape
    return np.mean(
        (img[0:window, 0:window],
         img[0:window, cols - window:cols],
         img[rows - window:rows, 0:window],
         img[rows - window:rows, cols - window:cols]))


def extract_fg(img, bg=0, epsilon=20):
    boxes = list()
    rows, cols = img.shape
    # binarize
    b_img = img <= (bg + epsilon)
    # background rows
    bg_rows = np.concatenate(([True],
                              b_img.all(axis=1),
                              [True]))
    # edge crossing between bg and fg
    bg_row_edges = np.diff(bg_rows)
    # start, end of each band of fg rows
    fg_row_ranges = np.where(bg_row_edges)[0]
    # pair (start, end) rows
    fg_row_ranges = fg_row_ranges.reshape((-1, 2))
    # background cols in each fg range
    for y0, y1 in fg_row_ranges:
        # background columns
        bg_cols = np.concatenate(([True],
                                  b_img[y0:y1].all(axis=0),
                                  [True]))
        bg_col_edges = np.diff(bg_cols)
        # start, end of each band of fg cols
        fg_col_ranges = np.where(bg_col_edges)[0]
        # pair (start, end) columns
        fg_col_ranges = fg_col_ranges.reshape((-1, 2))
        boxes.extend([((y1 - y0) * (x1 - x0),
                       (y0 + 1, y1 + 1, x0 + 1, x1 + 1))
                      for x0, x1 in fg_col_ranges])

    # extract largest fg object
    size, box = max(boxes)
    (y0, y1, x0, x1) = box
    return (y0, y1, x0, x1)


def crop(img, bounds):
    y0, y1, x0, x1 = bounds
    return img[y0:y1, x0:x1]


def crop_raw(raw_path):
    raw_img = Image.open(raw_path)
    rgb_img = np.uint8(raw_img)[:, :, :3]
    hsv_img = np.uint8(raw_img.convert('HSV'))
    val_img = hsv_img[:, :, 2]

    bg_val = extract_bg(val_img, window=100)
    fg_box = extract_fg(val_img, bg=bg_val)

    rgb_img = crop(rgb_img, fg_box)
    return rgb_img


def extract_dish(img):
    return ndimage.binary_fill_holes(img > extract_bg(img) + 10)


def resize_dish(img, factor=0.9):
    com = ndimage.measurements.center_of_mass(img)
    m, n = img.shape
    r = int(n / 2 * factor)
    mask = np.zeros((m, n), dtype='bool')
    y, x = map(int, map(round, com))
    b, a = np.ogrid[-y:m - y, -x:n - x]
    c = a * a + b * b <= r * r
    mask[c] = True
    return mask


def resize_discs(discs, factor=0.9):
    return {d: (x, y, int(round(ri * factor)), int(round(ro * factor)))
            for d, (x, y, ri, ro) in discs.items()}
    # return {d: (x,y,int(round(r*factor))) for d,(x,y,r) in discs.items()}


def save_discs(discs, f):
    Path(f).write_text(
        '\n'.join(
            ','.join(map(str, disc))
            for disc in discs.values()))


def load_discs(f):
    discs = {}
    lines = Path(f).read_text(encoding='U8').splitlines()
    for d, line in enumerate(lines):
        l = line.split(',')
        discs[d] = (int(l[0]), int(l[1]), float(l[2]), float(l[3]))
        # discs[d] = (int(l[0]), int(l[1]), float(l[2]))
    return discs


def save_zones(zones, f):
    Path(f).write_text(
        '\n'.join(
            ','.join(map(str, zone))
            for zone in zones.values()))


def load_zones(f):
    zones = {}
    lines = Path(f).read_text(encoding='U8').splitlines()
    for d, line in enumerate(lines):
        l = line.split(',')
        zones[d] = (int(l[0]), int(l[1]), int(l[2]), float(l[3]))
    return zones


def save_contours(contours, f):
    cfile = Path(f).with_suffix('')
    cdict = {str(d): np.squeeze(contour) for d, contour in enumerate(contours)}
    np.savez(cfile, **cdict)


def load_contours(f):
    cfile = Path(f).with_suffix('.npz')
    contours = np.load(cfile)
    return contours


def save_features(features, f):
    ffile = Path(f).with_suffix('')
    fdict = {str(d): np.squeeze(feature) for d, feature in features.items()}
    np.savez(ffile, **fdict)


def load_features(f):
    ffile = Path(f).with_suffix('.npz')
    features = np.load(ffile)
    return features


def save_abx_names(names, f):
    Path(f).write_text(
        '\n'.join(
            ','.join(map(str, name))
            for name in names.values()))


def load_abx_names(f):
    names = {}
    lines = Path(f).read_text(encoding='U8').splitlines()
    for d, line in enumerate(lines):
        l = line.split(',')
        names[d] = (l[0], int(l[1]))
    return names


def get_disc_locations(discs):
    return {int(d + 1): (x, y) for d, (x, y, ri, ro) in discs.items()}
    # return {int(d+1): (x,y) for d, (x,y,r) in enumerate(discs)}


def get_zone_diameters(zones):
    return [d for (x, y, r, d) in zones.values()]


def calc_diameter(img):
    com = ndimage.measurements.center_of_mass(img > 0)
    y, x = map(int, map(round, com))

    for i in range(min(img.shape[0] - y, img.shape[1] - x)):
        if img[y + i, x + i] == 0:
            max_y, max_x = y + i, x + i
            break

    for i in range(min(y, x)):
        if img[y - i, x - i] == 0:
            min_y, min_x = y - i, x - i
            break

    dy = max_y - min_y
    dx = max_x - min_x
    d = math.sqrt(dy * dy + dx * dx)
    return d


def calc_dish(dish):
    com = ndimage.measurements.center_of_mass(dish > 0)
    y, x = map(int, map(round, com))

    for i in range(min(dish.shape[0] - y, dish.shape[1] - x)):
        if dish[y + i, x + i] == 0:
            max_y, max_x = y + i, x + i
            break

    for i in range(min(y, x)):
        if dish[y - i, x - i] == 0:
            min_y, min_x = y - i, x - i
            break

    dy = max_y - min_y
    dx = max_x - min_x
    d = math.sqrt(dy * dy + dx * dx)
    r = int(math.ceil(d / 2))
    return (x, y), r


def draw_discs(img, discs):
    disloc = {}
    for d, disc in discs.items():
        draw_disc(img, disc)
        label = f'Disc {d + 1}'
        x, y, _, _ = disc
        disloc[d + 1] = (x, y)
        draw_label(img, x, y, label)
    return disloc


def draw_disc(img, disc):
    x, y, ri, ro = disc
    ri = int(round(ri))
    ro = int(round(ro))
    # width     = img.shape[1]
    # thickness = int(round(width /  600))
    thickness = 1
    cv2.circle(img, (x, y), ri, (255, 0, 0), thickness)
    cv2.circle(img, (x, y), ro, (255, 0, 0), thickness)


def draw_zones(img, zones):
    diameter = {}
    for z, zone in zones.items():
        draw_zone(img, zone)
        x, y, r, d = zone
        label = f'Disc {z + 1}: {d:.2f} mm'
        draw_label(img, x, y, label)
        diameter[z+1] = d
    return diameter


def draw_zone(img, zone):
    x, y, r, d = zone
    width = img.shape[1]
    thickness = int(round(width / 600))
    cv2.circle(img, (x, y), r, (255, 0, 0), thickness)


def draw_label(img, x, y, label, font=cv2.FONT_HERSHEY_SIMPLEX, color=(255, 0, 0)):
    width = img.shape[1]
    x_off = x - int(round(width / 20))
    y_off = y - int(round(width / 20))
    font_scale = (width / 1000)
    font_thick = int(round(width / 600))
    cv2.putText(img, label, (x_off, y_off), font, font_scale, color, font_thick)


def draw_contours(img, contours, color=(255, 0, 0), thickness=5):
    cv2.drawContours(img, contours, -1, color, thickness)


# apply threshold to image
#   return contours
def contours_from_thresh(img, thresh):
    _, ti = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(ti, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


# test whether a contour defines a valid disc based on
#   size, circularity, circumference, area
def valid_disc_contour(c, mmppx):
    # moments describe properties of the contour
    # https://docs.opencv.org/3.1.0/d8/d23/classcv_1_1Moments.html
    M = cv2.moments(c)
    area = cv2.contourArea(c) * mmppx * mmppx
    circumference = cv2.arcLength(c, True) * mmppx
    size = M['m00']

    if M['mu02'] > 0:
        circularity = M['mu20'] / M['mu02']
    else:
        circularity = 0

    if area > 0:
        roundness = circumference * circumference / (2 * 3.14159 * area)
    else:
        roundness = 0

    return (0 < size and
            (1 / 1.4) < circularity < 1.4 and  # 1/1.4, 1.4
            15 < circumference < 30 and  # 15, 30
            20 < area < 40 and  # 15, 40
            roundness < 3.1)  # 2.5


# return x,y coords and radius of disc defined by valid disc contour
def disc_from_contour(c):
    M = cv2.moments(c)
    circ = cv2.arcLength(c, True)
    radiusC = circ / (math.pi * 2)

    x = int(M["m10"] / M["m00"])
    y = int(M["m01"] / M["m00"])
    r = radiusC
    return (x, y, r, r)


# def find_discs(val_img):
def find_discs(rgb_img):
    hsv_img = np.uint8(Image.fromarray(rgb_img).convert('HSV'))
    val_img = hsv_img[:, :, 2]

    # subsample by a factor of 10 for speed
    s = 10
    val_sub = rescale_image(val_img, factor=(1 / s))

    dish = extract_dish(val_sub)
    dish_90 = resize_dish(dish, factor=0.9)
    diam_px = calc_diameter(dish)
    diam_mm = 90
    mmppx = diam_mm / diam_px

    r = round(round(diam_px / diam_mm) * 1.6)
    if r % 2 == 0:
        r += 1

    val_med = median_filter(val_sub, int(r))

    val_dish = val_med * dish_90

    discs = _find_discs(val_dish, mmppx)
    # rescale disc coordinates back to full resolution
    discs = {d: (x * s, y * s, ri * s, ro * s) for d, (x, y, ri, ro) in discs.items()}
    discs = refine_discs(val_img, discs)
    return discs


# input   gray/value channel image
#   brute-force search every threshold value to find max valid disc contours
#   threshold image with mean of threshold values that give max valid discs
# output  discs {d: (x, y, radius, radius)}
def _find_discs(img, mmppx):
    # brute-force search through all threshold values to find maximum valid discs
    counts = {x: sum(valid_disc_contour(c, mmppx) \
                     for c in contours_from_thresh(img, x))
              for x in range(256)}

    t = defaultdict(list)
    for threshold, count in counts.items():
        t[count].append(threshold)

    max_count = max(t.keys())
    best_thresh = np.median(t[max_count])
    # best_thresh = int( sum(t[max_count]) / len(t[max_count]) )

    valid = [disc_from_contour(c)
             for c in contours_from_thresh(img, best_thresh)
             if valid_disc_contour(c, mmppx)]
    return {d: disc for d, disc in enumerate(valid)}


def largest_object(mask):
    img, labels = ndimage.label(mask)
    count = np.count_nonzero
    counts = [(count(img == label), label) for label in range(1, 1 + labels)]
    _, largest = max(counts)
    return mask * (img == largest)


def refine_discs(val, discs):
    max_r = max(r for _, _, _, r in discs.values())
    strel = mask_discs((7, 7), {0: (3, 3, 3, 3)})
    r = max_r * 1.2

    # if max(val.shape) < 1000:
    #  strel = mask_discs((5,5), {0:(2,2,2,2)})
    #  r = max_r * 1.5
    # else:
    #  strel = mask_discs((7,7), {0:(3,3,3,3)})
    #  r = max_r * 1.2

    for d, disc in discs.items():
        x, y, _, _ = disc
        # binary mask from disc
        img = extract_disc(val, (x, y, r, r))
        t, _ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        mask = img < t
        # mask   = ndimage.binary_fill_holes(mask)

        # find inner radius, largest inscribed circle
        dist = ndimage.distance_transform_edt(mask)
        center = np.argmax(dist)
        yc, xc = np.unravel_index(center, dist.shape)
        ri = np.amax(dist)

        # filter markings and labels with circle of radius = 3
        mask = ndimage.binary_opening(mask, iterations=10, structure=strel)
        mask = largest_object(mask)

        # find outer radius, smallest circumscribed circle
        imask = np.ones(dist.shape)
        imask[yc, xc] = 0
        idist = ndimage.distance_transform_edt(imask)
        ro = np.amax(idist * mask)

        # adjust new center
        xr = int(x - r + 1) + xc
        yr = int(y - r + 1) + yc
        ri = int(round(ri - 0.5))
        ro = int(round(ro + 0.5))
        discs[d] = (xr, yr, ri, ro)

    return discs


def threshold_cwt(x, channel='sat'):
    hist = np.histogram(x, bins=range(256), density=True)
    counts = hist[0]
    values = hist[1][:-1]
    counts = conv_triangle(counts, 5)
    peaks = signal.find_peaks_cwt(counts, np.arange(7, 20))  # peak widths
    base = 0.001
    peaks = [p for p in peaks if counts[p] > base]

    if len(peaks) == 1:
        if channel == 'sat':
            t = 0 + 1
        elif channel == 'val':
            t = 255 - 1
    else:
        if channel == 'sat':
            lo = peaks[0] + 4
            hi = peaks[1] - 4
        elif channel == 'val':
            lo = peaks[-2] + 4
            hi = peaks[-1] - 4
        c, tc = min((count, val) for count, val in zip(counts[lo:hi], values[lo:hi]))
        to, _ = cv2.threshold(x, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if lo < to and to < hi:
            t = to
        else:
            t = tc

    return t, peaks


def conv_triangle(x, window):
    win = window // 2
    # pad with repeated edge values
    xpad = np.r_[np.repeat(x[0], win), x, np.repeat(x[-1], win)]
    # triangular window
    tri = np.r_[np.arange(1, win + 1), win + 1, np.arange(win, 0, -1)]
    tri = tri / np.sum(tri)
    # convolve
    return np.convolve(xpad, tri, mode='valid')


def threshold_relmax(x):
    hist = np.histogram(x, bins=range(256), density=True)
    counts = conv_triangle(hist[0], 5)
    values = hist[1][:-1]
    vals = [v for c, v in zip(counts, values) if c > 0]
    w = (max(vals) - min(vals)) // 10
    order = int(1.5 * w)
    peaks = [int(p) for p in signal.argrelmax(counts, order=order)[0]]
    peaks = [p for p in peaks if counts[p] > .001]

    to, _ = cv2.threshold(x, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if len(peaks) == 1:
        tc = 1
        t = 1
    else:
        lo = peaks[0]
        hi = peaks[1]
        c, tc = min((count, val) for count, val in zip(counts[lo:hi], values[lo:hi]))

        if lo < to and to < hi:
            t = to
        else:
            t = tc

    return t, peaks


def extract_zones_relmax(img, mask):
    x = img[mask > 0]
    t, _ = threshold_relmax(x)
    return np.uint8(img > t) * mask


def find_zones(rgb, discs):
    hsv = np.uint8(Image.fromarray(rgb).convert('HSV'))
    sat = hsv[:, :, 1]
    val = hsv[:, :, 2]

    dish = extract_dish(val)
    diam_mm = 90
    diam_px = calc_diameter(dish)
    pxpmm = diam_px / diam_mm

    # rescale sat from bias field
    mask = mask_all(val, discs)
    dish_sub = rescale_image(np.uint8(dish), factor=0.1)
    mask_sub = rescale_image(np.uint8(mask), factor=0.1)
    sat_sub = rescale_image(sat, factor=0.1)
    center, r = calc_dish(dish_sub)
    bias_sub = extract_bias(sat_sub * mask_sub, center, r * 0.8)
    sat_med = median_filter(np.uint8(sat_sub / bias_sub), 5)

    bias = rescale_image_shape(bias_sub, sat.shape[::-1])
    sat_scaled = np.uint8(sat / bias)

    # apply mask to sat
    mask_sub *= (sat_med > 0)
    sat_med *= mask_sub
    t, _ = threshold_relmax(sat_med[mask_sub > 0])
    # zone_mask  = extract_zones_relmax(sat_med, mask)
    zone_mask = np.uint8(sat_scaled > t) * mask
    zones = _find_zones(zone_mask, pxpmm, discs)
    return zones


def _find_zones(zone_mask, pxpmm, discs):
    def find_radii(discs):
        def find_radius(rn):
            count = np.count_nonzero
            for r in rn:
                circ = (radius == r)
                zone = zone_arr[circ]
                over = over_arr[circ]
                if count(zone) * 6 > (count(circ) - count(over)):
                    return r
            else:
                return 0

        # over_mask = mask_zones(height, width, zones)
        over_mask = mask_zones((height, width), zones)
        for d, disc in discs.items():
            r_px = 0  # r_disc

            # set array dims to multiply w/ circular masks, clipped to image bounds
            x_disc, y_disc, _, _ = disc

            y_min = max(y_disc - r_max, 0)
            x_min = max(x_disc - r_max, 0)
            y_max = min(y_disc + r_max, height)
            x_max = min(x_disc + r_max, width)

            x_m = x_max - x_min
            y_m = y_max - y_min
            x_c = x_disc - x_min
            y_c = y_disc - y_min
            shape = (y_m, x_m)
            center = (x_c, y_c)

            zone_arr = zone_mask[y_min:y_max, x_min:x_max]
            over_arr = over_mask[y_min:y_max, x_min:x_max]
            # radius   = mask_radius(y_m, x_m, x_c, y_c)
            radius = mask_radius(shape, center)
            r_px = find_radius(range(r_min, r_max, r_step))
            if r_px > r_min:
                r_last = max(r for r in range(r_min, r_max, r_step) if r < r_px)
                r_px = find_radius(range(r_last, r_px + 1, 1))
            elif r_px == r_min:
                r_px = r_disc

            zones[d] = (x_disc, y_disc, r_px, 2 * r_px / pxpmm)
            # print(f'zone {d}: {zones[d]}')

    zones = {}
    height, width = zone_mask.shape

    # set ring values to sample
    #        convert mm to px
    r_min = round(3.5 * pxpmm)
    r_max = round(25.0 * pxpmm)
    r_step = round(1.0 * pxpmm)
    r_disc = round(3.0 * pxpmm)

    find_radii(discs)
    unfound = {d: disc for d, disc in discs.items() if zones[d][2] == 0}
    # print(unfound)
    find_radii(unfound)

    return zones


def mask_radius(shape, center):
    m, n = shape
    x, y = center
    b, a = np.mgrid[-y:m - y, -x:n - x]
    r = np.sqrt((a * a) + (b * b))
    return np.floor(r)


def mask_disc_poly(shape, center, poly):
    m, n = shape
    x, y = center
    b, a = np.mgrid[-y:m - y, -x:n - x]
    r = np.sqrt((a * a) + (b * b))
    return poly(r) / poly(0)


def mask_disc_scaled(shape, center, radius, f):
    m, n = shape
    x, y = center
    b, a = np.ogrid[-y:m - y, -x:n - x]
    r = np.sqrt((a * a) + (b * b))
    rc = r / radius * f
    rc += 1
    return rc


def mask_discs(shape, discs, radius='outer'):
    m, n = shape
    mask = np.zeros(shape, dtype='bool')
    for disc in discs.values():
        x, y, ri, ro = disc
        if radius == 'inner':
            r = ri
        else:
            r = ro
        b, a = np.ogrid[-y:m - y, -x:n - x]
        c = a * a + b * b <= r * r
        mask[c] = True
    return mask


def mask_zones(shape, zones):
    m, n = shape
    mask = np.zeros(shape, dtype='bool')
    for zone in zones.values():
        x, y, r, _ = zone
        b, a = np.ogrid[-y:m - y, -x:n - x]
        c = a * a + b * b <= r * r
        mask[c] = True
    return mask


def mask_label(val, discs):
    # m, n   = val.shape
    # disc_mask = mask_discs(m, n, resize_discs(discs, factor=0.9))
    # disc_mask = mask_discs(val.shape, resize_discs(discs, factor=0.9))
    disc_mask = mask_discs(val.shape, discs, radius='inner')
    thresh = np.percentile(val[disc_mask > 0], 90)  # thresh < 90% disc max
    mask = (val < thresh)
    return mask


def mask_shadow(val):
    h = np.histogram(val[val > 0], bins=range(256))
    counts = np.log10(h[0] + 1)
    values = h[1][:-1]
    thresh = [value for count, value in zip(counts, values) if count >= 3.1][0]
    mask = (val < thresh)
    return mask


def mask_all(val, discs):
    labl_mask = mask_label(val, discs)
    dish_mask = resize_dish(extract_dish(val), factor=0.8)
    disc_mask = mask_discs(val.shape, discs)  # resize_discs(discs, factor=1.2))
    temp_mask = (dish_mask > 0) * (disc_mask == 0) * (labl_mask == 0)
    val_med = median_filter(val, 5)
    shdw_mask = mask_shadow(val_med * temp_mask)
    mask = temp_mask * (shdw_mask == 0)
    return mask


def median_filter(img, r):
    return median_filter_sp_fp(img, r)


def median_filter_cv(img, r):
    return cv2.medianBlur(img, r)


def median_filter_sp(img, r):
    return ndimage.filters.median_filter(img, size=r)


def median_filter_sp_fp(img, r):
    # footprint = mask_discs(r,r, [(r//2, r//2, r//2)])
    shape = (r, r)
    discs = {0: (r // 2, r // 2, r // 2, r // 2)}
    footprint = mask_discs(shape, discs)
    return ndimage.filters.median_filter(img, footprint=footprint)


def adjust_zones(zones, disc, adjustment_mm):
    x, y, r_px, d_mm = zones[disc]
    d_px = 2 * r_px
    pxpmm = d_px / d_mm
    d_mm += adjustment_mm
    d_px += adjustment_mm * pxpmm
    r_px = int(round(d_px / 2))
    zones[disc] = (x, y, r_px, d_mm)
    return zones


def radial_histogram(img, center, radius):
    m, n = img.shape
    x, y = center

    b, a = np.mgrid[-y:m - y, -x:n - x]
    r = np.floor(np.sqrt((a * a) + (b * b)))
    rn = np.arange(0, radius, dtype='uint16')
    prob = np.zeros([rn.size, 255])

    r = r[img > 0]
    img = img[img > 0]

    for ri in rn:
        prob[ri] = np.histogram(img[r == ri], bins=range(256), density=True)[0]

    return prob, rn


def extract_bias(img, center, radius):
    return extract_bias_poly(img, center, radius, deg=1)


def extract_bias_linalg(img, center, radius):
    # threshold inhibited peaks
    t, _ = threshold_cwt(img[img > 0])
    img[img < t] = 0

    # extract growth peak and fit line
    # radius *= 0.8 # adjust dish radius to 80%
    prob, rn = radial_histogram(img, center, radius)
    r = len(rn)
    peak = np.zeros([rn.size])

    for ri in rn:
        peaks = signal.find_peaks_cwt(prob[ri], np.arange(7, 20))
        peaks = [(prob[ri][p], p) for p in peaks if p > .001]
        if len(peaks):
            peak[ri] = max(peaks)[1]
        else:
            peak[ri] = 0

    # make matrix of radii and peak values for least squares fit
    A = np.vstack([rn[peak > 0], np.ones(len(rn[peak > 0]))]).T
    slope, intercept = np.linalg.lstsq(A, peak[peak > 0], rcond=None)[0]
    scale = slope * r / intercept
    # print(scale)

    # make bias field to correct shading
    bias = mask_disc_scaled(shape, center, r, scale)

    return bias


def extract_bias_poly(img, center, radius, deg=1):
    # threshold inhibited peaks
    t, _ = threshold_cwt(img[img > 0])
    img[img < t] = 0

    # extract growth peak and fit line
    # radius *= 0.8 # adjust dish radius to 80%
    prob, rn = radial_histogram(img, center, radius)
    r = len(rn)
    peak = np.zeros([rn.size])

    for ri in rn:
        peaks = signal.find_peaks_cwt(prob[ri], np.arange(7, 20))
        peaks = [(prob[ri][p], p) for p in peaks if p > .001]
        if len(peaks):
            peak[ri] = max(peaks)[1]
        else:
            peak[ri] = 0

    # apply polyfit
    x = rn[peak > 0]
    y = peak[peak > 0]
    z = np.polyfit(x, y, deg=deg)
    p = np.poly1d(z)

    # make bias field to correct shading
    bias = mask_disc_poly(img.shape, center, p)

    return bias


def extract_disc(img, disc):
    x, y, ri, ro = disc
    return img[int(y - ro + 1)
               :int(y + ro + 1),
           int(x - ro + 1)
           :int(x + ro + 1)]


def extract_disc_text(img):
    # create disc mask and 90% disc mask
    m, n = img.shape
    r = m // 2
    r90 = int(0.9 * m) // 2
    msk = np.uint8(mask_discs(img.shape, {0: (r, r, r, r)}))
    msk90 = np.uint8(mask_discs(img.shape, {0: (r, r, r90, r90)}))
    # fill area around mask with mean value to limit mask edge artifacts
    #   from adaptive threshold
    mean = int(round(np.mean(img[msk > 0])))
    inv = 1 - msk
    fill = (img * msk) + (inv * mean)

    med = median_filter_sp(fill, 3)
    med2 = median_filter_sp(img * msk90, 3)
    vals = med2[msk90 > 0]

    # apply global threshold to find area of disc where text is located
    thresh = int(np.mean(vals) - np.std(vals))
    t, gth = cv2.threshold(med2, thresh, 255, cv2.THRESH_BINARY)

    # apply local threshold to find text edges (still noisy outside text area)
    ath = cv2.adaptiveThreshold(med, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                cv2.THRESH_BINARY, 21, 1)

    # combine both thresholded images to get sharp text edges without noise
    txt = (gth == 0) * (ath == 0) * (msk90 > 0)
    txt = np.uint8(ndimage.binary_opening(txt)) * 255
    return txt


def find_features(rgb_img, discs):
    # convert rgb to hsv
    hsv_img = np.uint8(Image.fromarray(rgb_img).convert('HSV'))
    val_img = hsv_img[:, :, 2]

    features = {}
    keypoints = {}

    # create ORB descriptor
    orb = cv2.ORB_create(200,
                         scaleFactor=1.1,
                         nlevels=20,
                         edgeThreshold=10,
                         firstLevel=0,
                         WTA_K=2,
                         patchSize=50)

    for d, disc in discs.items():
        # get val sub-image of disc
        disc_img = extract_disc(val_img, disc)

        # binarize text vs non-text in disc
        disc_txt = extract_disc_text(disc_img)

        # extract features
        keypoints[d], features[d] = orb.detectAndCompute(disc_txt, None)

    return features


def load_descriptors(d):
    d = Path(d)
    descriptors = {}
    for feature_file in d.glob('*.npz'):
        dish = feature_file.stem
        features = load_features(feature_file)
        for disc in features.keys():
            descriptors[f'{dish}_{disc}'] = features[disc]
    return descriptors


def load_identifiers(f):
    lines = Path(f).read_text(encoding='U8').splitlines()
    return {disc: abx for disc, _, abx in map(lambda l: l.partition('  '), lines)}


def distances_to_score(distances, cutoff=11):
    return sum(cutoff - d for d in distances if 0 < d and d < cutoff)


def match_features(features, descriptors_dir):
    # load feature descriptors for previously seen discs
    descriptors = load_descriptors(descriptors_dir)
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = {}

    for disc, feature in features.items():
        distances = {i: [d.distance for d in matcher.match(descriptors[i], feature)]
                     for i in descriptors.keys()}
        scores = {i: distances_to_score(d) for i, d in distances.items()}
        matches[disc] = sorted(((score, i) for i, score in scores.items() if score > 0), reverse=True)

    return matches


def identify_matches(matches, abx_key):
    abx_ids = load_identifiers(abx_key)
    abx_names = {disc: [(abx_ids[name], score) for score, name in match]
                 for disc, match in matches.items()}
    return abx_names


def search_discs(rgb_img, discs, descriptors_dir=r'descriptors', abx_key=r'abx_key.txt'):
    features = find_features(rgb_img, discs)
    matches = match_features(features, descriptors_dir)
    abx_names = identify_matches(matches, abx_key)
    # return only top match
    abx_names = {disc: names[0] if len(names) else ('', 0.0)
                 for disc, names in abx_names.items()}
    return abx_names

# def mask_circ(m, n, x, y, r1, r0):
#  #https://stackoverflow.com/questions/8647024/
#  #  how-to-apply-a-disc-shaped-mask-to-a-numpy-array
#  mask = np.zeros((m, n), dtype='bool')
#  b,a  = np.ogrid[-y:m-y, -x:n-x]
#  c1   = a*a + b*b <= r1*r1
#  mask[c1] = True
#  c0   = a*a + b*b <= r0*r0
#  mask[c0] = False
#  return mask
#
# def mask_circ2(mask, x, y, r1, r0):
#  m,n  = mask.shape
#  b,a  = np.ogrid[-y:m-y, -x:n-x]
#  mask[:]  = False
#  c1   = a*a + b*b <= r1*r1
#  mask[c1] = True
#  c0   = a*a + b*b <= r0*r0
#  mask[c0] = False
#  return mask
#
# def mask_radius(m, n, x, y):
#  b,a  = np.mgrid[-y:m-y, -x:n-x]
#  bb   = b*b
#  aa   = a*a
#  return np.floor(np.sqrt(bb + aa))
#
# def mask_disc_poly(m, n, x, y, p):
#  b,a  = np.mgrid[-y:m-y, -x:n-x]
#  bb   = b*b
#  aa   = a*a
#  r    = np.sqrt(bb + aa)
#  mask = p(r) / p(0)
#  return mask
#
# def mask_disc_scaled(m, n, x, y, r, f):
#  #mask = np.ones((m,n), dtype='float')
#  b,a  = np.ogrid[-y:m-y, -x:n-x]
#  rc   = np.sqrt((a*a) + (b*b)) / r * f
#  rc  += 1
#  return rc
#
# def mask_discs(m, n, discs):
#  mask = np.zeros((m, n), dtype='bool')
#  for disc in discs.values():
#    x, y, r = disc
#    b,a = np.ogrid[-y:m-y, -x:n-x]
#    c   = a*a + b*b <= r*r
#    mask[c] = True
#  return mask
#
# def mask_zones(m, n, zones):
#  mask = np.zeros((m, n), dtype='bool')
#  for zone in zones.values():
#    x, y, r, _ = zone
#    b,a = np.ogrid[-y:m-y, -x:n-x]
#    c   = a*a + b*b <= r*r
#    mask[c] = True
#  return mask

# def radial_histogram(img, dish):
#  center, radius = calc_dish(dish)
#  return rad_hist(img, center, radius)
#  #diam = calc_diameter(dish)
#  #rd   = int(math.ceil(diam/2))
#  #y,x  = map(int, map(round, ndimage.measurements.center_of_mass(dish>0)))
#  #return rad_hist(img, (x,y), rd)
#
#  #m,n  = img.shape
#  #b,a  = np.mgrid[-y:m-y, -x:n-x]
#  #bb   = b*b
#  #aa   = a*a
#  #r    = np.floor(np.sqrt(bb + aa))
#  #rn   = np.arange(0, rd, dtype='uint16')
#  #prob = np.zeros([rn.size, 255])
#  #
#  #r    = r[img>0]
#  #img  = img[img>0]
#  #
#  #for ri in rn:
#  #  prob[ri] = np.histogram(img[r == ri], bins=range(256), density=True)[0]
#  #
#  #return prob, rn

# def rad_hist(img, center, radius):
#  x,y  = center
#
#  m,n  = img.shape
#  b,a  = np.mgrid[-y:m-y, -x:n-x]
#  bb   = b*b
#  aa   = a*a
#  r    = np.floor(np.sqrt(bb + aa))
#  rn   = np.arange(0, radius, dtype='uint16')
#  prob = np.zeros([rn.size, 255])
#
#  r    = r[img>0]
#  img  = img[img>0]
#
#  for ri in rn:
#    prob[ri] = np.histogram(img[r == ri], bins=range(256), density=True)[0]
#
#  return prob, rn
#
# def extract_bias(img, dish):
#  # threshold inhibited peaks
#  t, _ = threshold_cwt(img[img>0])
#  img[img<t] = 0
#  # extract growth peak and fit line
#  dish = resize_dish(dish, factor=0.8)
#  prob, rn = radial_histogram(img, dish)
#  r = len(rn)
#  peak = np.zeros([rn.size])
#  
#  for ri in rn:
#    peaks = signal.find_peaks_cwt(prob[ri], np.arange(7,20))
#    peaks = [(prob[ri][p],p) for p in peaks if p > .001]
#    if len(peaks):
#      peak[ri] = max(peaks)[1]
#    else:
#      peak[ri] = 0
#
#  # make matrix of radii and peak values for least squares fit
#  A     = np.vstack([rn[peak>0], np.ones(len(rn[peak>0]))]).T
#  slope, intercept = np.linalg.lstsq(A, peak[peak>0], rcond=None)[0]
#  scale = slope * r / intercept
#  #print(scale)
#
#  # make bias field to correct shading
#  m,n  = img.shape
#  y,x  = map(int, map(round, ndimage.measurements.center_of_mass(dish>0)))
#  bias = mask_disc_scaled(m,n, x,y, r, scale)
#
#  return bias
#
# def extract_bias_poly(img, dish, deg=1):
#  # threshold inhibited peaks
#  t, _ = threshold_cwt(img[img>0])
#  img[img<t] = 0
#  # extract growth peak and fit line
#  dish = resize_dish(dish, factor=0.8)
#  prob, rn = radial_histogram(img, dish)
#  r = len(rn)
#  peak = np.zeros([rn.size])
#  
#  for ri in rn:
#    peaks = signal.find_peaks_cwt(prob[ri], np.arange(7,20))
#    peaks = [(prob[ri][p],p) for p in peaks if p > .001]
#    if len(peaks):
#      peak[ri] = max(peaks)[1]
#    else:
#      peak[ri] = 0
#
#  # apply polyfit
#  x = rn[peak>0]
#  y = peak[peak>0]
#  z = np.polyfit(x, y, deg=deg)
#  p = np.poly1d(z)
#
#  # make bias field to correct shading
#  m,n  = img.shape
#  y,x  = map(int, map(round, ndimage.measurements.center_of_mass(dish>0)))
#  bias = mask_disc_poly(m,n, x,y, p)
#
#  return bias

# def contours_from_thresh2(img, thresh, mmppx):
#  #_, ti       = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)
#  mask        = img < thresh
#  strel       = mask_discs((6,6), {0:(3,3,3,3)})
#  mask        = ndimage.binary_opening(mask, iterations=10, structure=strel)
#  li, labels  = ndimage.label(mask)
#  sizes       = {label: np.count_nonzero(li == label)*mmppx*mmppx 
#                  for label in range(1, 1+labels)}
#  labels      = {l for l,s in sizes.items() 
#                  if 15 < s and s < 36}
#  mask        = np.zeros(mask.shape)
#  for l in labels:
#    mask += (li == l)
#  contours, _ = cv2.findContours(np.uint8(mask)*255, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#  return contours

# def valid_disc_contour(c, mmppx):
#  # moments describe properties of the contour
#  # https://docs.opencv.org/3.1.0/d8/d23/classcv_1_1Moments.html
#  M             = cv2.moments(c)
#  area          = cv2.contourArea(c)     * mmppx * mmppx
#  circumference = cv2.arcLength(c, True) * mmppx
#  size          = M['m00']
#
#  if M['mu02'] > 0:
#    circularity = M['mu20'] / M['mu02']
#  else:
#    circularity = 0
#  if area > 0:
#    roundness = circumference * circumference / (2 * 3.14159 * area)
#  else:
#    roundness = 0
#
#  return (       0 < size                 and
#         (1 / 1.2) < circularity   <  1.2 and
#                15 < circumference < 25   and   #   500,   800
#                15 < area          < 36   and   # 15000, 30000
#                     roundness     <  2.5   )   # k

# def find_discs(rgb_img):
#  #rgb_img  = Image.open(rgb_path)
#  hsv_img  = np.uint8(Image.fromarray(rgb_img).convert('HSV'))
#  val_img  = hsv_img[:,:,2]
#
#  dish     = extract_dish(val_img)
#  dish_90  = resize_dish(dish, factor=0.9)
#  diam_mm  = 90
#  diam_px  = calc_diameter(dish)
#  mmppx    = diam_mm / diam_px
#  
#  r = round(round(diam_px / diam_mm) * 1.6)
#  if r % 2 == 0:
#    r += 1
#
#  val_med  = median_filter(val_img, int(r))
#
#  val_dish = val_med * dish_90
#
#  discs    = _find_discs(val_dish, mmppx)
#  discs    = refine_discs(val_dish, discs)
#  return discs

# def _find_discs(img, mmppx):
#  # brute-force search through all threshold values to find maximum valid discs
#  counts  = {x: sum(valid_disc_contour(c, mmppx) \
#                for c in contours_from_thresh(img, x))
#              for x in range(256)}
#
#  t = defaultdict(list)
#  for threshold, count in counts.items():
#    t[count].append(threshold)
#
#  max_count   = max(t.keys())
#  best_thresh = int( sum(t[max_count]) / len(t[max_count]) )
#
#  return [disc_from_contour(c) 
#           for c in contours_from_thresh(img, best_thresh)
#           if valid_disc_contour(c, mmppx)]

# def compare_thresholds_relmax(img, mask):
#  x      = img[mask>0]
#  t, to, tc, peaks, counts, values = threshold_relmax(x)
#  return (t, to, tc, peaks, counts, values)
#
# def threshold_relmax(x):
#  hist   = np.histogram(x, bins=range(256), density=True)
#  counts = conv_triangle(hist[0], 5)
#  values = hist[1][:-1]
#  vals   = [v for c,v in zip(counts,values) if c > 0]
#  w      = (max(vals) - min(vals)) // 10
#  order  = int(1.5*w)
#  peaks  = [int(p) for p in signal.argrelmax(counts, order=order)[0]]
#  peaks  = [p for p in peaks if counts[p] > .001]
#
#  to,_ = cv2.threshold(x, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#
#  if len(peaks) == 1:
#    tc   = 1
#    t    = 1
#  else:
#    lo   = peaks[0]
#    hi   = peaks[1]
#    c,tc = min((count,val) for count, val in zip(counts[lo:hi], values[lo:hi]))
#
#    if lo < to and to < hi:
#      t = to
#    else:
#      t = tc
#
#  return t, to, tc, peaks, counts, values
#
# def extract_zones_relmax(img, mask):
#  x           = img[mask>0]
#  t,_,_,_,_,_ = threshold_relmax(x)
#  return np.uint8(img > t) * mask

# def find_zones(rgb, discs):
#  hsv        = np.uint8(Image.fromarray(rgb).convert('HSV'))
#  sat        = hsv[:,:,1]
#  val        = hsv[:,:,2]
#
#  dish       = extract_dish(val)
#  diam_mm    = 90
#  diam_px    = calc_diameter(dish)
#  mmppx      = diam_mm / diam_px
#  pxpmm      = diam_px / diam_mm
#  center, r  = calc_dish(dish)
#
#  # rescale sat from bias field
#  mask       = mask_all(val, discs)
#  #bias       = extract_bias(sat*mask, dish)
#  bias       = extract_bias(sat*mask, center, r*0.8)
#  sat_scaled = np.uint8(sat/bias)
#  # median_filter rescaled sat
#  sat_med    = median_filter(sat_scaled, 25)
#  # apply mask to sat
#  mask      *= (sat_med>0)
#  sat_med   *= mask
#  zone_mask  = extract_zones_relmax(sat_med, mask)
#  zones      = _find_zones(zone_mask, pxpmm, discs)
#  return zones

# def find_zones2(sat_med, discs, dish, mask):
#  diam_mm    = 90
#  diam_px    = calc_diameter(dish)
#  #mmppx      = diam_mm / diam_px
#  pxpmm      = diam_px / diam_mm
#
#  # apply mask to sat
#  mask      *= (sat_med>0)
#  sat_med   *= mask
#  zone_mask  = extract_zones_relmax(sat_med, mask)
#  zones      = _find_zones(zone_mask, pxpmm, discs)
#  return zones
