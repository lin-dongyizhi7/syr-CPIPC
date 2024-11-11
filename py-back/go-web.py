from flask import request
from flask_cors import *

from json_flask import JsonFlask
from json_response import JsonResponse
from config import *

from PyRun.run import Runner

import json

# 创建视图应用
app = JsonFlask(__name__)

# 解决跨域
CORS(app, supports_credentials=True)

db = SQLManager()
runner = Runner(None)

# 编写视图函数，绑定路由
@app.route("/generateInd", methods=["GET"])  # 查询（全部）
def generateInd():
    data = json.loads(request.data)
    runner.loadData(data)
    result = runner.generateIndicates()
    return JsonResponse.success(msg='查询成功', data=result)


@app.route("/train", methods=["POST"])  # 添加（单个）
def train():
    data = json.loads(request.data)  # 将json字符串转为dict
    isOk = db.modify(sql='insert into user(name,age,sex) values(%s,%s,%s)',
                      args=[data['name'], data['age'], data['sex']])
    return JsonResponse.success(msg='添加成功') if isOk else JsonResponse.fail(msg='添加失败')


@app.route("/predict", methods=["POST"])  # 修改（单个）
def predict():
    data = json.loads(request.data)  # 将json字符串转为dict
    if 'id' not in data:
        return JsonResponse.fail(msg='需要传入id')
    isOk = db.modify(sql='update user set name=%s,age=%s,sex=%s where id=%s',
                      args=[data['name'], data['age'], data['sex'], data['id']])
    return JsonResponse.success(msg='修改成功') if isOk else JsonResponse.fail(msg='修改失败')


@app.route("/delete", methods=["DELETE"])  # 删除（单个）
def delete():
    if 'id' not in request.args:
        return JsonResponse.fail(msg='需要传入id')
    isOk = db.modify(sql='delete from user where id=%s', args=[request.args['id']])
    return JsonResponse.success(msg='删除成功') if isOk else JsonResponse.fail(msg='删除失败')


# 运行flask：默认是5000端口，此处设置端口为666
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=666, debug=True)
