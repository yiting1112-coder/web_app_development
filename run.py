import os
import sqlite3
from flask import Flask

from app.routes.auth_routes import auth_bp
from app.routes.room_routes import room_bp
from app.routes.game_routes import game_bp

def init_db(app):
    """初始化資料庫與資料表"""
    with app.app_context():
        db_path = os.path.join(app.instance_path, 'database.db')
        schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
        
        # 確保存在 instance 資料夾
        os.makedirs(app.instance_path, exist_ok=True)
            
        conn = sqlite3.connect(db_path)
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

def create_app():
    app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
    
    # 環境變數設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_default_secret_key')
    
    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 若 database.db 不存在，則自動初始化 Schema
    db_file_path = os.path.join(app.instance_path, 'database.db')
    if not os.path.exists(db_file_path):
        init_db(app)

    # 註冊 Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(game_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
