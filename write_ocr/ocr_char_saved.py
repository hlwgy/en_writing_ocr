"""
模型调用, save_model权重模式
"""
# %%
import numpy as np
from setting import  CHAR_MODEL
import tensorflow as tf
import os
from char_model import hex_to_char

class NumOCR:

    load_ok = False

    def __init__(self):
        if os.path.exists(CHAR_MODEL):
            # 普通模式加载
            self.model = tf.keras.models.load_model(CHAR_MODEL)
            print(f"Loaded Model {CHAR_MODEL}  successfully!")
            self.load_ok = True
        else:
            print(f"Model {CHAR_MODEL} not found!")
            self.load_ok = False

    def predicts(self, imgs):
        classes = []
        if len(imgs) > 0 and self.load_ok:
            imgs = np.array(imgs)
            predictions = self.model.predict(imgs)
            classes = np.argmax(predictions, axis=1)
            predicted_chars = [hex_to_char[i] for i in classes]
            return predicted_chars
        return classes
    
    def predict(self, img):
        return self.predicts([img])[0] if self.load_ok else ""
        
ocr_saved = NumOCR()