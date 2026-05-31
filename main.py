import telebot
import time
import random
import re
import threading
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# =============== التوكن ===============
BOT_TOKEN = "8817608659:AAF8O-I58x-khZLq4AzY-OWTyfgPIcNEo1M"
bot = telebot.TeleBot(BOT_TOKEN)

# =============== قاعدة بيانات مؤقتة ===============
users = {}  # {user_id: {"phone": "+964...", "verified": True/False, "temp_code": "12345"}}
active_spams = {}  # {user_id: {"thread": threading.Thread, "stop": bool}}

# =============== كلمات التكليش (لا نهائية) ===============
TAKLEESH_WORDS = [
    "لحلكك الهالبك طيزمك", "اشيلك بعيري", "عبالك اعوفك؟", "انيجمك علصدرك", "ابن الزانيه",
    "غير انت ابني", "مصمص عيورتي", "اهف اختك بطرف عيري", "اربطك بقياطين قندرتي",
    "اشيل ربك واركعه بلكاع", "ابن الكحبه الستشرافيه", "ابن المراهقه", "امصمص ديوس اختك",
    "ابن بلاعت العيرين", "احط الويسكي بكس اختك", "اتفل بصرمك", "اصابعي تفترسك",
    "ابعبص صريمك", "ابن المتبربكه", "ابن الاسحاقيه", "ابن الناسوخيه", "اطحن ضلوعك",
    "اكهرب طيزك", "احط قضيبي بكس امك", "ابن الانحطاطيه", "اسوي كسيسمك طشار",
    "اشكشك ديوسك", "اقتحم نسلك", "اشلع راس اختك", "اتناطح وي عنابه امك", "اطب بين زرورك",
    "ابن الهايته", "دشوف شراح اسوي", "ابن الانزلاقيه", "ابن جبتي الحاره", "ولك شبيك خفت",
    "ابن الشراميط", "ابن التحب عيورتي", "ادحس عيري بكسمك", "ادك كسمك", "ابن الكحبه الرومانيه",
    "ابن بلاعت العير", "اخدر امك", "اسوي طويزك وصلتين", "ابن ام العيوره", "اعوج ركبت امك",
    "ازورك وجهك بعيري", "اصعد على ضهرك", "اتسودن عليك", "اهينك بعيري", "اهف راس امك بل طاوه",
    "انكز على صريمك", "ابن عاشقه العير", "ابن الكحيبه", "اخضع العيري", "انزل لعنه عيري بكسمك",
    "انيج امك الكحبه", "امك احطها بعيري", "وين تكدر لعيري", "نياج اختك", "اني اجك امك بعيري",
    "ابن الربل", "اشك صريمك بلقندره", "انزل غضب الله بطيزك", "ابن الزنا", "امصمص نهود امك",
    "ربك اسمطه", "طيز ابن الطيز", "ولك تعال مصعيري", "اعبد زبي", "المخنث", "كليشتي بكسمك",
    "اصعق صريمك", "فحلمك اني", "اله البك طيزمك", "احط الدروب بطيزك", "ادحس الكعبه بطيزك",
    "ابن القندره", "اكعد وصمه لصرمك", "اطشر صريمك", "وعلي ماتكدرلي", "ادحس البنكه بصرمك",
    "انيج اختك البربوك", "افلشك تفليش", "اخلي عيري براسك", "دمبك العير", "ابن الفريخه",
    "اذب تيزاب بكسمك", "ابول بحلكك", "افرش كسمك", "افلش كسمك بوكسات", "انيج رب ربك",
    "اخضع لجباتي الحاره", "استرجل", "اشكه لكسمك وعلي", "اخلي تمص جبتي", "اسد كس امك",
    "افترس طيزك", "اختك كحبتي", "اعجن عيورتي بكسمك", "ابن مصاصه عيورتي", "شو دتعال",
    "امد تيل بصرمك", "حدث", "ادحس رجلي بكس اختك", "اشنقك بلباس امك", "اله اشكه لحلكك",
    "احط عيورتي بطيزمك", "ابن سير النعال", "ابن كحباتي", "اخدر طيزختك", "اطشر مخك بعيري",
    "ابن زبوبتي", "احط العرك بكس امك", "اجب بلباس اختك", "ابن الحوله", "اصمل", "ولك فرخي",
    "اجنكل طيز اختك", "احط امك بطيزك", "اضربمك", "انيجمك فرنسي", "اخرمش طيزك", "ابن الدبل",
    "ارعن", "اكطع النعال على صرمك", "العب بوبجي بكسمك", "الفيمبوي", "اتنايج وي اهلك", "ادك كسمك"
]

