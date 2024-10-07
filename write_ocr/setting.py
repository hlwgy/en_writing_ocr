"""
配置文件
"""
import os

PROJ_DIR = str(os.path.dirname(os.path.abspath(__file__)))

def sep_join(names):
    return (os.sep).join(names)

# 训练集数据集目录
TRAIN_PATH = sep_join([PROJ_DIR,"datasets", "char_train"]) 
# 验证集数据集目录
VALID_PATH = sep_join([PROJ_DIR,"datasets", "char_valid"]) 
# 手写图片存储目录
CHAR_WRITE = sep_join([PROJ_DIR,"datasets", "write"]) 
# 模型文件存储目录
CHAR_CKPT = sep_join([PROJ_DIR,"models", "char_checkpoint", "char.ckpt"])
# 模型文件存储目录
CHAR_MODEL = sep_join([PROJ_DIR,"models", "char"])
# 用户上传目录
UPLOADS = sep_join([PROJ_DIR, "uploads"]) 
# 网页目录
WEB = sep_join([PROJ_DIR,"web"])