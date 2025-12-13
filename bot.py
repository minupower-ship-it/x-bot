import tweepy
import time

# --- API 키 / 토큰 ---
API_KEY = "bT0MePTguMvAurdPxx37AzbVq"
API_SECRET = "qN42QJoglnR7Go5J1nGSTh23o9lCyFU3kbzEDhsvjgtXYMqEC0"
ACCESS_TOKEN = "1983673230792765441-zu5NopX4PI8Ar1PUCPdmWiSgiXTvPP"
ACCESS_TOKEN_SECRET = "3yHndFORNxhUTfVHwIE8ABPiMjcDe7vAVes5MEdb1GxLJ"

# --- 보낼 메시지 ---
MESSAGE = (
    "DM for more vids\n"
    "Video: https://files.catbox.moe/em10m4.mp4\n"
    "Telegram bot: http://t.me/obtkryptobot"
)

# --- Tweepy 클라이언트 생성 ---
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

me = client.get_me().data.id
last_dm_id = None
replied_users = set()  # 유저당 1회만 전송

print("봇 실행중...")

while True:
    dms = client.get_direct_messages()

    if dms.data:
        for dm in reversed(dms.data):
            sender = dm.sender_id

            # 본인 제외 + 1회만 전송
            if sender != me and sender not in replied_users:
                client.send_direct_message(
                    recipient_id=sender,
                    text=MESSAGE
                )
                replied_users.add(sender)
                print("DM 전송 완료:", sender)

            # 마지막 DM ID 갱신
            last_dm_id = dm.id

    time.sleep(10)  # 10초마다 확인
