import os
import json
import numpy as np
import pandas as pd
from matplotlib.pyplot import MultipleLocator

def my_sort(x,y):
    tmpX = x.copy()
    tmpX.sort()
    tmpY = []
    for i in range(len(x)):
        tmpY.append(y[x.index(tmpX[i])])
    return tmpX,tmpY

# trials = []
units1_nums = []
units2_nums = []
units3_nums = []
units4_nums = []
units5_nums = []
batch_sizes = []
scores = []

params_list = [ {"u1":32,"u2":64,"u3":32},
                {"u1":32,"u2":128,"u3":32},
                {"u1":64,"u2":128,"u3":64},
                {"u1":32,"u2":32},
                {"u1":64,"u2":64},
                {"u1":32,"u2":64,"u3":128,"u4":64,"u5":32},
            ]

for layers in [2,3,5]:

    path = './p_list' + str(layers) + '_lstm/'
    files= os.listdir(path)
    name_ = 'trial_'

    l = len(files)-2

    # if(len(files[2].split('_')[1])==3):
    #     zero = '0'
    # else:
    #     zero = ''

    for i in range(l):
        f = open(path + name_ + '0' + str(i) +'/trial.json', 'r').read()
        # if i < 10:
            # f = open(path + name_ + zero + '0' + str(i) +'/trial.json', 'r').read()
        # elif i < 100:
        #     f = open(path + name_ + zero + str(i) +'/trial.json', 'r').read()
        # else:
        #     f = open(path + name_  + str(i) +'/trial.json', 'r').read()
        
        data = json.loads(f)
        if(data["status"]!="RUNNING"):
            # trials.append(i)
            if layers == 2:
                p_index = data["hyperparameters"]["values"]["params_index_two"]
        
                units1_nums.append(params_list[p_index]["u1"])
                units2_nums.append(params_list[p_index]["u2"])
                units3_nums.append(0)
                units4_nums.append(0)
                units5_nums.append(0)
        
            elif layers == 3:
                p_index = data["hyperparameters"]["values"]["params_index_three"]
                units1_nums.append(params_list[p_index]["u1"])
                units2_nums.append(params_list[p_index]["u2"])
                units3_nums.append(params_list[p_index]["u3"])
                units4_nums.append(0)
                units5_nums.append(0)

            else:
                units1_nums.append(params_list[5]["u1"])
                units2_nums.append(params_list[5]["u2"])
                units3_nums.append(params_list[5]["u3"])
                units4_nums.append(params_list[5]["u4"])
                units5_nums.append(params_list[5]["u5"])

            # batch_sizes.append(data["hyperparameters"]["values"]["batch_size"])
            batch_sizes.append(16)
            if data["score"]:
                scores.append(round(data["score"],8))


res = [units1_nums, units2_nums, units3_nums, units4_nums, units5_nums, batch_sizes, scores]
df = pd.DataFrame(res,index=["units1_nums", "units2_nums", "units3_nums", "units4_nums", "units5_nums", "batch_size", "score"])
df = df.T
df.sort_values(by="score", inplace=True, ascending=True)
df.to_csv("try_params_res_lstm.csv")