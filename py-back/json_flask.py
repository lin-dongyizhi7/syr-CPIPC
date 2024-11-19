'''
Author: lin-dongyizhi7 2985956026@qq.com
Date: 2024-11-15 00:20:22
LastEditors: lin-dongyizhi7 2985956026@qq.com
LastEditTime: 2024-11-19 17:11:29
FilePath: \systemic financial crises\py-back\json_flask.py
Description: Systemic Financial Crises
'''
from flask import Flask, jsonify

from json_response import JsonResponse


class JsonFlask(Flask):
    def make_response(self, rv):
        # 视图函数可以直接返回: list、dict、None
        if rv is None or isinstance(rv, (list, dict)):
            rv = JsonResponse.success(rv)

        if isinstance(rv, JsonResponse):
            rv = jsonify(rv.to_dict())

        return super().make_response(rv)
