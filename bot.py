import tweepy
import os
import time
from flask import Flask
import threading

# --- 환경변수에서 API 키 불러오기 ---
API_KEY = os.environ["API_KEY"]
API_SECRET = os.environ["API_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

# --- 전송할 메시지 ---
MESSAGE = (
    "DM for more vids\n"
    "Video: https://files.catbox.moe/em10m4.mp4\n"
    "Telegram bot: http://t.me/obtkryptobot"
)

# --- Tweepy v1.1 인증 ---
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

MY_ID = api.verify_credentials().id_str
replied_users = set()

print("봇 실행중...")

# --- DM 자동응답 루프 ---
def run_bot():
    while True:
        try:
            dms = api.get_direct_messages(count=20)
            for dm in reversed(dms):
                sender = dm.message_create['sender_id']
                if sender != MY_ID and sender not in replied_users:
                    try:
                        api.send_direct_message(recipient_id=sender, text=MESSAGE)
                        replied_users.add(sender)
                        print("DM 전송 완료:", sender)
                    except Exception as e:
                        print("DM 전송 실패:", e)
            time.sleep(10)
        except Exception as e:
            print("DM 가져오기 실패:", e)
            time.sleep(30)

# --- Flask 서버 (포트 열기용, Web Service용) ---
app = Flask(__name__)

@app.route("/")
def index():
    return "Bot is running!"

# --- 백그라운드 스레드로 봇 실행 ---
threading.Thread(target=run_bot).start()

if __name__ == "__main__":
    # Google Cloud 또는 Render Web Service에서 PORT 환경변수 사용
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
