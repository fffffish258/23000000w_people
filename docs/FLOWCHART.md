# [剩食與雜物互助系統] 流程圖設計 (Flowchart)

## 1. 使用者流程圖 (User Flow)

此圖展示了大學生進入系統後的主要操作路徑。

```mermaid
flowchart TD
    Start([使用者開啟網頁]) --> Home[首頁 - 物品布告欄]
    Home --> Filter{想要做什麼？}
    
    %% 搜尋與篩選
    Filter -->|搜尋與篩選| Search[輸入關鍵字或切換分類]
    Search --> List[瀏覽過濾後的物品清單]
    List --> Detail[點擊查看物品詳情]
    
    %% 發佈物品
    Filter -->|提供物資| Post[點擊「我要發佈」]
    Post --> Form[填寫物品資訊、分類與圖片網址]
    Form -->|如果是食品| Expiry[填寫有效日期]
    Form --> Submit[點擊送出]
    Submit --> Home
    
    %% 狀態管理
    Detail --> Manage{我是發佈者嗎？}
    Manage -->|是| Update[標記為「已領取」或「刪除」]
    Update --> Home
    Manage -->|否| Contact[取得領取資訊/聯繫發佈者]
```

---

## 2. 系統序列圖 (Sequence Diagram)

以「發佈物品」與「首頁載入（含過期過濾）」為例，展示資料在元件間的流動。

### A. 發佈物品流程
```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant DB as SQLite 資料庫

    User->>Browser: 填寫表單並點擊「發佈」
    Browser->>Flask: POST /create (包含標題、分類、效期等)
    Flask->>Flask: 驗證輸入格式與日期
    Flask->>DB: INSERT INTO items (status='Available')
    DB-->>Flask: 儲存成功
    Flask-->>Browser: HTTP Redirect (重導向至首頁)
    Browser->>User: 顯示「發佈成功」並更新清單
```

### B. 首頁載入流程 (含自動隱藏過期食品)
```mermaid
sequenceDiagram
    participant User as 使用者
    participant Flask as Flask Route
    participant DB as SQLite 資料庫

    User->>Flask: GET / (存取首頁)
    Flask->>Flask: 取得伺服器當前時間
    Flask->>DB: SELECT * FROM items WHERE status='Available' AND (expiry_date >= NOW OR expiry_date IS NULL)
    DB-->>Flask: 傳回有效物品列表
    Flask->>Flask: 渲染 Jinja2 模板
    Flask-->>User: 顯示首頁 HTML
```

---

## 3. 功能清單對照表 (URL Routes)

| 功能 | 頁面/動作 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** | 查看物品列表 | `/` | `GET` | 顯示所有可用的剩食與雜物 |
| **搜尋/篩選** | 搜尋物品 | `/` | `GET` | 透過 query string (如 `?q=蘋果&cat=food`) 進行過濾 |
| **發佈頁面** | 填寫發佈表單 | `/create` | `GET` | 顯示發佈物品的表單頁面 |
| **執行發佈** | 提交物品資料 | `/create` | `POST` | 將資料存入資料庫並重導向至首頁 |
| **物品詳情** | 查看單一物品 | `/item/<id>` | `GET` | 顯示物品詳細描述與大圖 |
| **標記已領取** | 更新物品狀態 | `/item/<id>/take` | `POST` | 將狀態改為 `Taken` 並在首頁隱藏 |
| **刪除物品** | 移除物品 | `/item/<id>/delete` | `POST` | 從資料庫或顯示清單中移除該物品 |
