from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session

room_bp = Blueprint('room', __name__)

@room_bp.route('/lobby', methods=['GET'])
def lobby():
    """
    顯示遊戲大廳。
    驗證必須為登入狀態，提供建立與加入房間的操作介面。
    """
    pass

@room_bp.route('/room/create', methods=['POST'])
def create_room():
    """
    房主建立新房間。自動產生邀請碼且將自己加入為第 1 順位玩家。
    建立完畢後重導向至 /game/<room_id>。
    """
    pass

@room_bp.route('/room/join', methods=['POST'])
def join_room():
    """
    玩家輸入邀請碼加入別人建立的房間。
    若成功加入，重導向至 /game/<room_id>；失敗(如客滿或無效碼)則 flash 錯誤並停留原畫面。
    """
    pass
