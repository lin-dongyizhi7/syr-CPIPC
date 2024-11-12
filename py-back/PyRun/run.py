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

from Informer.test_DWT_informer import test_DWT_informer
from Informer.test_informer import test_informer
from GRU.test_gru import test_gru
from LSTM.test_lstm import test_lstm

train_map = {
    'DWT-Informer': train_DWT_informer,
    'Informer': train_informer,
    'GRU-Informer': train_gru,
    'LSTM-Informer': train_lstm,
}

test_map = {
    'DWT-Informer': test_DWT_informer,
    'Informer': test_informer,
    'GRU-Informer': test_gru,
    'LSTM-Informer': test_lstm,
}

class Runner:
    def __init__(self):
        self.model = ''
        self.model_config = None
        self.file_info = None
        self.output = None
        self.draw_config = None
        self.data = None

    def loadTrainParams(self, params):
        self.model = params['model']
        self.model_config = params['model_config']
        self.file_info = params['file_info']
        self.data = params['data']

    def loadPredictParams(self, params):
        self.model = params['model']
        self.model_config = params['model_config']
        self.file_info = params['file_info']
        self.output = params['output']
        self.draw_config = params['draw_config']
        self.data = params['data']

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
            config = {
                'model_config': self.model_config,
                'file_info': self.file_info,
                'data': self.data,
                'output': self.output,
                'draw_config': self.draw_config,
            }
            test_map[self.model](config)
