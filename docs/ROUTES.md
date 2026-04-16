# 路由設計文件 (ROUTES)

本文件依據 PRD、ARCHITECTURE 與 DB_DESIGN 產出，定義 Flask 後端系統之路由規劃、API 設計與 Jinja2 網頁模板配置。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁/登入介面** | GET | `/` | `index.html` | 顯示系統首頁與登入註冊表單 |
| **用戶註冊** | POST | `/auth/register` | — | 接收註冊表單，寫入資料庫並重導向至登入頁 |
| **用戶登入** | POST | `/auth/login` | — | 接收登入表單，驗證通過後設定 session 並重導至大廳 |
| **登出** | POST | `/auth/logout` | — | 清除連線 session 並重導至首頁 |
| **遊戲大廳** | GET | `/lobby` | `lobby.html` | 顯示加入與建立房間的操作介面 |
| **建立房間** | POST | `/room/create` | — | 產生新房間並重導向至遊戲畫面 |
| **加入房間** | POST | `/room/join` | — | 驗證邀請碼後加入房間，重導向至遊戲畫面 |
| **遊戲主要畫面** | GET | `/game/<room_id>` | `board.html` | 渲染遊戲面板的初始佈局與玩家資訊 |
| **獲取遊戲狀態** | GET | `/game/<room_id>/state`| — (JSON) | 輪詢(Polling) API，取得最新的對局、資源與日誌狀態 |
| **玩家行動** | POST | `/game/<room_id>/action`| — (JSON) | 遊戲中打牌、建造等核心操作 |
| **發起/回應交易** | POST | `/game/<room_id>/trade`| — (JSON) | 送出交易請求或同意/拒絕交易請求 |
| **發送聊天訊息** | POST | `/game/<room_id>/chat` | — (JSON) | 在遊戲內發送對話 |
| **結束回合** | POST | `/game/<room_id>/end` | — (JSON) | 將操作權轉移給下一順位玩家 |

## 2. 每個路由的詳細說明

### `auth_routes` 模組

**1. 首頁/登入介面 (GET `/`)**
- 輸入：無
- 處理邏輯：檢查 session 中是否已有登入資訊，若有則直接重導至大廳。
- 輸出：渲染 `index.html`。

**2. 用戶註冊 (POST `/auth/register`)**
- 輸入：表單欄位 `username`, `password`。
- 處理邏輯：呼叫 `create_user()` 寫入 DB，雜湊密碼。若帳號重複則退回。
- 輸出：註冊成功重導到 `/` 或 `/lobby`；失敗則 flash 錯誤訊息。
- 錯誤處理：資料驗證失敗，或者帳號重複跳出錯誤提示。

**3. 用戶登入 (POST `/auth/login`)**
- 輸入：表單欄位 `username`, `password`。
- 處理邏輯：比對帳號密碼，成功後紀錄 `user_id` 至 session。
- 輸出：成功重導至 `/lobby`，失敗則 flash 錯誤訊息。

**4. 登出 (POST `/auth/logout`)**
- 輸入：無。
- 處理邏輯：清除 session 中的驗證資料。
- 輸出：重導向至 `/` 首頁。

### `room_routes` 模組

**5. 遊戲大廳 (GET `/lobby`)**
- 輸入：session 取 `user_id`。
- 處理邏輯：讀取玩家目前加入的房間供快速返回，渲染加入與建立按鈕。
- 輸出：渲染 `lobby.html`。
- 錯誤處理：若未登入則導向 `/` 並報錯 (HTTP 401/403)。

**6. 建立房間 (POST `/room/create`)**
- 輸入：session 取 `user_id`。
- 處理邏輯：隨機或固定產生邀請碼，呼叫 `create_room()` 並將自己加入玩家列表。
- 輸出：重導至 `/game/<room_id>`。

**7. 加入房間 (POST `/room/join`)**
- 輸入：表單欄位 `invite_code`。
- 處理邏輯：查詢房間 `get_room_by_invite_code()`，若有效且有空位則呼叫 `join_room()`。
- 輸出：重導至 `/game/<room_id>`。
- 錯誤處理：無效的邀請碼或錯誤發生，flash 錯誤訊息並停留在 `/lobby`。

### `game_routes` 模組

**8. 遊戲主要畫面 (GET `/game/<room_id>`)**
- 輸入：URL 參數 `room_id`，session 驗證。
- 處理邏輯：取得初次載入所需的靜態版面變數，嚴格檢查玩家是否在此房間名單內。
- 輸出：渲染 `board.html`。
- 錯誤處理：玩家若未加入遊戲房間中，拒絕存取並引導至大廳 (HTTP 403)。

**9. 獲取遊戲狀態 (GET `/game/<room_id>/state`)**
- 輸入：URL 參數 `room_id`。
- 處理邏輯：讀取資料庫獲得：玩家順位表、各資源、自己的手牌（過濾掉對手的暗牌）、日誌歷史、聊天對話與目前的交易請求狀態。
- 輸出：JSON 格式資料供前端畫面刷新。

**10. 玩家行動 (POST `/game/<room_id>/action`)**
- 輸入：JSON Payload `{"action_type": "...", "data": {...}}`。
- 處理邏輯：嚴密驗證當前是否為該玩家的回合。確認其資源餘額是否滿足操作所需。扣除資源、執行對應邏輯、最後存入 game logs。
- 輸出：JSON 回應成功與否 `{ "success": true }`。
- 錯誤處理：資源不足或非玩家回合回傳錯誤 (HTTP 400)。

**11. 發起/回應交易 (POST `/game/<room_id>/trade`)**
- 輸入：JSON Payload，若為建立新請求則傳入欲交換對價條件，若回應則傳入對應的 `trade_id` 與 `accept` 布林值。
- 處理邏輯：寫入或更新 `trade_requests`，並若成交則自動調配雙方資源，同時寫入 logs。
- 輸出：JSON `{ "success": true }`。

**12. 發送聊天訊息 (POST `/game/<room_id>/chat`)**
- 輸入：JSON Payload `{"message": "hi!"}`。
- 處理邏輯：限制字數與空值防護後，寫入 `chat_messages`。
- 輸出：JSON `{ "success": true }`。

**13. 結束回合 (POST `/game/<room_id>/end`)**
- 輸入：無額外參數。
- 處理邏輯：驗證為該玩家回合，把房間 `current_turn_user_id` 更新給列表中的順位下一位。
- 輸出：JSON `{ "success": true }`。

## 3. Jinja2 模板清單

這部分將於下一個前端階段（或實作時）建立於 `app/templates/` 中：

1. **`base.html`**
   - 角色：提供所有頁面的共通資源外框，包含網頁標題、Navbar、通用 CSS/JS 庫引用。實作 Flash errors 等訊息。
2. **`index.html`**
   - 角色：首頁與註冊/登入的整合畫面。
   - 繼承：無，或可自行繼承 `base.html` 實現。
3. **`lobby.html`**
   - 角色：供加入房間（輸入邀請碼）或建立房間介面使用。
   - 繼承：`{% extends "base.html" %}`
4. **`board.html`**
   - 角色：進入遊戲後的專用戰鬥面板。這裡可能不一定完全繼承 `base.html`，因為可能有固定比例的特殊排版、或是以滿版的地圖與卡牌槽配置為主。會專心加載 polling 專用的 Javascript 控制檔。

## 4. 路由骨架程式碼
各別放置於 `app/routes/` 的對應 Python 模組裡，為方便辨識分層設計。
