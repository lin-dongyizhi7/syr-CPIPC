import sys
sys.path.append("../")
from utils.tools import dotdict
from exp.exp_informer import Exp_Informer
import torch
import numpy as np
import random
import os
import pandas as pd
def setup_seed(seed):
   torch.manual_seed(seed)
   os.environ['PYTHONHASHSEED'] = str(seed)
   torch.cuda.manual_seed(seed)
   torch.cuda.manual_seed_all(seed)
   np.random.seed(seed)
   random.seed(seed)
   torch.backends.cudnn.benchmark = False
   torch.backends.cudnn.deterministic = True
   torch.backends.cudnn.enabled = True
setup_seed(415)

args = dotdict()

args.model = 'informer' # model of experiment, options: [informer, informerstack, informerlight(TBD)]

args.des0 = 'test'
args.des1 = 'protr'
args.des2 = 'prov'
args.des3 = 'prote'
args.des4 = 'prof'

#args.data = 'DWT13-20-1' # data
args.root_path = './data/' # root path of data file
args.data_path = 'DWT13-20-1.csv' # data file=-09
args.features = 'MS' # forecasting task, options:[M, S, MS]; M:multivariate predict multivariate, S:univariate predict univariate, MS:multivariate predict univariate
args.target = 'ind' # target feature in S or MS task
args.freq = 'd' # freq for time features encoding, options:[s:secondly, t:minutely, h:hourly, d:daily, b:business days, w:weekly, m:monthly], you can also use more detailed freq like 15min or 3h
args.checkpoints = './checkpoints/' # location of model checkpoints

args.seq_len = 20 # input sequence length of Informer encoder
args.label_len = 15 # start token length of Informer decoder
args.pred_len = 1 # prediction sequence length
# Informer decoder input: concat[start token series(label_len), zero padding series(pred_len)]

args.enc_in = 7 # encoder input size
args.dec_in = 7 # decoder input size
args.c_out = 7 # output size
args.factor = 5 # probsparse attn factor

args.d_layers = 2
args.s_layers = "3,2,1"

args.dropout = 0.05 # dropout
args.attn = 'prob' # attention used in encoder, options:[prob, full]
args.embed = 'timeF' # time features encoding, options:[timeF, fixed, learned]
args.activation = 'gelu' # activation
# args.distil = True # whether to use distilling in encoder  //model-20
args.distil = False # whether to use distilling in encoder
args.output_attention = False # whether to output attention in ecoder
args.mix = True
args.padding = 0

args.batch_size = 32
args.learning_rate = 0.0001 #原来是0.0001
args.loss = 'mse'
args.lradj = 'type1'
args.use_amp = False # whether to use automatic mixed precision training

args.num_workers = 0
args.itr = 2
args.train_epochs = 16
args.patience = 6
args.des = 'exp'
args.d_ff = 2048  # dimension of fcn in model
args.d_model = 512  # dimension of model

args.n_heads = 16
args.e_layers =2

args.use_gpu = True if torch.cuda.is_available() else False
args.gpu = 0
args.itr = 2
args.use_multi_gpu = False
args.devices = '0,1,2,3'

