"""
字符训练，结果采用三种方式保存：checkpoint、saved_model、tflite
代码来源
https://tensorflow.google.cn/tutorials/images/classification?hl=zh-cn
"""
# %%
import tensorflow as tf
import numpy as np
import os
from debug_tool import show_history
from char_model import create_model, img_height, img_width
from setting import TRAIN_PATH, CHAR_CKPT, VALID_PATH, CHAR_MODEL, sep_join
# %% 训练数据
def train():
    batch_size = 128
    epochs = 100

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        TRAIN_PATH,
        seed=123, color_mode="grayscale",
        image_size=(img_height, img_width),
        batch_size=batch_size
    )

    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        VALID_PATH,
        seed=123, color_mode="grayscale",
        image_size=(img_height, img_width),
        batch_size=batch_size
    )

    AUTOTUNE = tf.data.experimental.AUTOTUNE
    train_ds = train_ds.cache().shuffle(10000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    model = create_model()
    if os.path.exists(CHAR_CKPT + '.index'):
        print('load the model:', CHAR_CKPT)
        model.load_weights(CHAR_CKPT)

    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=CHAR_CKPT,
                                                     save_weights_only=True,
                                                     save_best_only=True)
    # 训练模型
    history = model.fit(train_ds, validation_data=val_ds, epochs=epochs, callbacks=[cp_callback])
    print("save model path:", CHAR_CKPT)
    model.save(CHAR_MODEL)
    # 将模型转换为 TensorFlow Lite 格式
    converter = tf.lite.TFLiteConverter.from_saved_model(CHAR_MODEL)
    tflite_model = converter.convert()
    tflite_path = sep_join([CHAR_MODEL, 'char.tflite'])
    with open(tflite_path, 'wb') as f:
        f.write(tflite_model)
    print("save tflite model path:", tflite_path)
    show_history(history, epochs)
# %%
if __name__ == '__main__':
    train()