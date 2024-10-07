import os
import time
import random
import string
import base64
import numpy as np
import cv2
import shutil

def base2file(image_data, mode = cv2.IMREAD_GRAYSCALE):
    base64_data = image_data.split(',')[1]
    decoded_data = base64.b64decode(base64_data)
    nparr = np.frombuffer(decoded_data, np.uint8)
    img = cv2.imdecode(nparr, mode)
    return img

def make_dir(filepath, clear=False):
    if clear and os.path.exists(filepath):
        shutil.rmtree(filepath, ignore_errors=True)
    if not os.path.exists(filepath):
        os.makedirs(filepath)

def new_fname(suf=""):
    rd_char = random.choice(string.ascii_lowercase)
    return f"{int(time.time()*1000000)}{rd_char}{suf}"