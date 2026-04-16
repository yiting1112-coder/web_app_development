import sqlite3
from app.models import get_db_connection

def create(data):
    """
    新增一筆使用者記錄。
    參數 data: dict，包含 'username' 與 'password_hash'
    回傳: 新增使用者的 ID，遇到錯誤（如帳號重複）回傳 None
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                       (data['username'], data['password_hash']))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        conn.close()

def get_all():
    """
    取得所有使用者記錄。
    回傳: 包含使用者字典的 list
    """
    conn = get_db_connection()
    try:
        users = conn.execute("SELECT id, username, created_at FROM users").fetchall()
        return [dict(u) for u in users]
    except sqlite3.Error as e:
        print(f"Error getting all users: {e}")
        return []
    finally:
        conn.close()

def get_by_id(id):
    """
    取得單筆使用者記錄。
    參數 id: 使用者的 ID
    回傳: user dict，找不到回傳 None
    """
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
        return dict(user) if user else None
    except sqlite3.Error as e:
        print(f"Error getting user by id: {e}")
        return None
    finally:
        conn.close()

def get_by_username(username):
    """
    透過使用者名稱取得記錄。
    參數 username: 使用者帳號
    回傳: user dict，找不到回傳 None
    """
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        return dict(user) if user else None
    except sqlite3.Error as e:
        print(f"Error getting user by username: {e}")
        return None
    finally:
        conn.close()

def update(id, data):
    """
    更新使用者記錄。
    參數 id: 使用者的 ID
    參數 data: 取 password_hash 進行更新
    回傳: boolean 代表是否成功
    """
    conn = get_db_connection()
    try:
        conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", 
                     (data['password_hash'], id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating user: {e}")
        return False
    finally:
        conn.close()

def delete(id):
    """
    刪除一筆使用者記錄。
    參數 id: 使用者 ID
    回傳: boolean 代表是否成功
    """
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")
        return False
    finally:
        conn.close()
