# 系统性金融风险

## 1.简介
这是一个用于训练并预测系统性金融风险的工程。在该工程中，你可以构造风险指标，
从多种模型中(DWT-Informer, Informer, LSTM, GRU)选择并训练得到自己的预测模型用于系统性金融风险的预测。

## 2.使用方法

要使用此项目，请按照以下步骤操作：

### 1. 克隆仓库

### 2. 安装依赖
**安装 Python 依赖项**  
在 `py-back` 文件夹中运行：
```bash
pip install -r requirements.txt
```

**安装 Vue 依赖项**  
在 `DISFR-web` 文件夹中运行：
```bash
npm install
```

### 3. 一键启动（推荐）
在项目根目录双击 `start-all.bat`，批处理将：
- 启动 Python 后端服务（Flask，端口 666）
- 启动 Vue 前端服务（Vite，端口 7527）

启动完成后，浏览器访问：`http://localhost:7527`

### 4. 手动启动（可选）
分别在两个终端中执行：
- 后端：
```bash
cd py-back
python go-web.py
```
- 前端：
```bash
cd DISFR-web
npm run dev
```