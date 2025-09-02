'''
Description: Systemic Financial Crises
version: 1.0
Author: YZP & SYR
Email: yys220124@outlook.com
Tip: Competition code support only, please contact the author
'''
import pandas as pd
import sys
import os
from pathlib import Path

# 获取项目根目录
root = os.getenv('PROJECT_ROOT')

def initModelData(config):
    name = config['file_info']['name']
    path = f"{root}/opt/{name}"
    if not os.path.exists(path):
        os.makedirs(path)

    if config['file_info']['type'] == 'file':
        df = pd.DataFrame(config['data'])
        df.to_csv(f"{path}/{name}.csv", index=False)
    else:
        path = config['file_info']['path']
        file_extension = Path(path).suffix.lower()

        # 根据文件扩展名选择读取方法
        if file_extension == '.csv':
            df = pd.read_csv(path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(path)
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")
        df.to_csv(f"{path}/{name}.csv", index=False)

    return df