'''
Author: lin-dongyizhi7 2985956026@qq.com
Date: 2024-11-15 00:20:22
LastEditors: lin-dongyizhi7 2985956026@qq.com
LastEditTime: 2024-11-19 17:12:17
FilePath: \systemic financial crises\py-back\json_response.py
Description: Systemic Financial Crises
'''
# 统一的json返回格式

class JsonResponse(object):

    def __init__(self, code, msg, data):
        self.code = code
        self.msg = msg
        self.data = data

    # 指定一个类的方法为类方法，通常用self来传递当前类的实例--对象，cls传递当前类。
    @classmethod
    def success(cls, code=200, msg='success', data=None):
        return cls(code, msg, data)

    @classmethod
    def fail(cls, code=400, msg='fail', data=None):
        return cls(code, msg, data)

    def to_dict(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data
        }
