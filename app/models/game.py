import sqlite3
from app.models import get_db_connection

# ---- Resources ----
def create_resource(data):
    """
    操作資源。給定 player_id 增加某種資源。
    data: {'player_id': 1, 'resource_type': 'wood', 'amount': 1}
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        resource = cursor.execute("SELECT * FROM resources WHERE player_id = ? AND resource_type = ?", 
                                  (data['player_id'], data['resource_type'])).fetchone()
        if resource:
            cursor.execute("UPDATE resources SET amount = amount + ? WHERE id = ?", 
                           (data['amount'], resource['id']))
        else:
            cursor.execute("INSERT INTO resources (player_id, resource_type, amount) VALUES (?, ?, ?)", 
                           (data['player_id'], data['resource_type'], data['amount']))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error adding resource: {e}")
        return False
    finally:
        conn.close()

def update_resource(id, data):
    """
    減少或更新物資 (可以直接指定數量扣除)。
    """
    conn = get_db_connection()
    try:
        if data.get('action') == 'reduce':
            cursor = conn.cursor()
            resource = cursor.execute("SELECT * FROM resources WHERE id = ?", (id,)).fetchone()
            if resource and resource['amount'] >= data['amount']:
                cursor.execute("UPDATE resources SET amount = amount - ? WHERE id = ?", 
                               (data['amount'], id))
                conn.commit()
                return True
            return False
    except sqlite3.Error as e:
        print(f"Error updating resource: {e}")
        return False
    finally:
        conn.close()

def get_all_by_player(player_id):
    """取得玩家的所有資源清單"""
    conn = get_db_connection()
    try:
        resources = conn.execute("SELECT * FROM resources WHERE player_id = ?", (player_id,)).fetchall()
        return [dict(r) for r in resources]
    except sqlite3.Error as e:
        return []
    finally:
        conn.close()

# ---- Cards ----
def create_card(data):
    """
    新增一張卡牌。data: {'room_id', 'card_type', 'status', 'owner_id' (optional)}
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        owner_id = data.get('owner_id')
        cursor.execute("INSERT INTO cards (room_id, owner_id, card_type, status) VALUES (?, ?, ?, ?)", 
                       (data['room_id'], owner_id, data['card_type'], data.get('status', 'deck')))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating card: {e}")
        return None
    finally:
        conn.close()

def get_cards_by_player(player_id):
    """取得該玩家手上的卡牌"""
    conn = get_db_connection()
    try:
        cards = conn.execute("SELECT * FROM cards WHERE owner_id = ? AND status = 'hand'", (player_id,)).fetchall()
        return [dict(c) for c in cards]
    except sqlite3.Error as e:
        return []
    finally:
        conn.close()

def update_card(id, data):
    """更改卡片狀態 (例如抽出或打出)"""
    conn = get_db_connection()
    try:
        updates = []
        params = []
        if 'status' in data:
            updates.append("status = ?")
            params.append(data['status'])
        if 'owner_id' in data:
            updates.append("owner_id = ?")
            params.append(data['owner_id'])
            
        params.append(id)
        if updates:
            conn.execute(f"UPDATE cards SET {', '.join(updates)} WHERE id = ?", params)
            conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating card: {e}")
        return False
    finally:
        conn.close()

# ---- Trade Requests ----
def create_trade(data):
    """新增交易請求。data: {room_id, offerer_id, target_id, offer_resource, offer_amount, request_resource, request_amount}"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trade_requests 
            (room_id, offerer_id, target_id, offer_resource, offer_amount, request_resource, request_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data['room_id'], data['offerer_id'], data.get('target_id'), 
              data['offer_resource'], data['offer_amount'], data['request_resource'], data['request_amount']))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating trade: {e}")
        return None
    finally:
        conn.close()

def update_trade(id, data):
    """更新交易狀態。data: {'status': 'accepted', ...}"""
    conn = get_db_connection()
    try:
        conn.execute("UPDATE trade_requests SET status = ? WHERE id = ?", (data['status'], id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        return False
    finally:
        conn.close()

def get_trades_by_room(room_id):
    conn = get_db_connection()
    try:
        trades = conn.execute("SELECT * FROM trade_requests WHERE room_id = ? AND status = 'pending'", (room_id,)).fetchall()
        return [dict(t) for t in trades]
    except sqlite3.Error:
        return []
    finally:
        conn.close()

# ---- Logs & Chat ----
def create_log(data):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO game_logs (room_id, user_id, action) VALUES (?, ?, ?)", 
                     (data['room_id'], data.get('user_id'), data['action']))
        conn.commit()
        return True
    except sqlite3.Error as e:
        return False
    finally:
        conn.close()

def create_chat(data):
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO chat_messages (room_id, user_id, message) VALUES (?, ?, ?)", 
                     (data['room_id'], data['user_id'], data['message']))
        conn.commit()
        return True
    except sqlite3.Error:
        return False
    finally:
        conn.close()
