from flask import Flask, request
import requests
import os
import psycopg2
import urllib.parse as up

app = Flask(__name__)

# ===== 기본 설정 =====
TOKEN = os.environ.get("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{TOKEN}"

VIDEO_URL = "https://files.catbox.moe/dt49t2.mp4"

CAPTION = """

──────────────────────────────

Welcome to Private Collection

──────────────────────────────

• Only high quality handpicked content.

• Premium ★nlyFans Videos

• DECEMBER 2025: ★ ACTIVE ★

──────────────────────────────

★ Price: $20

★ INSTANT ACCESS ★

──────────────────────────────

"""

ADMIN_ID = 5619516265

CRYPTO_QR = "https://files.catbox.moe/fkxh5l.png"
CRYPTO_ADDRESS = "TERhALhVLZRqnS3mZGhE1XgxyLnKHfgBLi"

# ===== Render Postgres 연결 =====
DATABASE_URL = os.environ["DATABASE_URL"]

up.uses_netloc.append("postgres")
url = up.urlparse(DATABASE_URL)

conn = psycopg2.connect(
    dbname=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
conn.autocommit = True


def save_user(chat_id):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                chat_id BIGINT PRIMARY KEY
            )
        """)
        cur.execute("""
            INSERT INTO users (chat_id)
            VALUES (%s)
            ON CONFLICT (chat_id) DO NOTHING
        """, (chat_id,))


def get_user_count():
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM users")
        return cur.fetchone()[0]


# ===== Webhook =====
@app.route("/", methods=["GET", "POST", "HEAD"])
def main():
    if request.method == "HEAD":
        return "", 200

    if request.method == "GET":
        return "Bot is running"

    update = request.get_json()
    print("UPDATE:", update)

    if not update:
        return "ok"

    message = update.get("message") or update.get("edited_message")
    callback_query = update.get("callback_query")

    # ===== 일반 메시지 처리 =====
    if message:
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        print("MESSAGE:", chat_id, text)

        if text == "/start":
            save_user(chat_id)

            try:
                res = requests.post(
                    f"{API_URL}/sendVideo",
                    json={
                        "chat_id": chat_id,
                        "video": VIDEO_URL,
                        "caption": CAPTION
                    },
                    timeout=10
                )
                print("sendVideo:", res.status_code, res.text)

                keyboard = {
                    "inline_keyboard": [
                        [{"text": "💸 PayPal", "url": "https://www.paypal.com/paypalme/minwookim384/20usd"}],
                        [{"text": "💳 Stripe", "url": "https://buy.stripe.com/bJe8wR1oO1nq3sN7Y41ck00"}],
                        [{"text": "🪙 CRYPTO USDT(TRON)", "callback_data": "crypto"}],
                        [{"text": "❓ Proof here", "url": "https://t.me/MBRYPIE"}]
                    ]
                }

                res = requests.post(
                    f"{API_URL}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "PAYMENT METHOD\n\n💡 After payment, please send me a proof!",
                        "reply_markup": keyboard
                    },
                    timeout=10
                )
                print("sendMessage:", res.status_code, res.text)

            except Exception as e:
                print("ERROR sending /start messages:", e)

        elif text == "/users":
            if chat_id == ADMIN_ID:
                count = get_user_count()
                res = requests.post(
                    f"{API_URL}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": f"👥 총 유입 인원 수: {count}명"
                    },
                    timeout=10
                )
                print("users cmd:", res.status_code, res.text)
            else:
                requests.post(
                    f"{API_URL}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "❌ 관리자만 사용할 수 있습니다."
                    },
                    timeout=10
                )

    # ===== 버튼 클릭 처리 =====
    elif callback_query:
        chat_id = callback_query["from"]["id"]
        data = callback_query["data"]

        print("CALLBACK:", chat_id, data)

        if data == "crypto":
            try:
                res = requests.post(
                    f"{API_URL}/sendPhoto",
                    json={
                        "chat_id": chat_id,
                        "photo": CRYPTO_QR,
                        "caption": f"💡 CRYPTO USDT(TRON) Payment\n\nWallet Address:\n{CRYPTO_ADDRESS}"
                    },
                    timeout=10
                )
                print("sendPhoto:", res.status_code, res.text)

                proof_keyboard = {
                    "inline_keyboard": [
                        [{"text": "❓ Text here", "url": "https://t.me/MBRYPIE"}]
                    ]
                }

                res = requests.post(
                    f"{API_URL}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "💡 After payment, please text me XX",
                        "reply_markup": proof_keyboard
                    },
                    timeout=10
                )
                print("send proof msg:", res.status_code, res.text)

            except Exception as e:
                print("ERROR sending crypto info:", e)

    return "ok"


# ===== Render 실행 =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
