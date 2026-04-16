import sqlite3
import os

def get_db_connection():
    """
    建立並回傳 SQLite 資料庫連線。
    設定 row_factory = sqlite3.Row，讓查詢結果可以用欄位名稱取值（類似 dict）。
    """
    try:
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        raise e
