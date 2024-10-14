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
import json
import datetime as dt
from core.data_processor import DataLoader
from core.utils import Timer
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping
from keras_tuner import HyperModel
from keras_tuner.tuners import RandomSearch
from keras_tuner.tuners import GridSearch
from keras_tuner import HyperParameters

params_list = [ {"u1":32,"u2":64,"u3":32},
                {"u1":32,"u2":128,"u3":32},
                {"u1":64,"u2":128,"u3":64},
                {"u1":32,"u2":32},
                {"u1":64,"u2":64},
                {"u1":32,"u2":64,"u3":128,"u4":64,"u5":32},
            ]


class MyHyperModel_2(HyperModel):

    # 这里是个摆设
    def __init__(self):
        self.name = 'MyHyperModel'

    def build(self, hp):
        # configs = json.load(open('config_2.json', 'r'))
        model = tf.keras.models.Sequential()
        timer = Timer()
        timer.start()

        two_i = hp.Choice('params_index_two',values=[3,4])

        params = params_list[two_i]

        model.add(tf.keras.layers.LSTM(params["u1"], input_shape=(20, 10), return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.05))
        model.add(tf.keras.layers.LSTM(params["u2"], input_shape=(20, 10), return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.05))
        model.add(tf.keras.layers.Dense(1, activation='gelu'))

        model.compile(keras.optimizers.Adam(1e-4),loss=configs['model']['loss'])

        print('[Model] Model Compiled')

        timer.stop()
        return model

class MyHyperModel_3(HyperModel):

    # 这里是个摆设
    def __init__(self):
        self.name = 'MyHyperModel'

    def build(self, hp):
        # configs = json.load(open('config_2.json', 'r'))
        model = tf.keras.models.Sequential()
        timer = Timer()
        timer.start()

        three_i = hp.Choice('params_index_three',values=[0,1,2])

        params = params_list[three_i]

        model.add(tf.keras.layers.LSTM(params["u1"], input_shape=(20, 10), return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.05))
        model.add(tf.keras.layers.LSTM(params["u2"], input_shape=(20, 10), return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.05))
        model.add(tf.keras.layers.LSTM(params["u3"], input_shape=(20, 10), return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.05))
        model.add(tf.keras.layers.Dense(1, activation='gelu'))

        model.compile(keras.optimizers.Adam(1e-4),loss=configs['model']['loss'])

        print('[Model] Model Compiled')

        timer.stop()
        return model

class MyHyperModel_5(HyperModel):

    # 这里是个摆设
    def __init__(self):
        self.name = 'MyHyperModel'

    def build(self, hp):
        # configs = json.load(open('config_2.json', 'r'))
        model = tf.keras.models.Sequential()
        timer = Timer()
        timer.start()
        
        params = params_list[5]

        model.add(tf.keras.layers.LSTM(params["u1"], input_shape=(20, 10), return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.05))
        model.add(tf.keras.layers.LSTM(params["u2"], input_shape=(20, 10), return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.05))
        model.add(tf.keras.layers.LSTM(params["u3"], input_shape=(20, 10), return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.05))
        model.add(tf.keras.layers.LSTM(params["u4"], input_shape=(20, 10), return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.05))
        model.add(tf.keras.layers.LSTM(params["u5"], input_shape=(20, 10), return_sequences=True))
        model.add(tf.keras.layers.Dropout(0.05))
        model.add(tf.keras.layers.Dense(1, activation='gelu'))

        model.compile(keras.optimizers.Adam(1e-4),loss=configs['model']['loss'])

        print('[Model] Model Compiled')

        timer.stop()
        return model



es = EarlyStopping(monitor='val_loss', patience=6)

#读取所需参数
configs = json.load(open('config_2.json', 'r'))
if not os.path.exists(configs['model']['save_dir']): os.makedirs(configs['model']['save_dir'])
    #读取数据
data = DataLoader(
    os.path.join('data', configs['data']['filename']),
    configs['data']['train_test_split'],
    configs['data']['columns']
)

x, y = data.get_train_data(
            seq_len=configs['data']['sequence_length'],
            normalise=configs['data']['normalise']
        )

length = x.shape[0]
val_split = int(-0.1765 * length)
val_x = x[val_split:]
val_y = y[val_split:]

def try_2():
    hyperModel = MyHyperModel_2()

    hp = HyperParameters()

    tuner_2 = GridSearch(
        hyperModel,
        objective='val_loss',
        max_trials=60,
        seed=415,
        hyperparameters=hp,
        project_name='p_list2_lstm',
        # directory="/"
    )

    tuner_2.search(x, y,
             epochs=16,callbacks=[es],
             validation_data=(val_x, val_y))

def try_3():
    hyperModel = MyHyperModel_3()

    hp = HyperParameters()

    tuner_3 = GridSearch(
        hyperModel,
        objective='val_loss',
        max_trials=60,
        seed=415,
        hyperparameters=hp,
        project_name='p_list3_lstm',
        # directory="\\"
    )

    tuner_3.search(x, y,
             epochs=16,callbacks=[es],
             validation_data=(val_x, val_y))

def try_5():
    hyperModel = MyHyperModel_5()

    hp = HyperParameters()

    tuner_5 = GridSearch(
        hyperModel,
        objective='val_loss',
        max_trials=60,
        seed=415,
        hyperparameters=hp,
        project_name='p_list5_lstm',
        # directory="\\"
    )

    tuner_5.search(x, y,
             epochs=16,callbacks=[es],
             validation_data=(val_x, val_y))
    
try_2()
try_3()
try_5()