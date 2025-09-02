# Systemic Financial Risk

## 1. Introduction
This project is designed to train and predict systemic financial risk. In this project, you can construct risk indicators and select from multiple models (DWT-Informer, Informer, LSTM, GRU) to train your own models for prediction.

## 2. Getting Started

Follow these steps:

### 1) Clone the repository

### 2) Install dependencies
**Install Python dependencies**  
Run in the `py-back` folder:
```bash
pip install -r requirements.txt
```

**Install Vue dependencies**  
Run in the `DISFR-web` folder:
```bash
npm install
```

### 3) One-click start (recommended)
Double-click `start-all.bat` in the project root. It will:
- Start the Python backend (Flask on port 666)
- Start the Vue frontend (Vite on port 7527)

Then open your browser at `http://localhost:7527`.

### 4) Manual start (optional)
Run them in two terminals:
- Backend:
```bash
cd py-back
python go-web.py
```
- Frontend:
```bash
cd DISFR-web
npm run dev
```