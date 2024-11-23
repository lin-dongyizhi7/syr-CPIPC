'''
Description: Systemic Financial Crises
version: 1.0
Author: YZP & SYR
Email: yys220124@outlook.com
Tip: Competition code support only, please contact the author
'''
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

# 绘图展示结果train，修改
def plot_results_train(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    #plt.show()
    plt.savefig('results_train.png')



#RNN时间序列
def train_gru(params):
    # 读取所需参数
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建 params.json 文件的完整路径
    config_path = os.path.join(current_dir, 'config.json')
    configs = json.load(open(config_path, 'r'))
    if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])
    #读取数据
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
    configs['model']['layers'][0]['input_dim'] = len(data.in_cols)
    #创建RNN模型
    model = Model()
    mymodel = model.build_model(configs)
    # print(mymodel.summary())
    # plot_model(mymodel, to_file='model.png',show_shapes=True)

    #加载训练数据
    x, y = data.get_full_data(
        seq_len=configs['data']['sequence_length'],
        normalise=configs['data']['normalise']
    )
    #print (x.shape)
    #print (y.shape)
    
	#训练模型
    model.train(
		x,
		y,
        epochs=params['model_config']['totalEpoch'],
        batch_size=params['model_config']['batchSize'],
        save_dir=os.path.normpath(f"{root}/models/{params['file_info']['name']}-gru"),
        validation_split =configs['model']["validation_split"]#修改
	)
   #训练结果
    x_train, y_train = data.get_full_data(#修改+
        seq_len=configs['data']['sequence_length'],
        normalise=configs['data']['normalise']
    )
    # 展示拟合结果,修改+
    predictions_pointbypoint = model.predict_point_by_point(x_train, debug=True)
    # print(len(predictions_pointbypoint))
    # print(len(y_train))
    # print(y_train[:, 0])
    MSE = metrics.mean_squared_error(y_train[:, 0], predictions_pointbypoint)
    MAE = metrics.mean_absolute_error(y_train[:, 0], predictions_pointbypoint)
    print('train_MSE', MSE)
    print('train_MAE', MAE)

    # plot_results_train(predictions_pointbypoint, y_train)

    # 测试结果
    x_test, y_test = data.get_test_data(
        seq_len=configs['data']['sequence_length'],
        normalise=configs['data']['normalise']
    )
    predictions_pointbypoint = model.predict_point_by_point(x_test, debug=False)
    MSE = metrics.mean_squared_error(y_test[:, 0], predictions_pointbypoint)
    MAE = metrics.mean_absolute_error(y_test[:, 0], predictions_pointbypoint)
    print('MSE_test', MSE)
    print('MAE_test', MAE)

