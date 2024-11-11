import random
import tensorflow as tf
import os
import numpy as np
def seed_tensorflow(seed=415):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)

seed_tensorflow(415)
from sklearn import metrics
import os
import json
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from core.data_processor import DataLoader
from core.model import Model

def test_lstm(config):
    return