"""
模型调用TFLITE版本
"""
# %%
import numpy as np
from setting import  sep_join, CHAR_MODEL
import tensorflow as tf
import os
from char_model import hex_to_char

class NumOCRLite:

    load_ok = False
    def __init__(self):
        lite_path = sep_join([CHAR_MODEL, "char.tflite"])
        if os.path.exists(lite_path):
            self.interpreter = tf.lite.Interpreter(model_path=lite_path)
            self.interpreter.allocate_tensors()
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            self.load_ok = True
        else:
            self.load_ok = False

    def predicts(self, images):
        """ 批量预测多张图片 """
        if self.load_ok and len(images) > 0:
            # 转换输入为 NumPy 数组并添加通道维度
            images_array = np.array([np.expand_dims(img.astype(np.float32), axis=-1) for img in images])
            # 更新 interpreter 的输入
            input_index = self.input_details[0]['index']
            self.interpreter.resize_tensor_input(input_index, [len(images), *images_array.shape[1:]])
            self.interpreter.allocate_tensors()  # 调整tensor大小后重新分配
            self.interpreter.set_tensor(input_index, images_array)
            self.interpreter.invoke()

            # 获取预测结果
            output_index = self.output_details[0]['index']
            predictions = self.interpreter.get_tensor(output_index)
            classes = np.argmax(predictions, axis=1)
            predicted_chars = [hex_to_char[i] for i in classes]
            return predicted_chars
        return []

    def predict(self, image):
        """ 单张图片预测 """
        return self.predicts([image])[0] if self.load_ok else ""
    
ocr_lite = NumOCRLite()