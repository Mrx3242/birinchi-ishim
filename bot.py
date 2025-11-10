import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

TOKEN = '8110417760:AAENXu6mT0V4EDCenKhY2F_o7qc4XpQJ2pM'  # <<< bu yerga o'z bot tokeningizni yozing
WEBAPP_URL = "https://regal-moxie-819aa6.netlify.app/"  # Telegram Web App (index.html)
BACKEND_URL = "http://127.0.0.1:5000"  # Flask backend (localhost yoki hosting)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    phone_btn = KeyboardButton("📱 Telefon raqam yuborish", request_contact=True)
    markup.add(phone_btn)
    bot.send_message(message.chat.id, "Iltimos, telefon raqamingizni yuboring:", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    phone = message.contact.phone_number
    telegram_id = message.from_user.id

    # Backend'ga ro'yxatdan o'tkazish
    try:
        response = requests.post(f"{BACKEND_URL}/register", json={
            "telegram_id": str(telegram_id),
            "phone": phone
        })
        if response.status_code == 200:
            bot.send_message(message.chat.id, f"✅ Raqamingiz qabul qilindi: {phone}")
        else:
            bot.send_message(message.chat.id, "❌ Serverdan javob kelmadi.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Serverga ulanib bo‘lmadi:\n{e}")

    # Web App tugmasi chiqarish
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    web_btn = KeyboardButton("🛒 Magazinga kirish", web_app=WebAppInfo(WEBAPP_URL))
    markup.add(web_btn)
    bot.send_message(message.chat.id, "Endi magazinga kirishingiz mumkin:", reply_markup=markup)

bot.polling()
