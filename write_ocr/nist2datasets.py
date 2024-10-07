# %%

from debug_tool import show_img
from image_tools import regular_size
import cv2
import os
import shutil
from random import sample
import random

# nist数据集转为黑底白字图片
def nist2img(img_path):
    # img_path = "datasets2/4a/4A_00000.png"
    image = cv2.imread(img_path)
    # show_img(image,  is_gray=False)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh2 = cv2.bitwise_not(thresh)
    # show_img(thresh2)
    x, y, img_w, img_h = cv2.boundingRect(thresh2)  # 找边框
    left, top, right, bottom = x, y, x+img_w, y+img_h
    bound_thresh = thresh2[top:bottom, left:right]
    # show_img(bound_thresh)
    bound = regular_size(bound_thresh)
    # show_img(bound)
    return bound

# %% 
print("start")
origin_dataset_dir = "/Users/mac/Desktop/by_class"
dataset_dir = "datasets/char_train"
for class_dir in os.listdir(origin_dataset_dir):
    class_path = os.path.join(origin_dataset_dir, class_dir+f"/train_{class_dir}")
    if not os.path.isdir(class_path):
        continue
    print(class_path)
    new_class_dir = os.path.join(dataset_dir, class_dir)
    if not os.path.exists(new_class_dir):
        os.makedirs(new_class_dir)
    all_images = os.listdir(class_path)
    random.shuffle(all_images)
    cNum = 0
    for img_name in all_images:
        img_path = os.path.join(class_path, img_name)
        if not img_name.endswith(".png"):
            continue
        try:
            new_image = nist2img(img_path)
            save_img_path = os.path.join(new_class_dir, img_name)
            cv2.imwrite(save_img_path, new_image)
        except:
            print("处理图片错误")
        cNum = cNum + 1
        if cNum >= 3500:
            break

    print(class_path+"->"+new_class_dir)
    # break
# %%
train_dataset_dir = 'datasets/char_train'
valid_dataset_dir = 'datasets/char_valid'
validation_ratio = 0.15

if not os.path.exists(valid_dataset_dir):
    os.makedirs(valid_dataset_dir)

if not os.path.exists(train_dataset_dir):
    os.makedirs(train_dataset_dir)

for class_dir in os.listdir(train_dataset_dir):
    if not os.path.isdir(os.path.join(train_dataset_dir, class_dir)):
        continue

    valid_class_dir = os.path.join(valid_dataset_dir, class_dir)
    if not os.path.exists(valid_class_dir):
        os.makedirs(valid_class_dir)

    all_images = os.listdir(os.path.join(train_dataset_dir, class_dir))
    num_validation = int(len(all_images) * validation_ratio)
    validation_images = sample(all_images, num_validation)
    for image in validation_images:
        src_path = os.path.join(train_dataset_dir, class_dir, image)
        dst_path = os.path.join(valid_class_dir, image)
        shutil.move(src_path, dst_path)
print('Validation data has been split from the training data.')
# %%
