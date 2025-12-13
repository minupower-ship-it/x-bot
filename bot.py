import tweepy
import os
import time

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

# 내 계정 ID 확인
MY_ID = api.me().id_str
replied_users = set()  # 유저당 1회만 전송

print("봇 실행중...")

while True:
    try:
        # 최근 20개 DM 가져오기
        dms = api.get_direct_messages(count=20)
        for dm in reversed(dms):
            sender = dm.message_create['sender_id']

            # 본인 제외 + 1회만 전송
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
