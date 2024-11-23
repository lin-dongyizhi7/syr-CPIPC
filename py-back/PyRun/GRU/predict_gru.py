'''
Description: Systemic Financial Crises
version: 1.0
Author: YZP & SYR
Email: yys220124@outlook.com
Tip: Competition code support only, please contact the author
'''
import random
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from sklearn import metrics
import json
import time
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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

def predict_gru(params):
    name = params['file_info']['name']
    # 指定模型文件路径
    model_path = params['model']
    # 加载模型
    model = Model()
    # 加载模型
    model.load_model(model_path)

    # 打印模型摘要
    m = load_model(model_path)
    m.summary()

    # 读取所需参数
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 params.json 文件的完整路径
    config_path = os.path.join(current_dir, 'config.json')
    configs = json.load(open(config_path, 'r'))
    if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])
    # 读取数据
    if params['file_info']['type'] == 'path':
        data = DataLoader(
            params['file_info']['path'],
            None,
            configs['data']['train_test_split'],
        )
    else:
        data = DataLoader(
            None,
            params['data'],
            configs['data']['train_test_split'],
        )
    configs['data']['columns'] = data.in_cols
    # 加载训练数据
    x, y = data.get_test_data(
        seq_len=configs['data']['sequence_length'],
        normalise=configs['data']['normalise']
    )

    pre_len = params['pred_len']

    predictions = model.predict_sequences_multiple(x, 16, pre_len,debug=False)
    print(predictions)
    # result save
    folder_path = os.path.normpath(f'{root}/opt/{name}/results/')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 保存npy文件
    res_file = os.path.normpath(folder_path + f"/prediction_{pre_len}_gru.npy")
    np.save(res_file, predictions)
    print('save result file:' + res_file)
    # 保存绘图
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    pre_x = np.arange(1, pre_len + 1)
    ax.plot(pre_x, predictions, label='预测值')
    # 设置横轴刻度为整数
    ax.xaxis.set_major_locator(ticker.MultipleLocator(int(pre_len/8)))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
    ax.set_ylim(-1, 1)
    if pre_len <= 30:
        ax.scatter(pre_x, predictions, marker='*')
    res_picture = os.path.normpath(folder_path + f"/prediction_{pre_len}_gru.png")
    plt.savefig(res_picture)
    print('save result picture:' + res_picture)
    return True