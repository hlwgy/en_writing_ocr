"""
常用的图片处理相关工具类
包括：
1、预处理图片：二值化、开运算、寻找边框
2、对整张进行按行切割
3、对单行图片进行按列切割
4、处理单个字符，形成固定大小的图片
"""
from debug_tool import show_img
import cv2
import numpy as np
import random

is_debug = False

#   ===预处理图片:读入并形成寻找边框后的二值化图片============
def img_pre(image):
    # 灰度 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # show_img(gray)
    # 二值化
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # show_img(thresh)
    # 开运算去除小点
    mopen_size = 3 # 开运算的大小，可以是具体数值，可以是比例
    kernel_open = np.ones((mopen_size, mopen_size), np.uint8)  # 去小点
    thresh_open = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_open)
    # show_img(thresh_open)
    # 寻找边框
    x, y, img_w, img_h = cv2.boundingRect(thresh_open)  # 找边框
    left, top, right, bottom = x, y, x+img_w, y+img_h
    bound_thresh = thresh[top:bottom, left:right]
    # show_img(bound_thresh)

    return bound_thresh

#  === 对整张进行按行切割，获得标注信息 =====================
def img2rows(bound_thresh):
    """
        按行求和，横向切割
    """
    # 
    bound_thresh_b = bound_thresh.copy()
    bound_thresh_b[bound_thresh_b == 255] = 1
    row_sums = np.sum(bound_thresh_b, axis=1)
    # 
    img_h,img_w = bound_thresh.shape[0:2]
    min_w = int(0.05*img_w) # 最小宽度
    min_h = 3 # 最小高度
    rows = []
    is_satrt = False  # 是否开始
    row_len = len(row_sums)
    for i, row_v in enumerate(row_sums):
        if not is_satrt and row_v > min_w:  # 没开始&有数据
            is_satrt = True
            row = {}
            row["start"] = i
        if is_satrt and (row_v < min_w or i+1 >= row_len):  # 已开始&（没数据|结束）
            is_satrt = False
            row["end"] = i
            # 太窄不记录
            if (row["end"] - row["start"]) > min_h:
                rows.append(row)

    if is_debug:
        image_copy = bound_thresh.copy()
        for i, row in enumerate(rows):
            left, top, right, bottom = 0, row["start"], img_w, row["end"]
            cv2.rectangle(image_copy, (left, top), (right, bottom),  (255, 255, 255), 2)
        # show_img(image_copy)

    return rows

#   ===对单行的图片进行按列切割，获得标注信息=====================
def img2cols(bound_thresh):
    """
     按列求和，竖向切割
    """
    bound_thresh_b = bound_thresh.copy()
    bound_thresh_b[bound_thresh_b == 255] = 1
    column_sums = np.sum(bound_thresh_b, axis=0)
    img_h,img_w = bound_thresh.shape[0:2]
    min_h = int(0.05*img_h) # 最小高度
    min_w = 3 # 最小宽度
    cols = []
    is_satrt = False  # 是否开始
    col_len = len(column_sums)
    for i, col_v in enumerate(column_sums):
        if not is_satrt and col_v > min_h:  # 没开始&有数据
            is_satrt = True
            col = {}
            col["start"] = i
        if is_satrt and (col_v < min_h or i+1 >= col_len):  # 已开始&（没数据|结束）
            is_satrt = False
            col["end"] = i
            # 太窄不记录
            if (col["end"] - col["start"]) > min_w:
                cols.append(col)

    if is_debug:
        image_copy = bound_thresh.copy()
        for i, col in enumerate(cols):
            left, top, right, bottom = col["start"], 0, col["end"], img_h
            cv2.rectangle(image_copy, (left, top), (right, bottom),  (255, 255, 255), 2)
        # show_img(image_copy)

    char_imgs = []
    for i, col in enumerate(cols):
        left, top, right, bottom = col["start"], 0, col["end"], img_h
        col_img = bound_thresh[top:bottom, left:right]
        # show_img(col_img)
        r_img = regular_size(col_img)
        # show_img(r_img)
        char_imgs.append(r_img)

    return char_imgs

#  对拆分的单个字符进行细化处理，裁剪成标准固定大小
def regular_size(binary_img, SIZE=28):
    # 边框法切分字符
    if np.sum(binary_img) > 0:
        x, y, w, h = cv2.boundingRect(binary_img)
        (img_h, img_w) = binary_img.shape[:2]
        left = max(0, x-1)
        top = max(0, y-1)
        right = min(img_w, x+w+1)
        bottom = min(img_h, y+h+1)
        bn_new = binary_img[top:bottom, left:right]
    else:
        bn_new = binary_img
        
    # 字符尺寸缩放至固定大小
    scale = min(SIZE/w, SIZE/h)
    random_s = random.uniform(0.55, 0.90)
    new_w = int(w*scale*random_s)
    new_h = int(h*scale*random_s)
    resized_img = cv2.resize(bn_new, (new_w, new_h))
    background = np.zeros((SIZE, SIZE), dtype=np.uint8)
    start_x = (SIZE - new_w) // 2
    start_y = (SIZE - new_h) // 2
    background[start_y:start_y+new_h, start_x:start_x+new_w] = resized_img

    return background