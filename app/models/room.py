import sqlite3
from app.models import get_db_connection

def create_room(invite_code, host_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rooms (invite_code, host_id, status)
        VALUES (?, ?, 'waiting')
    """, (invite_code, host_id))
    conn.commit()
    room_id = cursor.lastrowid
    conn.close()
    return room_id

def get_room_by_id(room_id):
    conn = get_db_connection()
    room = conn.execute("SELECT * FROM rooms WHERE id = ?", (room_id,)).fetchone()
    conn.close()
    return dict(room) if room else None

def get_room_by_invite_code(invite_code):
    conn = get_db_connection()
    room = conn.execute("SELECT * FROM rooms WHERE invite_code = ?", (invite_code,)).fetchone()
    conn.close()
    return dict(room) if room else None

def update_room_status(room_id, status):
    conn = get_db_connection()
    conn.execute("UPDATE rooms SET status = ? WHERE id = ?", (status, room_id))
    conn.commit()
    conn.close()

def update_room_turn(room_id, current_turn_user_id):
    conn = get_db_connection()
    conn.execute("UPDATE rooms SET current_turn_user_id = ? WHERE id = ?", (current_turn_user_id, room_id))
    conn.commit()
    conn.close()

def delete_room(room_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
    conn.commit()
    conn.close()

def join_room(room_id, user_id, turn_order):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO players (room_id, user_id, turn_order)
            VALUES (?, ?, ?)
        """, (room_id, user_id, turn_order))
        conn.commit()
        player_id = cursor.lastrowid
    except sqlite3.Error:
        player_id = None
    finally:
        conn.close()
    return player_id

def get_players_in_room(room_id):
    conn = get_db_connection()
    players = conn.execute("""
        SELECT p.*, u.username 
        FROM players p
        JOIN users u ON p.user_id = u.id
        WHERE p.room_id = ?
        ORDER BY p.turn_order
    """, (room_id,)).fetchall()
    conn.close()
    return [dict(p) for p in players]
