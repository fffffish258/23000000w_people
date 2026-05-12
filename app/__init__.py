import os
from flask import Flask
from app.models.item import db
from app.routes.main import main_bp

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # 預設設定
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'database.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 初始化套件
    db.init_app(app)

    # 註冊 Blueprint
    app.register_blueprint(main_bp)

    # 初始化資料庫命令
    @app.cli.command("init-db")
    def init_db():
        """初始化資料庫並建立資料表"""
        db.create_all()
        print("Initialized the database.")

    return app
