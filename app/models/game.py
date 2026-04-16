from app.models import get_db_connection

def add_resource(player_id, resource_type, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    resource = cursor.execute("SELECT * FROM resources WHERE player_id = ? AND resource_type = ?", (player_id, resource_type)).fetchone()
    if resource:
        cursor.execute("UPDATE resources SET amount = amount + ? WHERE id = ?", (amount, resource['id']))
    else:
        cursor.execute("INSERT INTO resources (player_id, resource_type, amount) VALUES (?, ?, ?)", (player_id, resource_type, amount))
    conn.commit()
    conn.close()

def reduce_resource(player_id, resource_type, amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    resource = cursor.execute("SELECT * FROM resources WHERE player_id = ? AND resource_type = ?", (player_id, resource_type)).fetchone()
    if resource and resource['amount'] >= amount:
        cursor.execute("UPDATE resources SET amount = amount - ? WHERE id = ?", (amount, resource['id']))
        conn.commit()
        success = True
    else:
        success = False
    conn.close()
    return success

def get_player_resources(player_id):
    conn = get_db_connection()
    resources = conn.execute("SELECT * FROM resources WHERE player_id = ?", (player_id,)).fetchall()
    conn.close()
    return [dict(r) for r in resources]

def create_card(room_id, card_type, status='deck', owner_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cards (room_id, owner_id, card_type, status) VALUES (?, ?, ?, ?)", 
                   (room_id, owner_id, card_type, status))
    conn.commit()
    card_id = cursor.lastrowid
    conn.close()
    return card_id

def draw_card(room_id, player_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    card = cursor.execute("SELECT * FROM cards WHERE room_id = ? AND status = 'deck' LIMIT 1", (room_id,)).fetchone()
    if card:
        cursor.execute("UPDATE cards SET status = 'hand', owner_id = ? WHERE id = ?", (player_id, card['id']))
        conn.commit()
        ret = dict(card)
        ret['status'] = 'hand'
        ret['owner_id'] = player_id
    else:
        ret = None
    conn.close()
    return ret

def get_player_cards(player_id):
    conn = get_db_connection()
    cards = conn.execute("SELECT * FROM cards WHERE owner_id = ? AND status = 'hand'", (player_id,)).fetchall()
    conn.close()
    return [dict(c) for c in cards]

def play_card(card_id):
    conn = get_db_connection()
    conn.execute("UPDATE cards SET status = 'played' WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()

def add_game_log(room_id, user_id, action):
    conn = get_db_connection()
    conn.execute("INSERT INTO game_logs (room_id, user_id, action) VALUES (?, ?, ?)", (room_id, user_id, action))
    conn.commit()
    conn.close()

def get_game_logs(room_id):
    conn = get_db_connection()
    logs = conn.execute("""
        SELECT gl.*, u.username 
        FROM game_logs gl
        LEFT JOIN users u ON gl.user_id = u.id
        WHERE gl.room_id = ?
        ORDER BY gl.created_at ASC
    """, (room_id,)).fetchall()
    conn.close()
    return [dict(l) for l in logs]

def add_chat_message(room_id, user_id, message):
    conn = get_db_connection()
    conn.execute("INSERT INTO chat_messages (room_id, user_id, message) VALUES (?, ?, ?)", (room_id, user_id, message))
    conn.commit()
    conn.close()

def get_chat_messages(room_id):
    conn = get_db_connection()
    msgs = conn.execute("""
        SELECT cm.*, u.username 
        FROM chat_messages cm
        JOIN users u ON cm.user_id = u.id
        WHERE cm.room_id = ?
        ORDER BY cm.created_at ASC
    """, (room_id,)).fetchall()
    conn.close()
    return [dict(m) for m in msgs]

def create_trade_request(room_id, offerer_id, target_id, offer_resource, offer_amount, request_resource, request_amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO trade_requests 
        (room_id, offerer_id, target_id, offer_resource, offer_amount, request_resource, request_amount)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (room_id, offerer_id, target_id, offer_resource, offer_amount, request_resource, request_amount))
    conn.commit()
    trade_id = cursor.lastrowid
    conn.close()
    return trade_id

def get_pending_trades(room_id):
    conn = get_db_connection()
    trades = conn.execute("SELECT * FROM trade_requests WHERE room_id = ? AND status = 'pending'", (room_id,)).fetchall()
    conn.close()
    return [dict(t) for t in trades]

def update_trade_status(trade_id, status):
    conn = get_db_connection()
    conn.execute("UPDATE trade_requests SET status = ? WHERE id = ?", (status, trade_id))
    conn.commit()
    conn.close()
