import sys
import os

# 获取项目根目录
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

from indicate.ind import generateInd

from Informer.train_DWT_informer import train_DWT_informer
from Informer.train_informer import train_informer
from GRU.train_gru import train_gru
from LSTM.train_lstm import train_lstm

from Informer.predict_DWT_informer import predict_DWT_informer
from Informer.predict_informer import predict_informer
from GRU.predict_gru import predict_gru
from LSTM.predict_lstm import predict_lstm

train_map = {
    'DWT-Informer': train_DWT_informer,
    'Informer': train_informer,
    'GRU': train_gru,
    'LSTM': train_lstm,
}

predict_map = {
    'DWT-Informer': predict_DWT_informer,
    'Informer': predict_informer,
    'GRU': predict_gru,
    'LSTM': predict_lstm,
}


def getModelType(dir_name):
    if dir_name.endswith('DWT'):
        return 'DWT-Informer'
    elif dir_name.endswith('lstm'):
        return 'LSTM'
    elif dir_name.endswith('gru'):
        return 'GRU'
    else:
        return 'Informer'


class Runner:
    def __init__(self):
        self.model = ''
        self.model_config = None
        self.file_info = None
        self.output = None
        self.draw_config = None
        self.data = None
        self.pred_len = 1

    def loadTrainParams(self, params):
        self.model = params['model']
        self.model_config = params['model_config']
        self.file_info = params['file_info']
        self.data = params['data']

    def loadPredictParams(self, params):
        self.model = params['model']
        self.file_info = params['file_info']
        self.output = params['output']
        self.draw_config = params['draw_config']
        self.data = params['data']
        self.pred_len = params['pred_len']

    def loadIndData(self, data):
        self.data = data

    def generateIndexes(self):
        return generateInd(self.data)

    def train(self):
        if self.file_info is None:
            return
        if self.model:
            config = {
                'model_config': self.model_config,
                'file_info': self.file_info,
                'data': self.data,
            }
            train_map[self.model](config)

    def predict(self):
        if self.file_info is None:
            return
        if self.model:
            # 使用 os.path.dirname 获取父目录
            parent_dir = os.path.dirname(self.model)
            # 使用 os.path.basename 获取父目录的最后一级目录名
            dir_name = os.path.basename(parent_dir)
            model_type = getModelType(dir_name)

            config = {
                'model': self.model,
                'file_info': self.file_info,
                'data': self.data,
                'output': self.output,
                'draw_config': self.draw_config,
                'pred_len': self.pred_len
            }
            predict_map[model_type](config)

