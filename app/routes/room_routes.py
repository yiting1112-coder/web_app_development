from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
import random
import string
from app.models import room as room_model

room_bp = Blueprint('room', __name__)

def generate_invite_code(length=6):
    """產生隨機 6 碼大寫英數邀請碼"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@room_bp.route('/lobby', methods=['GET'])
def lobby():
    """
    顯示遊戲大廳。
    驗證必須為登入狀態，提供建立與加入房間的操作介面。
    """
    if 'user_id' not in session:
        flash("請先登入系統！", 'error')
        return redirect(url_for('auth.index'))
        
    return render_template('lobby.html', username=session.get('username'))

@room_bp.route('/room/create', methods=['POST'])
def create_room():
    """
    房主建立新房間。自動產生邀請碼且將自己加入為第 1 順位玩家。
    建立完畢後重導向至 /game/<room_id>。
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
        
    invite_code = generate_invite_code()
    user_id = session['user_id']
    
    room_id = room_model.create({
        'invite_code': invite_code,
        'host_id': user_id
    })
    
    if not room_id:
        flash("建立房間時發生錯誤，請重試。", "error")
        return redirect(url_for('room.lobby'))
        
    # 自動將房主加進第一順位
    room_model.add_player({
        'room_id': room_id,
        'user_id': user_id,
        'turn_order': 1
    })
    
    return redirect(url_for('game.game_board', room_id=room_id))

@room_bp.route('/room/join', methods=['POST'])
def join_room():
    """
    玩家輸入邀請碼加入別人建立的房間。
    若成功加入，重導向至 /game/<room_id>；失敗(如客滿或無效碼)則 flash 錯誤並停留原畫面。
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
        
    invite_code = request.form.get('invite_code', '').strip().upper()
    if not invite_code:
        flash("請輸入邀請碼！", "error")
        return redirect(url_for('room.lobby'))
        
    room = room_model.get_by_invite_code(invite_code)
    if not room:
        flash("找不到此邀請碼對應的房間！", "error")
        return redirect(url_for('room.lobby'))
        
    if room['status'] != 'waiting':
        flash("該房間已經開始遊戲或已經結束，無法加入了！", "error")
        return redirect(url_for('room.lobby'))
        
    # 檢查是否早就已經加入在裡面了
    players = room_model.get_players_by_room(room['id'])
    for p in players:
        if p['user_id'] == session['user_id']:
            # 已經加入，直接引導到房間裡面
            return redirect(url_for('game.game_board', room_id=room['id']))
            
    # 新玩家加入
    turn_order = len(players) + 1
    player_id = room_model.add_player({
        'room_id': room['id'],
        'user_id': session['user_id'],
        'turn_order': turn_order
    })
    
    if not player_id:
        flash("加入房間時發生錯誤！", "error")
        return redirect(url_for('room.lobby'))
        
    return redirect(url_for('game.game_board', room_id=room['id']))
