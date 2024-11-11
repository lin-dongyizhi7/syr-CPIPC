import random
import tensorflow as tf
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

from core.data_processor import DataLoader
from core.model import Model

def seed_tensorflow(seed=415):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

seed_tensorflow(415)

def test_lstm(config):
    return