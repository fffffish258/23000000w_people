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

    @classmethod
    def get_all_available(cls):
        """取得所有狀態為 Available 且未過期的物品"""
        now = datetime.utcnow().date()
        return cls.query.filter(
            cls.status == 'Available',
            db.or_(
                cls.expiry_date >= now,
                cls.expiry_date == None
            )
        ).order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_category(cls, category):
        """按分類篩選有效物品"""
        now = datetime.utcnow().date()
        return cls.query.filter(
            cls.status == 'Available',
            cls.category == category,
            db.or_(
                cls.expiry_date >= now,
                cls.expiry_date == None
            )
        ).order_by(cls.created_at.desc()).all()

    def mark_as_taken(self):
        """標記為已領取"""
        self.status = 'Taken'
        db.session.commit()
