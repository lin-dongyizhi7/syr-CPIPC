import random
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from sklearn import metrics
import json
import time
import math
import matplotlib.pyplot as plt

import sys
import os

# 获取项目根目录
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

# 获取项目根目录
root = os.getenv('PROJECT_ROOT')

from core.data_processor import DataLoader
from core.model import Model

def seed_tensorflow(seed=415):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

seed_tensorflow(415)

def test_lstm(config):
    # 指定模型文件路径
    model_path = config['model']
    # 加载模型
    model = load_model(model_path)
    # 打印模型摘要
    model.summary()
    return