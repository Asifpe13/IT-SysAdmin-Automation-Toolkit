import os
import requests
import time
import logging
from datetime import datetime


def load_env(filepath=".env"):
    """
    Lightweight .env loader (no external deps).
    קורא קובץ .env אם קיים ומכניס לערכי סביבה.
    """
    if not os.path.exists(filepath):
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())
    except Exception as e:
        print(f"[!] Failed loading .env: {e}")

# --- CONFIGURATION ---  # Basic settings / הגדרות בסיס
load_env()  # Load secrets from .env if present / טען סודות מ-.env אם קיים

TARGET_URL = os.environ.get("TARGET_URL", "https://www.instagram.com/")  # Target URL to monitor / האתר למעקב
CHECK_INTERVAL_SECONDS = int(os.environ.get("CHECK_INTERVAL_SECONDS", "60"))  # Check interval in seconds / מרווח בדיקה

# Telegram bot credentials (replace for org use) / פרטי הבוט (להחליף בערכי ארגון)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID") 

# Logging configuration (local file) / הגדרת לוג מקומי
logging.basicConfig(
    filename="uptime.log",
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def send_telegram_alert(message):
    """
    Send a Telegram alert via the official API.
    פונקציה ששולחת הודעה לטלגרם דרך ה-API הרשמי.
    """
    try:
        # Telegram API endpoint / הכתובת הרשמית של טלגרם
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        
        # Send request (POST) / שליחת בקשה (POST)
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("   [V] Telegram alert sent.")
            logging.info(f"Alert sent: {message}")
        else:
            print(f"   [X] Failed to send Telegram alert: {response.text}")
            
    except Exception as e:
        print(f"   [!] Connection Error with Telegram: {e}")

def check_website(url):
    """
    Check if site responds with HTTP 200.
    בודק אם האתר למעלה (מחזיר קוד 200).
    """
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except:
        return False

def main():
    # Warn if placeholders are still present / אזהרה אם הערכים לא הוזנו
    if TELEGRAM_BOT_TOKEN.startswith("YOUR_") or TELEGRAM_CHAT_ID.startswith("YOUR_"):
        print("[!] TELEGRAM_BOT_TOKEN/CHAT_ID not set. Update .env or env vars.")

    print(f"--- Telegram Monitor Started for: {TARGET_URL} ---")
    
    # Send a test message to verify bot connectivity / הודעת בדיקה לוודא שהבוט עובד
    send_telegram_alert(f"🚀 Monitoring started for {TARGET_URL}")
    
    is_server_down = False 

    while True:
        timestamp = datetime.now().strftime("%H:%M:%S")
        is_up = check_website(TARGET_URL)

        if is_up:
            print(f"[{timestamp}] Status: ONLINE")
            
            # אם האתר חזר מנפילה - שלח הודעת הרגעה
            if is_server_down:
                send_telegram_alert(f"✅ RECOVERY: {TARGET_URL} is back online!")
                is_server_down = False
        else:
            print(f"[{timestamp}] Status: DOWN !!!")
            
            # אם האתר נפל ועדיין לא שלחנו התראה - שלח עכשיו
            if not is_server_down:
                send_telegram_alert(f"🚨 CRITICAL ALERT: {TARGET_URL} is DOWN!")
                is_server_down = True

        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()