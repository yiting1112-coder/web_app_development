from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import user as user_model

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁與登入/註冊介面。
    若 session 中已登入則重新導向至 /lobby。
    """
    if 'user_id' in session:
        return redirect(url_for('room.lobby'))
    return render_template('index.html')

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """
    接收註冊表單。
    成功則建立使用者帳號並導向首頁，失敗則 flash 錯誤訊息。
    """
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        flash("請輸入帳號與密碼", 'error')
        return redirect(url_for('auth.index'))
        
    hashed_password = generate_password_hash(password)
    user_id = user_model.create({'username': username, 'password_hash': hashed_password})
    
    if user_id is None:
        flash("這組帳號已經有人使用囉！請嘗試別的名稱。", 'error')
        return redirect(url_for('auth.index'))
        
    flash("註冊成功！請直接登入。", 'success')
    return redirect(url_for('auth.index'))

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """
    接收登入表單。
    驗證通過後設定 session (例如 user_id) 並重導至 /lobby，失敗則 flash 錯誤訊息。
    """
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        flash("請輸入帳號與密碼", 'error')
        return redirect(url_for('auth.index'))
        
    user = user_model.get_by_username(username)
    
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        return redirect(url_for('room.lobby'))
    else:
        flash("帳號或密碼錯誤。", 'error')
        return redirect(url_for('auth.index'))

@auth_bp.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    """
    清除玩家連線 session，並重導向至首頁。
    """
    session.clear()
    flash("已成功登出。", 'info')
    return redirect(url_for('auth.index'))
