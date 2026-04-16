import sqlite3
from app.models import get_db_connection

def create(data):
    """
    新增一筆房間記錄。
    參數 data: dict，需包含 'invite_code', 'host_id'
    回傳: 新增的 room_id，失敗則回傳 None
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rooms (invite_code, host_id, status) VALUES (?, ?, 'waiting')", 
                       (data['invite_code'], data['host_id']))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating room: {e}")
        return None
    finally:
        conn.close()

def get_all():
    """
    取得所有的房間。
    回傳: room dict list
    """
    conn = get_db_connection()
    try:
        rooms = conn.execute("SELECT * FROM rooms").fetchall()
        return [dict(r) for r in rooms]
    except sqlite3.Error as e:
        print(f"Error getting all rooms: {e}")
        return []
    finally:
        conn.close()

def get_by_id(id):
    """
    依據 ID 取得房間錄。
    """
    conn = get_db_connection()
    try:
        room = conn.execute("SELECT * FROM rooms WHERE id = ?", (id,)).fetchone()
        return dict(room) if room else None
    except sqlite3.Error as e:
        print(f"Error getting room by id: {e}")
        return None
    finally:
        conn.close()

def get_by_invite_code(invite_code):
    """
    透過邀請碼取得房間資訊。
    """
    conn = get_db_connection()
    try:
        room = conn.execute("SELECT * FROM rooms WHERE invite_code = ?", (invite_code,)).fetchone()
        return dict(room) if room else None
    except sqlite3.Error as e:
        print(f"Error getting room by invite code: {e}")
        return None
    finally:
        conn.close()

def update(id, data):
    """
    更新房間記錄（例如狀態或換回合）。
    參數 data: 可包含 'status' 或 'current_turn_user_id'。
    """
    conn = get_db_connection()
    try:
        if 'status' in data:
            conn.execute("UPDATE rooms SET status = ? WHERE id = ?", (data['status'], id))
        if 'current_turn_user_id' in data:
            conn.execute("UPDATE rooms SET current_turn_user_id = ? WHERE id = ?", (data['current_turn_user_id'], id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating room: {e}")
        return False
    finally:
        conn.close()

def delete(id):
    """刪除單筆房間紀錄"""
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM rooms WHERE id = ?", (id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting room: {e}")
        return False
    finally:
        conn.close()

# ---- Player In Room CRUD ----

def add_player(data):
    """
    將玩家加入房間 (Players Table)
    參數 data: 需包含 'room_id', 'user_id', 'turn_order'
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO players (room_id, user_id, turn_order) VALUES (?, ?, ?)", 
                       (data['room_id'], data['user_id'], data['turn_order']))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error adding player: {e}")
        return None
    finally:
        conn.close()

def get_players_by_room(room_id):
    """取得某房間內所有加入的玩家名單"""
    conn = get_db_connection()
    try:
        players = conn.execute("""
            SELECT p.*, u.username 
            FROM players p
            JOIN users u ON p.user_id = u.id
            WHERE p.room_id = ?
            ORDER BY p.turn_order
        """, (room_id,)).fetchall()
        return [dict(p) for p in players]
    except sqlite3.Error as e:
        print(f"Error getting players: {e}")
        return []
    finally:
        conn.close()
