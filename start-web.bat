@echo off
echo Starting backend server...
cd py-back
start python go-web.py

echo Starting frontend server...
cd DISFR-web
start npm run serve

echo Both servers are running.
pause