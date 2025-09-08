# pythonskeleton
python 基礎骨架


# 📦 Python 常用套件整理

## 🟢 內建標準函式庫 (Standard Library)
Python 安裝後就有，不需額外安裝。

### 系統相關
- `os`：檔案、路徑、環境變數操作  
- `sys`：Python 執行環境、模組載入路徑  
- `subprocess`：呼叫外部程式  
- `pathlib`：物件導向的檔案/路徑處理  
- `shutil`：複製、刪除檔案或資料夾  

### 時間 / 日期
- `datetime`：日期與時間處理  
- `time`：Unix 時間、延遲  
- `calendar`：月曆相關  

### 資料結構 / 演算法
- `collections`：`deque`, `Counter`, `defaultdict`  
- `heapq`：最小堆演算法  
- `functools`：`lru_cache`, `partial`  
- `itertools`：排列組合、迴圈工具  

### 序列化 / 檔案
- `json`：JSON 讀寫  
- `csv`：CSV 檔處理  
- `pickle`：Python 物件序列化  
- `gzip` / `zipfile` / `tarfile`：壓縮與解壓縮  

### 網路 / HTTP
- `http` / `urllib`：HTTP 請求（簡單版，通常用 `requests` 取代）  
- `socket`：TCP/UDP Socket  
- `ssl`：加密連線  

### 數學 / 隨機
- `math`：數學函式  
- `random`：隨機數產生  
- `statistics`：平均數、中位數、標準差  
- `decimal` / `fractions`：高精度數值  

### 其他常用
- `logging`：日誌系統  
- `argparse`：命令列參數解析  
- `typing`：型別提示  
- `re`：正則表達式  
- `threading` / `multiprocessing`：多執行緒與多行程  

---

## 🔵 常用外部套件 (需 pip install)

### 開發 / 工具
- `requests`：更好用的 HTTP 請求  
- `pydantic`：資料驗證與模型  
- `python-dotenv`：讀取 `.env` 設定檔  
- `rich`：終端機美化輸出（表格、進度條）  

### Web 框架
- `flask`：輕量 Web API 框架  
- `fastapi`：高效能 Web API 框架  
- `django`：大型 Web 框架  

### 資料處理
- `numpy`：數值運算  
- `pandas`：資料表處理（DataFrame）  
- `openpyxl`：Excel 讀寫  
- `sqlalchemy`：ORM，連接資料庫  

### 測試
- `pytest`：單元測試框架  
- `faker`：假資料產生  

### 資料庫
- `pymysql` / `mysql-connector-python`：MySQL 連線  
- `psycopg2`：PostgreSQL 連線  
- `redis`：Redis 客戶端  

### AI / 科學運算
- `scikit-learn`：機器學習  
- `matplotlib`：繪圖  
- `seaborn`：統計圖表  
- `opencv-python`：影像處理  
- `torch` (PyTorch) / `tensorflow`：深度學習  

### 其他熱門
- `loguru`：更簡單的 logging  
- `tqdm`：進度條顯示  
- `pillow`：影像處理 (PIL 分支)  
- `fastapi[all]`：安裝 FastAPI + 全套依賴  

---

✅ 建議：把 `.venv` 加入 `.gitignore`，避免把虛擬環境推上 Git。
