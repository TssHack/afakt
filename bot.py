from telethon import TelegramClient, events
import asyncio 
import os

api_id = int(os.getenv("TG_API_ID", "18377832"))
api_hash = os.getenv("TG_API_HASH", "ed8556c450c6d0fd68912423325dd09c")

channel_id = -1001906449648
target_user_id = 5700245077

client = TelegramClient('gift_watcher', api_id, api_hash)

client.on(events.NewMessage(chats=channel_id))
async def handler(event):
    message_text = event.raw_text
    if "هدیه مستر سرور" in message_text:
        try:
            await asyncio.sleep(2)  # تاخیر دو ثانیه‌ای
            user = await client.get_entity(target_user_id)
            await client.send_message(user, "هدیه مستر سرور")
            print("🎁 پیام هدیه با تاخیر ارسال شد.")
        except Exception as e:
            print(f"❌ خطا در ارسال پیام: {e}")

if __name__ == "__main__":
    try:
        client.start()
        print("✅ ربات اجرا شد و منتظر پیام‌هاست...")
        client.run_until_disconnected()
    except Exception as e:
        print(f"❌ خطا در اجرای ربات: {e}")
