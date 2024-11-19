'''
Author: lin-dongyizhi7 2985956026@qq.com
Date: 2024-11-15 00:20:22
LastEditors: lin-dongyizhi7 2985956026@qq.com
LastEditTime: 2024-11-19 17:10:52
FilePath: \systemic financial crises\py-back\go-web.py
Description: Systemic Financial CrisesE
'''

import sys
import os
import glob
import subprocess

project_root = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

# 在项目的入口点设置环境变量
os.environ['PROJECT_ROOT'] = project_root
# print(f'project root:{project_root}')

# for i in sys.path:
#     print(i)

from flask import request
from flask_cors import *

from json_flask import JsonFlask
from json_response import JsonResponse

from PyRun.run import Runner
from start_vue import start_vue_server

import json

from art import text2art

# pipreqs生成使用到的包的requirements.txt

# 艺术字
art_text_1 = text2art(f"SYSTEMIC FINANCIAL\n RISK", font='slant')
print(art_text_1)

# 创建视图应用
app = JsonFlask(__name__)

# 解决跨域
CORS(app, supports_credentials=True)

start_vue_server()

runner = Runner()

# 创建子进程
process = subprocess.Popen([os.path.normpath(project_root + 'DISFR-web/src/assets/logo.exe')], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 获取输出
stdout, stderr = process.communicate()

# 输出结果
print("", stdout.decode('utf-8'))
print("", stderr.decode('utf-8'))

print('start----------')

# 编写视图函数，绑定路由
@app.route("/generateInd", methods=["POST"])  # 构造指标
def generateInd():
    data = json.loads(request.data)
    runner.loadIndData(data)
    result = runner.generateIndexes()
    return JsonResponse.success(msg='查询成功', data=result)


@app.route("/train", methods=["POST"])  # 训练
def train():
    data = json.loads(request.data)  # 将json字符串转为dict
    params = {
        'model': data['baseModel'],
        'model_config': {
            'totalEpoch': data['totalEpoch'],
            'batchSize': data['batchSize'],
            'gpu': data['gpu'],
        },
        'file_info': {
            'type': data['type'],
            'name': data['name'],
            'path': data['filePath'] if 'filePath' in data else '',
        },
        'data': data['data'] if 'data' in data else ''
    }
    runner.loadTrainParams(params)
    isOk = runner.train()
    return JsonResponse.success(msg='训练成功') if isOk else JsonResponse.fail(msg='训练失败')


@app.route("/predict", methods=["POST"])  # 预测
def predict():
    data = json.loads(request.data)  # 将json字符串转为dict
    params = {
        'model': data['model'],
        'file_info': {
            'type': data['type'],
            'name': data['name'],
            'path': data['filePath'] if 'filePath' in data else '',
        },
        'draw_config': {
            'drawStyle': data['drawStyle'],
        },
        'data': data['data'] if 'data' in data else '',
        'pred_len': data['pred_len'],
        'output': ''
    }
    runner.loadPredictParams(params)
    isOk = runner.predict()
    return JsonResponse.success(msg='预测成功') if isOk else JsonResponse.fail(msg='预测失败')

@app.route("/getModelsList", methods=["GET"])
def getModelsList():
    pth_files = []
    result = []
    # 使用 glob 模块递归查找所有 .pth 文件
    for dir_path, _, _ in os.walk(project_root + '/models'):
        for ext in ['*.pth', '*.h5']:
            pth_files.extend(glob.glob(os.path.join(dir_path, ext)))
    for pth in pth_files:
        result.append(pth.replace('/', '\\'))
    return JsonResponse.success(msg='模型列表查询成功', data=result)

# 运行flask：默认是5000端口，此处设置端口为666
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=666, debug=True)
