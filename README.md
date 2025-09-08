# Python 後端服務骨架(未完成)

一個完整的 Python 後端服務骨架，包含配置管理、資料庫操作、日誌系統、服務層架構和常用裝飾器。

## 🚀 功能特色

- **配置管理**: 支援多環境配置 (dev/test/prod)
- **資料庫整合**: SQLAlchemy ORM 與 MySQL 支援
- **日誌系統**: 彩色日誌、檔案輸出、不同環境配置
- **服務層架構**: 分層架構設計，支援依賴注入
- **裝飾器工具**: 重試、計時、驗證、資料庫操作等裝飾器
- **優雅關閉**: 信號處理和資源清理
- **型別提示**: 完整的型別註解支援

## 📁 專案結構

```
pythonskeleton/
├── config.py                 # 配置管理
├── logger.py                 # 日誌系統
├── main.py                   # 主程式入口
├── requirements.txt          # 依賴套件
├── decorators/               # 裝飾器模組
│   ├── __init__.py
│   ├── retry.py             # 重試裝飾器
│   ├── timing.py            # 計時裝飾器
│   ├── logging.py           # 日誌裝飾器
│   ├── validation.py        # 驗證裝飾器
│   └── database.py          # 資料庫裝飾器
├── repositories/             # 資料存取層
│   ├── initMySql.py         # 資料庫初始化
│   └── models/              # 資料模型
│       ├── __init__.py
│       ├── base.py          # 基礎模型
│       └── user.py          # 使用者模型
├── services/                 # 服務層
│   ├── __init__.py          # 服務模組初始化
│   ├── base.py              # 基礎服務類別
│   ├── user_service.py      # 使用者服務
│   ├── main_service.py      # 主要服務
│   └── notification_service.py # 通知服務
└── utils/                    # 工具模組
    └── helper.py            # 輔助函數
```

## 🛠️ 安裝與使用

### 1. 安裝依賴

```bash
pip install -r requirements.txt
```

### 2. 環境配置

建立 `.env` 檔案：

```env
# 應用程式環境設定
APP_ENV=dev

# 資料庫設定
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=your_database

# 日誌設定
LOG_LEVEL=INFO

# 效能設定
MAX_WORKERS=4
```

### 3. 執行應用程式

```bash
# 開發環境
python main.py

# 生產環境
python main.py --env prod

# 測試環境
python main.py --env test
```

## 🔧 主要模組說明

### 配置管理 (config.py)
- 支援多環境配置
- 自動載入 `.env` 檔案
- 配置驗證和錯誤處理
- 型別安全的配置物件

### 日誌系統 (logger.py)
- 彩色控制台輸出
- 檔案日誌記錄
- 不同環境的日誌配置
- 可自訂的日誌格式

### 資料庫層 (repositories/)
- SQLAlchemy ORM 整合
- 連線池管理
- 自動會話管理
- 基礎模型類別

### 服務層 (services/)
- **分層架構設計**: 每個服務類別獨立檔案，便於維護
- **基礎服務類別**: 提供共同功能和介面
- **使用者服務**: 處理使用者相關業務邏輯
- **主要服務**: 協調各個子服務的運作
- **通知服務**: 處理各種通知功能
- **依賴注入支援**: 服務間鬆耦合設計
- **錯誤處理和日誌記錄**: 統一的錯誤處理機制

### 裝飾器工具 (decorators/)
- **重試裝飾器**: 自動重試失敗的操作
- **計時裝飾器**: 測量函數執行時間
- **日誌裝飾器**: 自動記錄函數執行
- **驗證裝飾器**: 參數和返回值驗證
- **資料庫裝飾器**: 自動會話管理

## 📝 使用範例

### 基本服務使用

```python
from config import load_config
from services import MainService, UserService, NotificationService

# 載入配置
config = load_config()

# 建立主要服務
main_service = MainService(config)
main_service.initialize()

# 執行服務
main_service.run()

# 取得子服務
user_service = main_service.get_user_service()
notification_service = main_service.get_notification_service()

# 清理資源
main_service.cleanup()
```

