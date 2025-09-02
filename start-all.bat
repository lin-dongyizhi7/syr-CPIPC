@echo off
setlocal ENABLEDELAYEDEXPANSION

REM 项目根目录为当前脚本所在目录
cd /d %~dp0

echo 正在启动后端(Flask: port 666)...
start "Backend - Flask" cmd /k "cd /d py-back && python go-web.py"

echo 正在启动前端(Vite: port 7527)...
start "Frontend - Vite" cmd /k "cd /d DISFR-web && npm run dev"

echo 已在两个独立窗口中启动前后端服务。
exit /b 0
