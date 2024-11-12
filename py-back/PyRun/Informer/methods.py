import pandas as pd
import sys
import os
from pathlib import Path

# 获取项目根目录
root = os.getenv('PROJECT_ROOT')

def initModelData(config):
    if config['file_info']['type'] == 'file':
        df = pd.DataFrame(config['data'])
        df.to_csv(f"{root}/opt/{config['file_info']['name']}-ind.csv")
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
        df.to_csv(f"{root}/opt/{config['file_info']['name']}-ind.csv")