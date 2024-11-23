'''
Description: Systemic Financial Crises
version: 1.0
Author: YZP & SYR
Email: yys220124@outlook.com
Tip: Competition code support only, please contact the author
'''
import pandas as pd
import numpy as np
from pywt import wavedec
from pywt import idwt

import os

# 获取项目根目录
root = os.getenv('PROJECT_ROOT')

def DWT(X, cols, wavelet, level):
    for i in cols:
        if i == 'ind':
            break
        for j in range(level):
            coeffs = wavedec(X[i],wavelet,level=1)
            m = idwt(coeffs[0], None, wavelet, 'smooth')
            if len(m) == len(X):
                X[i] = m
            else:
                X[i] = m[:len(X)]
    return X#定义小波分解函数

def getDWTRes(df, name):
    # print(df.head())
    cols = df.columns.tolist()[1:]
    df_DWT = DWT(df, cols, 'sym4', 4)

    df_DWT['date'] = df['date'].astype('datetime64[ns]')  # 转化时间格式

    path = f"{root}/opt/{name}"
    if not os.path.exists(path):
        os.makedirs(path)

    df_DWT.to_csv(os.path.normpath(f"{path}/{name}-DWT.csv"), index=False)

    return cols
