'''
Author: lin-dongyizhi7 2985956026@qq.com
Date: 2024-11-15 00:20:22
LastEditors: lin-dongyizhi7 2985956026@qq.com
LastEditTime: 2024-11-19 17:12:48
FilePath: \systemic financial crises\py-back\start_vue.py
Description: Systemic Financial Crises
'''
import subprocess
import os

def start_vue_server():
    # 切换到前端项目的目录
    frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'DISFR-web')

    # 使用 subprocess.Popen 启动 Vue 前端服务
    try:
        process = subprocess.Popen(['npm', 'run', 'dev'], cwd=frontend_dir, shell=True)
        print("Vue frontend server started.")
    except Exception as e:
        print(f"Error starting Vue frontend server: {e}")