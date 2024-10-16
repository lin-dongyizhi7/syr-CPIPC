'''
from sklearn import metrics
import os
import json
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from core.data_processor import DataLoader
from core.model import Model
from keras.utils import plot_model
configs = json.load(open('config_2.json', 'r'))
print(type(configs))
print(configs)
'''
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
from keras.utils import plot_model



# 绘图展示结果test,修改
def plot_results_test(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    #plt.show()
    plt.savefig('results_test.png')
# 绘图展示结果train，修改
def plot_results_train(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    #plt.show()
    plt.savefig('results_train.png')
# 绘图展示结果full，修改
def plot_results_full(predicted_data, true_data):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.plot(predicted_data, label='Prediction')
    plt.legend()
    #plt.show()
    plt.savefig('results_full.png')


#RNN时间序列
def main():
    #读取所需参数
    configs = json.load(open('config.json', 'r'))
    if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])
    #读取数据
    data = DataLoader(
        os.path.join('data', configs['data']['filename']),
        configs['data']['train_test_split'],
        configs['data']['columns']
    )
    #创建RNN模型
    model = Model()
    mymodel = model.build_model(configs)

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
		epochs = configs['training']['epochs'],
		batch_size = configs['training']['batch_size'],
		save_dir = configs['model']['save_dir'],
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
    # plot_results_multiple(predictions_multiseq, y_test, configs['data']['sequence_length'])
    plot_results_train(predictions_pointbypoint, y_train)


    
    #展示测试效果
    '''
    #predictions_multiseq = model.predict_sequences_multiple(x_test, configs['data']['sequence_length'], configs['data']['sequence_length'])
    predictions_pointbypoint = model.predict_point_by_point(x_test,debug=True)        
    print(len(predictions_pointbypoint))
    print(len(y_test))
    print(y_test[:,0])
    MSE = metrics.mean_squared_error(y_test[:,0], predictions_pointbypoint)
    MAE = metrics.mean_absolute_error(y_test[:,0], predictions_pointbypoint)
    print('MSE_test',MSE)
    print('MAE_test', MAE)
    #plot_results_multiple(predictions_multiseq, y_test, configs['data']['sequence_length'])
    plot_results_train(predictions_pointbypoint, y_test)
    '''



if __name__ == '__main__':
    main()
'''
def plot_results_multiple(predicted_data, true_data, prediction_len):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot(true_data, label='True Data')
    plt.legend()
    for i, data in enumerate(predicted_data):
        padding = [None for p in range(i * prediction_len)]
        plt.plot(padding + data, label='Prediction')
    #plt.show()
    plt.savefig('results_multiple_2.png')
    '''
