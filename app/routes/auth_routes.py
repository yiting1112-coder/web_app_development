from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁與登入/註冊介面。
    若 session 中已登入則重新導向至 /lobby。
    """
    pass

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """
    接收註冊表單。
    成功則建立使用者帳號並導向首頁，失敗則 flash 錯誤訊息。
    """
    pass

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """
    接收登入表單。
    驗證通過後設定 session (例如 user_id) 並重導至 /lobby，失敗則 flash 錯誤訊息。
    """
    pass

@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    """
    清除玩家連線 session，並重導向至首頁。
    """
    pass
