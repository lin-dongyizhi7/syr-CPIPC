'''
Description: Systemic Financial Crises
version: 1.0
Author: YZP & SYR
Email: yys220124@outlook.com
Tip: Competition code support only, please contact the author
'''
import sys
import os
from pathlib import Path

# 获取项目根目录
root = os.getenv('PROJECT_ROOT')

# 获取项目根目录
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.append(project_root)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from tqdm import tqdm
import time

def CDF(X):
    X.dropna(inplace = True)#删去空值
    X = X.sort_values()#按值排序
    for i in range(len(X)):
        if X[i] == X.iloc[-1]:
            X[i] = 1
        else:
            if X[i]<X[i+1]:
                X[i] = (i+1)/len(X)
            else:
                for j in range(i+1,len(X)):
                    a = j
                    if X[i] == X[j]:
                        a = a+1
                    else:
                        break
                    X[i] = a/len(X)
    X.sort_index(inplace = True)#按时间顺序排
    return X

def ICDF(X):
    X.dropna(inplace = True)#删去空值
    for i in range(1,len(X)+1):#倒着遍历
        a = 0#记录前面比该元素大的数据的个数
        for j in range(len(X)-i):
            if X[-i] < X[j]:
                a = a+1
        X.iloc[-i] = 1 - a/(len(X)-i+1)#直接计算
    return X

def INDEX(X,lam):
    d = X.shape[1]-1#列数-1，最后一列存储结果
    a = X.columns#列名
    w = np.ones(d)/d#权重向量
    for k in tqdm(range(d), desc="Sub to get new indicates:"):
        X[a[k]] = X[a[k]].map(lambda x: x-0.5)#各子指标减去理论均值得到新的子指标
    X_s =  X.applymap(lambda x: x**2)#都取平方，为方差计算做准备
    for t in tqdm(range(len(X)), desc="Calculating everyday indicates:"):#该循环计算每一天的总指标
        s = list(X.iloc[t,:-1]+0.5)#为后面计算总指标时，需要用原始子指标，做准备
        C = np.eye(d)#构造和相关矩阵大小一样的矩阵
        sig_i = X_s.applymap(lambda x: x**2)#存储方差
        for k in range(d):#用EWMA计算方差
            sig_i.iloc[:,k] = X_s.iloc[:,k].ewm(alpha=1-lam,adjust=False).mean()#lam即式中lamda
        for i in range(d):#用EWMA计算协方差，并计算
            Cov = X.applymap(lambda x: x**2)#存储协方差
            for j in range(d):
                Y_s = X.iloc[:,i]*X.iloc[:,j]#交叉点乘,为了计算相关系数
                Cov.iloc[:,j] = Y_s.ewm(alpha=1-lam,adjust=False).mean()#存储协方差
                C[i,j] = Cov.iloc[t,j]/(sig_i.iloc[t,i]*sig_i.iloc[t,j])**0.5#计算相关系数
        X.iloc[t,d] = s@C@s/(d**2)#将总指标存到最后一列
    return X

negative = []
def is_number(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False
def dataLoader(data):
    # 读取
    if 'filePath' in data.keys():
        path = data['filePath']
        file_extension = Path(path).suffix.lower()

        # 根据文件扩展名选择读取方法
        if file_extension == '.csv':
            df = pd.read_csv(path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(path)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
    else:
        df = pd.DataFrame(data['data'])

    used_cols = ['date'] + data['cols']
    df = df[used_cols]
    # 复值取反
    for column in df.columns:
        # 检查列中的值是否全部为负数
        if is_number(df[column]) and any(df[column] < 0):
            negative.append(column)
            # 将该列的所有值取反
            df[column] = -df[column]

    df['date'] = df['date'].astype('datetime64[ns]')  # 转化时间格式
    df = df.set_index('date')  # 设置时间索引
    return df

def generateInd(init_data):
    name = init_data['name'].split('.')[0]
    data = dataLoader(init_data)

    # 测试用
    # data.to_excel(f"{root}/opt/{name}-ind.xlsx")
    # return

    # start_day = '2018-01-01'
    # con1 = data.index < start_day

    print(data.head())

    date = data.index.tolist()

    head_len = int(len(data) * 2 / 3)
    header = data[:head_len]

    # 前面的数据做CDF
    b = []
    for m in tqdm(range(header.shape[1]), desc="CDF-step1:"):
        b.append(CDF(header.iloc[:, m]))
    cdf_all = b[0]
    for i in tqdm(range(1, len(b)), desc="CDF-step2:"):
        cdf_all = pd.concat([cdf_all, b[i]], axis=1)
    cdf_all.dropna(inplace=True)

    # 后面的做ICDF,先全部后剪切
    a = []
    for m in tqdm(range(data.shape[1]), desc="ICDF-step1:"):
        a.append(ICDF(data.iloc[:, m]))
    ic_all = a[0]
    for i in tqdm(range(1, len(a)), desc="ICDF-step2:"):
        ic_all = pd.concat([ic_all, a[i]], axis=1)
    ic_all.dropna(inplace=True)  # 将上面的数据组合

    # con2 = ic_all.index >= start_day
    # ic_all = ic_all[con2]  # 取之后的
    ic_all = ic_all[head_len-1:]


    EW = pd.concat([cdf_all, ic_all], axis=0)
    EW = pd.concat([EW, pd.DataFrame(columns=['ind'])], sort=False)
    INDEX(EW, 0.93)

    EW.insert(0, 'date', date)
    EW.set_index('date')

    EW.to_csv(os.path.normpath(f"{root}/opt/{name}-ind.csv"), index=False)

    ind_col = EW.loc[:, "ind"]
    mean = ind_col.mean()
    std = ind_col.std()
    ms = mean + std

    if not init_data['draw']:
        return

    ind_col.plot(x_compat=True, figsize=(20, 10))
    matplotlib.pyplot.axhline(init_data['drawThreshold'])
    plt.ylabel("ind")
    plt.autoscale(enable=True, axis='y')
    plt.savefig(os.path.normpath(f"{root}/opt/{name}-ind.png"))
    # plt.show()

    result = {'info': 'success'}
    return result