data_parser = {
    'ETTh1':{'data':'ETTh1.csv','T':'OT','M':[7,7,7],'S':[1,1,1],'MS':[7,7,1]},
    'ETTh2':{'data':'ETTh2.csv','T':'OT','M':[7,7,7],'S':[1,1,1],'MS':[7,7,1]},
    'ETTm1':{'data':'ETTm1.csv','T':'OT','M':[7,7,7],'S':[1,1,1],'MS':[7,7,1]},
    'ETTm2':{'data':'ETTm2.csv','T':'OT','M':[7,7,7],'S':[1,1,1],'MS':[7,7,1]},
    'WTH':{'data':'WTH.csv','T':'WetBulbCelsius','M':[12,12,12],'S':[1,1,1],'MS':[12,12,1]},
    'ECL':{'data':'ECL.csv','T':'MT_320','M':[321,321,321],'S':[1,1,1],'MS':[321,321,1]},
    'Solar':{'data':'solar_AL.csv','T':'POWER_136','M':[137,137,137],'S':[1,1,1],'MS':[137,137,1]},
    'DWT4':{'data':'DWT4.csv','T':'ind','M':[10,10,10],'S':[1,1,1],'MS':[10,10,1]},
    'DWT1':{'data':'DWT1.csv','T':'ind','M':[10,10,10],'S':[1,1,1],'MS':[10,10,1]},
    'In0':{'data':'In0.csv','T':'ind','M':[10,10,10],'S':[1,1,1],'MS':[10,10,1]},
    'DWTall':{'data':'DWTall.csv','T':'ind','M':[10,10,10],'S':[1,1,1],'MS':[10,10,1]},
    'DWTt':{'data':'DWTall.csv','T':'ind','M':[10,10,10],'S':[1,1,1],'MS':[10,10,1]},
    'DWTlongin':{'data':'DWTlongin.csv','T':'ind','M':[10,10,10],'S':[1,1,1],'MS':[10,10,1]},
    'DWT15':{'data':'DWT15.csv','T':'ind','M':[10,10,10],'S':[1,1,1],'MS':[10,10,1]},
    'All_model15_s':{'data':'All_model15_s.csv','T':'ind','M':[10,10,10],'S':[1,1,1],'MS':[10,10,1]},
    'ind13-20-day': {'data': 'ind13-20-day.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20-1': {'data': 'DWT13-20-1.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20': {'data': 'DWT13-20.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_1_1':{'data': 'DWT13-20_shuffled_C_1_1.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_1_2':{'data': 'DWT13-20_shuffled_C_1_2.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_1_3':{'data': 'DWT13-20_shuffled_C_1_3.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_1_4':{'data': 'DWT13-20_shuffled_C_1_4.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_1_5':{'data': 'DWT13-20_shuffled_C_1_5.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_1_6':{'data': 'DWT13-20_shuffled_C_1_6.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_1_7':{'data': 'DWT13-20_shuffled_C_1_7.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_1_8':{'data': 'DWT13-20_shuffled_C_1_8.csv', 'T': 'ind','M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_1_9':{'data': 'DWT13-20_shuffled_C_1_9.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_1_10': {'data': 'DWT13-20_shuffled_C_1_10.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_2_1':{'data': 'DWT13-20_shuffled_C_2_1.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_2_2':{'data': 'DWT13-20_shuffled_C_2_2.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_2_3':{'data': 'DWT13-20_shuffled_C_2_3.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_2_4':{'data': 'DWT13-20_shuffled_C_2_4.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_2_5':{'data': 'DWT13-20_shuffled_C_2_5.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_2_6':{'data': 'DWT13-20_shuffled_C_2_6.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_2_7':{'data': 'DWT13-20_shuffled_C_2_7.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_2_8':{'data': 'DWT13-20_shuffled_C_2_8.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_2_9':{'data': 'DWT13-20_shuffled_C_2_9.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_2_10':{'data': 'DWT13-20_shuffled_C_2_10.csv', 'T': 'ind','M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_3_1':{'data': 'DWT13-20_shuffled_C_3_1.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_3_2':{'data': 'DWT13-20_shuffled_C_3_2.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_3_3':{'data': 'DWT13-20_shuffled_C_3_3.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_3_4':{'data': 'DWT13-20_shuffled_C_3_4.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_3_5':{'data': 'DWT13-20_shuffled_C_3_5.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_3_6':{'data': 'DWT13-20_shuffled_C_3_6.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_3_7':{'data': 'DWT13-20_shuffled_C_3_7.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_3_8':{'data': 'DWT13-20_shuffled_C_3_8.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_3_9':{'data': 'DWT13-20_shuffled_C_3_9.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_C_3_10':{'data': 'DWT13-20_shuffled_C_3_10.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_1_1':{'data': 'DWT13-20_shuffled_D_1_1.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_1_2':{'data': 'DWT13-20_shuffled_D_1_2.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_1_3':{'data': 'DWT13-20_shuffled_D_1_3.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_1_4':{'data': 'DWT13-20_shuffled_D_1_4.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_1_5':{'data': 'DWT13-20_shuffled_D_1_5.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_1_6':{'data': 'DWT13-20_shuffled_D_1_6.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_1_7':{'data': 'DWT13-20_shuffled_D_1_7.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_1_8':{'data': 'DWT13-20_shuffled_D_1_8.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_1_9':{'data': 'DWT13-20_shuffled_D_1_9.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_1_10':{'data': 'DWT13-20_shuffled_D_1_10.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_2_1':{'data': 'DWT13-20_shuffled_D_2_1.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_2_2':{'data': 'DWT13-20_shuffled_D_2_2.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_2_3':{'data': 'DWT13-20_shuffled_D_2_3.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_2_4':{'data': 'DWT13-20_shuffled_D_2_4.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_2_5':{'data': 'DWT13-20_shuffled_D_2_5.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_2_6':{'data': 'DWT13-20_shuffled_D_2_6.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_2_7':{'data': 'DWT13-20_shuffled_D_2_7.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_2_8':{'data': 'DWT13-20_shuffled_D_2_8.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_2_9':{'data': 'DWT13-20_shuffled_D_2_9.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_D_2_10':{'data': 'DWT13-20_shuffled_D_2_10.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_1_1':{'data': 'DWT13-20_shuffled_E_1_1.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_1_2':{'data': 'DWT13-20_shuffled_E_1_2.csv', 'T': 'ind','M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_1_3':{'data': 'DWT13-20_shuffled_E_1_3.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_1_4':{'data': 'DWT13-20_shuffled_E_1_4.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_1_5':{'data': 'DWT13-20_shuffled_E_1_5.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_1_6':{'data': 'DWT13-20_shuffled_E_1_6.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_1_7':{'data': 'DWT13-20_shuffled_E_1_7.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_1_8':{'data': 'DWT13-20_shuffled_E_1_8.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_1_9':{'data': 'DWT13-20_shuffled_E_1_9.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_1_10':{'data': 'DWT13-20_shuffled_E_1_10.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_2_1':{'data': 'DWT13-20_shuffled_E_2_1.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_2_2':{'data': 'DWT13-20_shuffled_E_2_2.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_2_3':{'data': 'DWT13-20_shuffled_E_2_3.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_2_4':{'data': 'DWT13-20_shuffled_E_2_4.csv', 'T': 'ind','M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_2_5':{'data': 'DWT13-20_shuffled_E_2_5.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_2_6':{'data': 'DWT13-20_shuffled_E_2_6.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_2_7':{'data': 'DWT13-20_shuffled_E_2_7.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_2_8':{'data': 'DWT13-20_shuffled_E_2_8.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_2_9':{'data': 'DWT13-20_shuffled_E_2_9.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_2_10':{'data': 'DWT13-20_shuffled_E_2_10.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_3_1':{'data': 'DWT13-20_shuffled_E_3_1.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_3_2':{'data': 'DWT13-20_shuffled_E_3_2.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_3_3':{'data': 'DWT13-20_shuffled_E_3_3.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_3_4':{'data': 'DWT13-20_shuffled_E_3_4.csv', 'T': 'ind','M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_3_5':{'data': 'DWT13-20_shuffled_E_3_5.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_3_6':{'data': 'DWT13-20_shuffled_E_3_6.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_3_7':{'data': 'DWT13-20_shuffled_E_3_7.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_3_8':{'data': 'DWT13-20_shuffled_E_3_8.csv', 'T': 'ind','M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_3_9':{'data': 'DWT13-20_shuffled_E_3_9.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_E_3_10':{'data': 'DWT13-20_shuffled_E_3_10.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_F_3_1':{'data': 'DWT13-20_shuffled_F_3_1.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_F_3_2':{'data': 'DWT13-20_shuffled_F_3_2.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_F_3_3':{'data': 'DWT13-20_shuffled_F_3_3.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_F_3_4':{'data': 'DWT13-20_shuffled_F_3_4.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_F_3_5':{'data': 'DWT13-20_shuffled_F_3_5.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_F_3_6':{'data': 'DWT13-20_shuffled_F_3_6.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_F_3_7':{'data': 'DWT13-20_shuffled_F_3_7.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_F_3_8':{'data': 'DWT13-20_shuffled_F_3_8.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_F_3_9':{'data': 'DWT13-20_shuffled_F_3_9.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
    'DWT13-20_shuffled_F_3_10':{'data': 'DWT13-20_shuffled_F_3_10.csv', 'T': 'ind', 'M': [10, 10, 10], 'S': [1, 1, 1], 'MS': [10, 10, 1]},
}


model_list = [
             {'data': 'DWT13-20_shuffled_C_1_1'}, 
             {'data': 'DWT13-20_shuffled_C_1_2'}, 
             {'data': 'DWT13-20_shuffled_C_1_3'}, 
             {'data': 'DWT13-20_shuffled_C_1_4'}, 
             {'data': 'DWT13-20_shuffled_C_1_5'}, 
             {'data': 'DWT13-20_shuffled_C_1_6'}, 
             {'data': 'DWT13-20_shuffled_C_1_7'}, 
             {'data': 'DWT13-20_shuffled_C_1_8'}, 
             {'data': 'DWT13-20_shuffled_C_1_9'}, 
             {'data': 'DWT13-20_shuffled_C_1_10'}, 
             {'data': 'DWT13-20_shuffled_C_2_1'}, 
             {'data': 'DWT13-20_shuffled_C_2_2'}, 
             {'data': 'DWT13-20_shuffled_C_2_3'}, 
             {'data': 'DWT13-20_shuffled_C_2_4'}, 
             {'data': 'DWT13-20_shuffled_C_2_5'}, 
             {'data': 'DWT13-20_shuffled_C_2_6'}, 
             {'data': 'DWT13-20_shuffled_C_2_7'},
             {'data': 'DWT13-20_shuffled_C_2_8'}, 
             {'data': 'DWT13-20_shuffled_C_2_9'}, 
             {'data': 'DWT13-20_shuffled_C_2_10'}, 
             {'data': 'DWT13-20_shuffled_C_3_1'}, 
             {'data': 'DWT13-20_shuffled_C_3_2'}, 
             {'data': 'DWT13-20_shuffled_C_3_3'}, 
             {'data': 'DWT13-20_shuffled_C_3_4'}, 
             {'data': 'DWT13-20_shuffled_C_3_5'}, 
             {'data': 'DWT13-20_shuffled_C_3_6'}, 
             {'data': 'DWT13-20_shuffled_C_3_7'}, 
             {'data': 'DWT13-20_shuffled_C_3_8'}, 
             {'data': 'DWT13-20_shuffled_C_3_9'}, 
             {'data': 'DWT13-20_shuffled_C_3_10'}, 
             {'data': 'DWT13-20_shuffled_D_1_1'}, 
             {'data': 'DWT13-20_shuffled_D_1_2'}, 
             {'data': 'DWT13-20_shuffled_D_1_3'}, 
             {'data': 'DWT13-20_shuffled_D_1_4'}, 
             {'data': 'DWT13-20_shuffled_D_1_5'}, 
             {'data': 'DWT13-20_shuffled_D_1_6'}, 
             {'data': 'DWT13-20_shuffled_D_1_7'}, 
             {'data': 'DWT13-20_shuffled_D_1_8'}, 
             {'data': 'DWT13-20_shuffled_D_1_9'}, 
             {'data': 'DWT13-20_shuffled_D_1_10'}, 
             {'data': 'DWT13-20_shuffled_D_2_1'}, 
             {'data': 'DWT13-20_shuffled_D_2_2'}, 
             {'data': 'DWT13-20_shuffled_D_2_3'}, 
             {'data': 'DWT13-20_shuffled_D_2_4'},
             {'data': 'DWT13-20_shuffled_D_2_5'}, 
             {'data': 'DWT13-20_shuffled_D_2_6'}, 
             {'data': 'DWT13-20_shuffled_D_2_7'}, 
             {'data': 'DWT13-20_shuffled_D_2_8'}, 
             {'data': 'DWT13-20_shuffled_D_2_9'}, 
             {'data': 'DWT13-20_shuffled_D_2_10'}, 
             {'data': 'DWT13-20_shuffled_E_1_1'}, 
             {'data': 'DWT13-20_shuffled_E_1_2'}, 
             {'data': 'DWT13-20_shuffled_E_1_3'}, 
             {'data': 'DWT13-20_shuffled_E_1_4'}, 
             {'data': 'DWT13-20_shuffled_E_1_5'}, 
             {'data': 'DWT13-20_shuffled_E_1_6'}, 
             {'data': 'DWT13-20_shuffled_E_1_7'}, 
             {'data': 'DWT13-20_shuffled_E_1_8'}, 
             {'data': 'DWT13-20_shuffled_E_1_9'}, 
             {'data': 'DWT13-20_shuffled_E_1_10'}, 
             {'data': 'DWT13-20_shuffled_E_2_1'}, 
             {'data': 'DWT13-20_shuffled_E_2_2'}, 
             {'data': 'DWT13-20_shuffled_E_2_3'}, 
             {'data': 'DWT13-20_shuffled_E_2_4'}, 
             {'data': 'DWT13-20_shuffled_E_2_5'}, 
             {'data': 'DWT13-20_shuffled_E_2_6'}, 
             {'data': 'DWT13-20_shuffled_E_2_7'}, 
             {'data': 'DWT13-20_shuffled_E_2_8'}, 
             {'data': 'DWT13-20_shuffled_E_2_9'}, 
             {'data': 'DWT13-20_shuffled_E_2_10'}, 
             {'data': 'DWT13-20_shuffled_E_3_1'}, 
             {'data': 'DWT13-20_shuffled_E_3_2'}, 
             {'data': 'DWT13-20_shuffled_E_3_3'}, 
             {'data': 'DWT13-20_shuffled_E_3_4'}, 
             {'data': 'DWT13-20_shuffled_E_3_5'}, 
             {'data': 'DWT13-20_shuffled_E_3_6'}, 
             {'data': 'DWT13-20_shuffled_E_3_7'}, 
             {'data': 'DWT13-20_shuffled_E_3_8'}, 
             {'data': 'DWT13-20_shuffled_E_3_9'}, 
             {'data': 'DWT13-20_shuffled_E_3_10'}, 
             {'data': 'DWT13-20_shuffled_F_3_1'}, 
             {'data': 'DWT13-20_shuffled_F_3_2'}, 
             {'data': 'DWT13-20_shuffled_F_3_3'}, 
             {'data': 'DWT13-20_shuffled_F_3_4'}, 
             {'data': 'DWT13-20_shuffled_F_3_5'}, 
             {'data': 'DWT13-20_shuffled_F_3_6'}, 
             {'data': 'DWT13-20_shuffled_F_3_7'}, 
             {'data': 'DWT13-20_shuffled_F_3_8'}, 
             {'data': 'DWT13-20_shuffled_F_3_9'}, 
             {'data': 'DWT13-20_shuffled_F_3_10'}
            ]



for i in range(69,len(model_list)):
    args.data = model_list[i]["data"]
    if args.data in data_parser.keys():
        data_info = data_parser[args.data]
        args.data_path = data_info['data']
        args.target = data_info['T']
        args.enc_in, args.dec_in, args.c_out = data_info[args.features]

    #args.s_layers = [int(s_l) for s_l in args.s_layers.replace(' ','').split(',')]
    #args.detail_freq = args.freq
    #args.freq = args.freq[-1:]

    print("model number:",i+1)
    print('Args in experiment:')
    print(args)

    setup_seed(415)
    Exp = Exp_Informer

    for ii in range(args.itr):
        print(ii)
    # setting record of experiments
        setting = '{}_{}_ft{}_sl{}_ll{}_pl{}_dm{}_nh{}_el{}_dl{}_df{}_at{}_fc{}_eb{}_dt{}_mx{}_{}_{}'.format(args.model, args.data, args.features,
            args.seq_len, args.label_len, args.pred_len,
            args.d_model, args.n_heads, args.e_layers, args.d_layers, args.d_ff, args.attn, args.factor,
            args.embed, args.distil, args.mix, args.des0, ii)
        settingtr = '{}_{}_ft{}_sl{}_ll{}_pl{}_dm{}_nh{}_el{}_dl{}_df{}_at{}_fc{}_eb{}_dt{}_mx{}_{}_{}'.format(args.model,args.data,args.features,
            args.seq_len, args.label_len, args.pred_len,
            args.d_model, args.n_heads, args.e_layers, args.d_layers, args.d_ff, args.attn, args.factor,
            args.embed, args.distil, args.mix, args.des1, ii)
        settingv = '{}_{}_ft{}_sl{}_ll{}_pl{}_dm{}_nh{}_el{}_dl{}_df{}_at{}_fc{}_eb{}_dt{}_mx{}_{}_{}'.format(args.model, args.data, args.features, 
            args.seq_len, args.label_len, args.pred_len, 
            args.d_model, args.n_heads, args.e_layers, args.d_layers, args.d_ff, args.attn, args.factor,
            args.embed, args.distil, args.mix, args.des2, ii)
        settingte = '{}_{}_ft{}_sl{}_ll{}_pl{}_dm{}_nh{}_el{}_dl{}_df{}_at{}_fc{}_eb{}_dt{}_mx{}_{}_{}'.format(args.model, args.data, args.features,
            args.seq_len, args.label_len, args.pred_len, 
            args.d_model, args.n_heads, args.e_layers, args.d_layers, args.d_ff, args.attn, args.factor,
            args.embed, args.distil, args.mix, args.des3, ii)
        settingf = '{}_{}_ft{}_sl{}_ll{}_pl{}_dm{}_nh{}_el{}_dl{}_df{}_at{}_fc{}_eb{}_dt{}_mx{}_{}_{}'.format(args.model, args.data, args.features,
            args.seq_len, args.label_len, args.pred_len, 
            args.d_model, args.n_heads, args.e_layers, args.d_layers, args.d_ff, args.attn, args.factor,
            args.embed, args.distil, args.mix, args.des4, ii)
        setting0 = '{}_{}_ft{}_sl{}_ll{}_pl{}_dm{}_nh{}_el{}_dl{}_df{}_at{}_fc{}_eb{}_dt{}_mx{}_{}_{}'.format(args.model, args.data, args.features,
            args.seq_len, args.label_len, args.pred_len,
            args.d_model, args.n_heads, args.e_layers, args.d_layers, args.d_ff, args.attn, args.factor,
            args.embed, args.distil, args.mix, args.des0, ii)

        exp = Exp(args)  # set experiments
        print('>>>>>>>start training : {}>>>>>>>>>>>>>>>>>>>>>>>>>>'.format(setting))
        exp.train(setting)
        if ii == 1:
            print('>>>>>>> pretesting : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(setting0))
            exp.pretest(setting0)


    # print('>>>>>>> protring : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(settingtr))
    # exp.protr(settingtr)
        print('>>>>>>> protring : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(settingtr))
        exp.protr(settingtr)
        print('>>>>>>> proving : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(settingv))
        exp.prov(settingv)
        print('>>>>>>>testing  : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(settingte))
        exp.test(settingte)
        print('>>>>>>> profing : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(settingf))
        exp.prof(settingf)

    torch.cuda.empty_cache()
