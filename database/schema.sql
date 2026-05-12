-- 建立物品資料表
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(20) NOT NULL, -- 'Food' or 'Misc'
    image_url VARCHAR(500),
    expiry_date DATE,
    status VARCHAR(20) DEFAULT 'Available', -- 'Available' or 'Taken'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 建立索引以優化篩選效能
CREATE INDEX idx_item_status_category ON items(status, category);
CREATE INDEX idx_item_expiry ON items(expiry_date);
