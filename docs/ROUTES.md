# [剩食與雜物互助系統] 路由設計 (Routes)

## 1. 路由總覽表格

本系統採用 Flask + Jinja2 架構，所有的頁面跳轉與資料提交均透過以下路由處理。

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁 (物品清單)** | GET | `/` | `index.html` | 顯示所有「可領取」且「未過期」的物品清單。支援搜尋與分類篩選。 |
| **發佈頁面** | GET | `/items/new` | `create.html` | 顯示發佈新物品的表單。 |
| **建立物品** | POST | `/items/new` | — | 接收並驗證表單資料，存入資料庫後重導向至首頁。 |
| **物品詳情** | GET | `/items/<int:id>` | `detail.html` | 顯示該物品的詳細描述、完整圖片與發佈時間。 |
| **標記已領取** | POST | `/items/<int:id>/take` | — | 將物品狀態改為 `Taken`，處理完後重導向至首頁。 |
| **刪除物品** | POST | `/items/<int:id>/delete` | — | 從資料庫刪除該物品資訊，處理完後重導向至首頁。 |

---

## 2. 每個路由的詳細說明

### 首頁 (Index)
- **路徑**：`/`
- **參數 (Query String)**：
  - `q`: 搜尋關鍵字 (選填)
  - `cat`: 分類篩選 (`Food` / `Misc` / `All`)
- **處理邏輯**：
  1. 呼叫 `Item.get_all_available()` 取得基礎清單。
  2. 若有 `q`，則對標題或描述進行關鍵字過濾。
  3. 若有 `cat` 且非 `All`，則篩選特定分類。
- **輸出**：渲染 `index.html`。

### 建立物品 (Create Item)
- **路徑**：`/items/new`
- **表單欄位**：
  - `title`: 物品名稱 (必填)
  - `description`: 描述
  - `category`: 分類 (必填，下拉選單)
  - `image_url`: 圖片連結
  - `expiry_date`: 有效日期 (食品類必填)
- **處理邏輯**：
  1. 檢查必填欄位。
  2. 若為食品類，確保日期格式正確且不為空。
  3. 實體化 `Item` 並存入資料庫。
- **輸出**：成功後重導向至 `/`；失敗則帶回表單並顯示錯誤訊息。

---

## 3. Jinja2 模板清單

所有的模板均存放於 `app/templates/` 目錄下。

| 檔案名稱 | 說明 | 繼承模板 |
| :--- | :--- | :--- |
| `base.html` | 基礎佈局 (包含 Navigation, CSS 連結, Footer) | — |
| `index.html` | 首頁布告欄，包含搜尋框、分類按鈕與物品卡片列表 | `base.html` |
| `create.html` | 物品發佈表單頁面 | `base.html` |
| `detail.html` | 物品詳情顯示頁面 | `base.html` |

---

## 4. 路由骨架程式碼 (參考)

路徑：`app/routes/main.py`

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.item import Item

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """顯示首頁物品列表，支援關鍵字搜尋與分類篩選"""
    pass

@main_bp.route('/items/new', methods=['GET', 'POST'])
def create_item():
    """顯示發佈表單 (GET) 或 處理表單提交 (POST)"""
    pass

@main_bp.route('/items/<int:id>')
def item_detail(id):
    """查看特定物品的詳細資訊"""
    pass

@main_bp.route('/items/<int:id>/take', methods=['POST'])
def take_item(id):
    """將物品標記為已領取"""
    pass

@main_bp.route('/items/<int:id>/delete', methods=['POST'])
def delete_item(id):
    """刪除物品"""
    pass
```
