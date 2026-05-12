from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(20), nullable=False)  # 'Food', 'Misc'
    image_url = db.Column(db.String(500), nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='Available') # 'Available', 'Taken'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Item {self.title}>'

    # --- CRUD Methods ---

    @classmethod
    def create(cls, title, category, description=None, image_url=None, expiry_date=None):
        """新增一筆物品記錄"""
        try:
            new_item = cls(
                title=title,
                category=category,
                description=description,
                image_url=image_url,
                expiry_date=expiry_date
            )
            db.session.add(new_item)
            db.session.commit()
            return new_item
        except Exception as e:
            db.session.rollback()
            print(f"Error creating item: {e}")
            return None

    @classmethod
    def get_all(cls):
        """取得所有記錄 (不論狀態)"""
        try:
            return cls.query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error getting items: {e}")
            return []

    @classmethod
    def get_by_id(cls, item_id):
        """取得單筆記錄"""
        try:
            return cls.query.get(item_id)
        except Exception as e:
            print(f"Error getting item by id: {e}")
            return None

    def update(self, **kwargs):
        """更新記錄內容"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating item: {e}")
            return False

    def delete(self):
        """刪除記錄"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting item: {e}")
            return False

    # --- Specialized Search Methods ---

    @classmethod
    def get_all_available(cls, keyword=None, category=None):
        """
        取得所有狀態為 Available 且未過期的物品。
        支援關鍵字搜尋與分類篩選。
        """
        try:
            now = datetime.utcnow().date()
            query = cls.query.filter(
                cls.status == 'Available',
                db.or_(
                    cls.expiry_date >= now,
                    cls.expiry_date == None
                )
            )

            if keyword:
                query = query.filter(
                    db.or_(
                        cls.title.contains(keyword),
                        cls.description.contains(keyword)
                    )
                )
            
            if category and category != 'All':
                query = query.filter(cls.category == category)

            return query.order_by(cls.created_at.desc()).all()
        except Exception as e:
            print(f"Error filtering available items: {e}")
            return []

    def mark_as_taken(self):
        """標記為已領取 (邏輯刪除)"""
        return self.update(status='Taken')
