from flask import Blueprint, request, jsonify, render_template, session

game_bp = Blueprint('game', __name__, url_prefix='/game')

@game_bp.route('/<int:room_id>', methods=['GET'])
def game_board(room_id):
    """
    渲染遊戲核心面板 (board.html)。
    驗證 session 使用者是否確實屬於此房間的遊戲名單，若否則回傳 403 並建議退回首頁。
    """
    return f"進入遊戲房間 {room_id} 的畫面準備開發中"

@game_bp.route('/<int:room_id>/state', methods=['GET'])
def get_game_state(room_id):
    """
    [Polling API]
    前端輪詢取得最新的回合狀態、資源清單、玩家手牌、資源交易與遊戲日誌。
    只回傳當前玩家有權限知道的資料（避免暗牌與別人的牌外洩）。
    """
    pass

@game_bp.route('/<int:room_id>/action', methods=['POST'])
def perform_action(room_id):
    """
    [Game Logic API]
    接收玩家操作 (如消耗資源升級、抽牌)。
    驗證是否輪到該玩家的回合、資源是否充足，通過後修改對應 DB 並記錄至 game_logs。
    """
    pass

@game_bp.route('/<int:room_id>/trade', methods=['POST'])
def process_trade(room_id):
    """
    [Game Logic API]
    處理交換資源邏輯，可發文建立新的 trade_request，或接受/拒絕別人的交易請求。
    """
    pass

@game_bp.route('/<int:room_id>/chat', methods=['POST'])
def send_chat(room_id):
    """
    [Game Logic API]
    接收文字對話並存入 chat_messages 資料表，供後續狀態同步。
    """
    pass

@game_bp.route('/<int:room_id>/end', methods=['POST'])
def end_turn(room_id):
    """
    [Game Logic API]
    結束當前回合，換給房間排序中下一位的人，同時記錄更迭動作。
    """
    pass
