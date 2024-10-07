"""
模型结构
代码来源
https://tensorflow.google.cn/tutorials/images/classification?hl=zh-cn
"""
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

# 定义标签列表
class_names = ['30', '31', '32', '33', '34', '35', '36', '37', '38', '39',  # 0-9
               '41', '42', '43', '44', '45', '46', '47', '48', '49', '4a',  # A-J
               '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54',  # K-T
               '55', '56', '57', '58', '59', '5a',                         # U-Z
               '61', '62', '63', '64', '65', '66', '67', '68', '69', '6a',  # a-j
               '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74',  # k-t
               '75', '76', '77', '78', '79', '7a']                         # u-z

hex_to_char = [chr(int(h, 16)) for h in class_names]

img_width = 28
img_height = 28

def create_model():

    num_classes = len(class_names)
    model = Sequential([
        layers.Rescaling(1./255, input_shape=(img_height, img_width, 1)),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Dropout(0.1),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(num_classes)
    ])

    model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
    
    return model