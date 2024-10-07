"""
fastapi接口管理
"""
import cv2
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from file_tool import make_dir, new_fname, base2file
from setting import UPLOADS, WEB, CHAR_WRITE, sep_join
from ocr_char_saved import ocr_saved
from ocr_char_tflite import ocr_lite
from char_model import img_height, img_width, class_names
import numpy as np
from loguru import logger
from debug_tool import show_img
from image_tools import img_pre, img2rows, img2cols

make_dir(UPLOADS)



app = FastAPI(title='手写识别接口', description='', docs_url="/docs", version="v1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount('/web', StaticFiles(directory=WEB), 'web')
app.mount('/uploads', StaticFiles(directory=UPLOADS), 'uploads')

class ImageData(BaseModel):
    image_data: str
    id: str

@app.post('/write_char', tags=[''], summary="手写单个字符OCR识别")
async def write_char(image_data: ImageData):
    try:
        img = base2file(image_data.image_data)
        img_resized = cv2.resize(img, (img_width, img_height))
        if np.sum(img_resized) < 255*20:
            return {"code": 201, "data": "", "msg": "笔画不足"}
        if image_data.id == "lite":
            result = ocr_lite.predict(img_resized)
        else:
            result = ocr_saved.predict(img_resized)
            if result == "":
                return {"code": 201, "data": "", "msg": "加载模型失败"}
        return {"code": 200, "data": result, "msg": ""}
    except Exception as e:
        logger.opt(exception=e).error('识别失败')
        return {"code": 500, "data": "", "msg": f"处理失败"}

@app.post('/write_char_save', tags=[''], summary="手写字符保存")
async def write_char_save(image_data: ImageData):
    try:
        img = base2file(image_data.image_data)
        img_resized = cv2.resize(img, (img_width, img_height))
        if np.sum(img_resized) < 255*20:
            return {"code": 201, "data": "", "msg": "笔画不足"}
        img_id = image_data.id
        save_dir = sep_join([CHAR_WRITE, f"{img_id}"])
        make_dir(save_dir)
        new_path = sep_join([save_dir, new_fname(suf=".png")])
        cv2.imwrite(new_path, img_resized)
        return {"code": 200, "data": "保存成功", "msg": ""}
    except Exception as e:
        print(e)
        return {"code": 500, "data": "", "msg": "处理失败"}

@app.post('/write_string', tags=[''], summary="手写多个字符OCR识别")
async def write_string(image_data: ImageData):
    try:
        img = base2file(image_data.image_data)
        img_id = image_data.id
        save_dir = sep_join([CHAR_WRITE, f"{img_id}"])
        make_dir(save_dir)
        new_path = sep_join([save_dir, new_fname(suf=".png")])
        cv2.imwrite(new_path, img)

        image = cv2.imread(new_path)
        bound_thresh = img_pre(image) # 预处理
        img_h,img_w = bound_thresh.shape[0:2]
        rows = img2rows(bound_thresh) # 切行
        results = []
        # 对每一行进行处理
        for i, row in enumerate(rows):
            left, top, right, bottom = 0, row["start"], img_w, row["end"]
            row_img = bound_thresh[top:bottom, left:right] # 其中一行
            # show_img(row_img)
            char_imgs = img2cols(row_img) # 行切列
            if img_id == "lite":
                result = ocr_lite.predicts(char_imgs)
            else:
                result = ocr_saved.predicts(char_imgs)
            if result == []:
                return {"code": 201, "data": "", "msg": "加载模型失败"}
            results.append(result)
        # print(type(results),results)
        return {"code": 200, "data": results, "msg": ""}
    except Exception as e:
        print(e)
        return {"code": 500, "data": "", "msg": "处理失败"}
    
if __name__ == '__main__':
    uvicorn.run("api:app", host="0.0.0.0", port=9001)