# =============== كلمات التسطير (لا نهائية) ===============
TASTEER_WORDS = [
    "القحاب", "يا اخو الشرموطه", "يا ابن الوسيعه", "يا ديوث", "يا ابن القحبه",
    "يا ابن المنيوكه", "يا ابن الزقتين", "يا ابن الشرموطه", "يا ابن الحماره",
    "يا خنيث", "يا اخو الشرموط", "الخنيث", "يا ابن الديوث", "يا ابن الزب",
    "يا ابن الوسيعه", "اصمل بنيك", "عار امك", "يا مخنث", "يا ابن الكس",
    "يا ابن الهايته", "يا حمار", "يا فحل اختك", "يا ابن السافله", "يا كس امك",
    "يا زب الكلب", "يا ابن المتناكه", "يا شرمطه", "يا عاهر", "يا ابن العرص",
    "يا نجس", "يا خول", "يا قواد", "يا منيوك", "يا ابن الحزانه", "يا وسخ", "يا جربان"
]

# =============== دوال مساعدة ===============
def generate_otp():
    return str(random.randint(10000, 99999))

def stop_spam(user_id):
    if user_id in active_spams:
        active_spams[user_id]["stop"] = True
        del active_spams[user_id]

# =============== أمر البدء ===============
@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    if user_id in users and users[user_id].get("verified"):
        bot.reply_to(message, "✅ أنت مسجل الدخول بالفعل.\nاستخدم:\n/takleesh - للتكليش\n/tasteer - للتسطير\n/stop - للإيقاف")
    else:
        bot.reply_to(message, "🔐 مرحبًا بك في بوت فشار.\nالرجاء تسجيل الدخول عبر الأمر التالي:\n\n/login")

# =============== أمر تسجيل الدخول ===============
@bot.message_handler(commands=['login'])
def login(message):
    user_id = str(message.from_user.id)
    if user_id in users and users[user_id].get("verified"):
        bot.reply_to(message, "✅ أنت مسجل بالفعل.")
        return
    
    msg = bot.reply_to(message, "📱 أرسل رقم هاتفك مع رمز الدولة\nمثال: +9647701234567")
    bot.register_next_step_handler(msg, process_phone)

def process_phone(message):
    user_id = str(message.from_user.id)
    phone = message.text.strip()
    
    if not re.match(r'^\+\d{7,15}$', phone):
        bot.reply_to(message, "❌ رقم غير صالح. استخدم الصيغة الدولية مع +\nمثال: +9647701234567\nاستخدم /login للمحاولة مجددًا")
        return
    
    code = generate_otp()
    users[user_id] = {"phone": phone, "verified": False, "temp_code": code}
    
    # 🔻 وضع تجريبي (يعرض الكود في البوت بدلاً من SMS)
    bot.reply_to(message, f"🧪 [وضع تجريبي] كود التفعيل الخاص بك: {code}\nأدخل الكود **بمسافات** بين كل رقم:\nمثال: {code[0]} {code[1]} {code[2]} {code[3]} {code[4]}")
    
    msg = bot.reply_to(message, "✍️ أدخل الكود الآن بمسافات بين الأرقام:")
    bot.register_next_step_handler(msg, verify_code)

def verify_code(message):
    user_id = str(message.from_user.id)
    entered = message.text.strip().replace(" ", "")
    stored_code = users.get(user_id, {}).get("temp_code")
    
    if entered == stored_code:
        users[user_id]["verified"] = True
        users[user_id]["temp_code"] = None
        bot.reply_to(message, "✅ تم تسجيل الدخول بنجاح!\nالآن يمكنك استخدام:\n/takleesh - للتكليش\n/tasteer - للتسطير\n/stop - للإيقاف")
    else:
        bot.reply_to(message, "❌ كود غير صحيح. استخدم /login للمحاولة مجددًا")
        if user_id in users:
            del users[user_id]