### 使用特定服務

```python
from services import UserService, NotificationService

# 直接使用使用者服務
user_service = UserService(config)
user_service.initialize()

# 建立使用者
user = user_service.create_user(
    session, 
    username="testuser", 
    email="test@example.com", 
    password_hash="hashed_password"
)

# 使用通知服務
notification_service = NotificationService(config)
notification_service.initialize()

# 發送通知
notification_service.send_email_notification(
    to_email="user@example.com",
    subject="歡迎註冊",
    content="歡迎使用我們的服務！"
)
```

### 使用裝飾器

```python
from decorators import retry, timing, log_execution

@retry(max_attempts=3, delay=1.0)
@timing()
@log_execution()
def my_function():
    # 您的業務邏輯
    pass
```

### 資料庫操作

```python
from repositories.initMySql import get_db_session
from repositories.models import User

with get_db_session() as session:
    user = User.get_by_id(session, 1)
    print(user.username)
```

## 🎯 最佳實踐

1. **配置管理**: 使用環境變數和 `.env` 檔案管理敏感資訊
2. **錯誤處理**: 適當的例外處理和日誌記錄
3. **資源管理**: 使用上下文管理器確保資源正確釋放
4. **型別提示**: 為所有函數和類別添加型別註解
5. **測試**: 為關鍵功能編寫單元測試
6. **日誌記錄**: 適當的日誌等級和詳細的錯誤資訊

## 🔄 版本資訊

- **版本**: v1.0.0
- **Python**: 3.8+
- **主要依賴**: SQLAlchemy 2.0+, PyMySQL, python-dotenv


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


# 🐍 Python 裝飾器速查表

| 裝飾器 | 用途 | 範例 |
|--------|------|------|
| `@property` | 把方法變成屬性 (getter) | ```python\nclass Person:\n    def __init__(self, name):\n        self._name = name\n\n    @property\n    def name(self):\n        return self._name\n``` |
| `@<property>.setter` | 定義屬性的 setter | ```python\n    @name.setter\n    def name(self, value):\n        self._name = value\n``` |
| `@<property>.deleter` | 定義屬性的 deleter | ```python\n    @name.deleter\n    def name(self):\n        del self._name\n``` |
| `@classmethod` | 定義類別方法，第一參數是 `cls` | ```python\nclass Person:\n    @classmethod\n    def create_anonymous(cls):\n        return cls(\"無名氏\")\n``` |
| `@staticmethod` | 定義靜態方法，與類別/實例無關 | ```python\nclass Math:\n    @staticmethod\n    def add(a, b):\n        return a + b\n``` |
| `@dataclass` | 自動生成 `__init__`、`__repr__` 等 | ```python\nfrom dataclasses import dataclass\n@dataclass\nclass Point:\n    x: int\n    y: int\n``` |
| `@abstractmethod` | 定義抽象方法，強制子類別實作 | ```python\nfrom abc import ABC, abstractmethod\nclass Shape(ABC):\n    @abstractmethod\n    def area(self):\n        pass\n``` |
| `@functools.lru_cache` | 快取函式結果 (memoization) | ```python\nfrom functools import lru_cache\n@lru_cache(maxsize=None)\ndef fib(n):\n    return n if n < 2 else fib(n-1)+fib(n-2)\n``` |
| `@functools.cache` | (Python 3.9+) 無上限快取 | ```python\nfrom functools import cache\n@cache\ndef fib(n):\n    return n if n < 2 else fib(n-1)+fib(n-2)\n``` |
| `@functools.wraps` | 保留原函式資訊 (自訂裝飾器必備) | ```python\nfrom functools import wraps\ndef log(func):\n    @wraps(func)\n    def wrapper(*args, **kwargs):\n        print(\"呼叫\", func.__name__)\n        return func(*args, **kwargs)\n    return wrapper\n``` |

---

## 📝 自訂裝飾器範例
```python
def log(func):
    def wrapper(*args, **kwargs):
        print(f"執行 {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log
def say_hello():
    print("Hello")

say_hello()
# 輸出：
# 執行 say_hello
# Hello