# =============== أمر التكليش ===============
@bot.message_handler(commands=['takleesh'])
def takleesh(message):
    user_id = str(message.from_user.id)
    if user_id not in users or not users[user_id].get("verified"):
        bot.reply_to(message, "❌ يجب تسجيل الدخول أولاً. استخدم /login")
        return
    
    stop_spam(user_id)
    msg = bot.reply_to(message, "✍️ أرسل معرف المستخدم المستهدف (@username أو ID):")
    bot.register_next_step_handler(msg, get_target_for_takleesh)

def get_target_for_takleesh(message):
    user_id = str(message.from_user.id)
    target = message.text.strip()
    
    msg = bot.reply_to(message, "🔢 كم رسالة تريد إرسالها؟ (التطفية التلقائية)")
    bot.register_next_step_handler(msg, lambda m: start_takleesh(m, target))

def start_takleesh(message, target):
    user_id = str(message.from_user.id)
    try:
        count = int(message.text.strip())
        if count < 1:
            raise ValueError
    except:
        bot.reply_to(message, "❌ عدد غير صالح.")
        return
    
    bot.reply_to(message, f"⚡ بدء إرسال {count} كليشة إلى {target}...")
    
    stop_flag = {"stop": False}
    active_spams[user_id] = {"stop_flag": stop_flag}
    
    def send_messages():
        for i in range(count):
            if stop_flag["stop"]:
                break
            word = random.choice(TAKLEESH_WORDS)
            try:
                bot.send_message(target, word)
            except:
                bot.send_message(message.chat.id, f"❌ فشل الإرسال إلى {target}")
                break
            time.sleep(1)
        bot.send_message(message.chat.id, f"✅ تم إرسال {count} كليشة.")
        if user_id in active_spams:
            del active_spams[user_id]
    
    thread = threading.Thread(target=send_messages)
    thread.start()
    active_spams[user_id]["thread"] = thread

# =============== أمر التسطير ===============
@bot.message_handler(commands=['tasteer'])
def tasteer(message):
    user_id = str(message.from_user.id)
    if user_id not in users or not users[user_id].get("verified"):
        bot.reply_to(message, "❌ يجب تسجيل الدخول أولاً. استخدم /login")
        return
    
    stop_spam(user_id)
    msg = bot.reply_to(message, "🎯 أرسل معرف المستخدم المستهدف (@username أو ID):")
    bot.register_next_step_handler(msg, get_target_for_tasteer)

def get_target_for_tasteer(message):
    target = message.text.strip()
    msg = bot.reply_to(message, "⏱️ السرعة بين كل سطر (بالثواني، مثال: 3):")
    bot.register_next_step_handler(msg, lambda m: start_tasteer(m, target))

def start_tasteer(message, target):
    user_id = str(message.from_user.id)
    try:
        delay = float(message.text.strip())
        if delay < 0.5:
            raise ValueError
    except:
        bot.reply_to(message, "❌ سرعة غير صالحة (أقل قيمة 0.5 ثانية).")
        return
    
    bot.reply_to(message, f"🚀 سيتم إرسال 3 أسطر إلى {target} بفاصل {delay} ثانية.")
    
    stop_flag = {"stop": False}
    active_spams[user_id] = {"stop_flag": stop_flag}
    
    def send_lines():
        for i in range(3):
            if stop_flag["stop"]:
                break
            insult = random.choice(TASTEER_WORDS)
            try:
                bot.send_message(target, insult)
            except:
                bot.send_message(message.chat.id, f"❌ فشل الإرسال إلى {target}")
                break
            time.sleep(delay)
        bot.send_message(message.chat.id, "✅ تم الانتهاء من التسطير.")
        if user_id in active_spams:
            del active_spams[user_id]
    
    thread = threading.Thread(target=send_lines)
    thread.start()
    active_spams[user_id]["thread"] = thread

# =============== أمر الإيقاف ===============
@bot.message_handler(commands=['stop'])
def stop(message):
    user_id = str(message.from_user.id)
    if user_id in active_spams:
        active_spams[user_id]["stop_flag"]["stop"] = True
        del active_spams[user_id]
        bot.reply_to(message, "🛑 تم إيقاف التكليش/التسطير.")
    else:
        bot.reply_to(message, "⚠️ لا توجد عملية نشطة لإيقافها.")

# =============== تشغيل البوت ===============
if __name__ == "__main__":
    print("🔥 SHΔDØW BOT with Python is running...")
    bot.infinity_polling()
