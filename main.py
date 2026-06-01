import asyncio
import re
import random
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telebot.async_telebot import AsyncTeleBot

# =============== إعدادات API (أنت فقط تضعها مرة واحدة) ===============
API_ID = 30324289
API_HASH = "93e20ced9ed0fa7e7e903900c11633d6"
BOT_TOKEN = "8817608659:AAF8O-I58x-khZLq4AzY-OWTyfgPIcNEo1M"

# =============== جلسات المستخدمين ===============
user_sessions = {}
active_spams = {}

# =============== كلمات التكليش ===============
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

# =============== كلمات التسطير ===============
TASTEER_WORDS = [
    "القحاب", "يا اخو الشرموطه", "يا ابن الوسيعه", "يا ديوث", "يا ابن القحبه",
    "يا ابن المنيوكه", "يا ابن الزقتين", "يا ابن الشرموطه", "يا ابن الحماره",
    "يا خنيث", "يا اخو الشرموط", "الخنيث", "يا ابن الديوث", "يا ابن الزب",
    "يا ابن الوسيعه", "اصمل بنيك", "عار امك", "يا مخنث", "يا ابن الكس",
    "يا ابن الهايته", "يا حمار", "يا فحل اختك", "يا ابن السافله", "يا كس امك",
    "يا زب الكلب", "يا ابن المتناكه", "يا شرمطه", "يا عاهر", "يا ابن العرص",
    "يا نجس", "يا خول", "يا قواد", "يا منيوك", "يا ابن الحزانه", "يا وسخ", "يا جربان"
]

# =============== دوال تسجيل الدخول ===============
async def send_code(user_id, phone):
    client = TelegramClient(f"sessions/user_{user_id}", API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            user_sessions[user_id] = {"client": client, "phone": phone, "step": "waiting_code"}
            return True
        except Exception as e:
            return str(e)
    else:
        user_sessions[user_id] = {"client": client, "phone": phone, "step": "ready"}
        return True

async def verify_code(user_id, code):
    data = user_sessions.get(user_id)
    if not data or data["step"] != "waiting_code":
        return False
    
    client = data["client"]
    phone = data["phone"]
    
    try:
        await client.sign_in(phone, code)
        user_sessions[user_id]["step"] = "ready"
        return True
    except SessionPasswordNeededError:
        user_sessions[user_id]["step"] = "waiting_password"
        return "password_needed"
    except Exception as e:
        return str(e)

async def verify_password(user_id, password):
    data = user_sessions.get(user_id)
    if not data or data["step"] != "waiting_password":
        return False
    
    client = data["client"]
    try:
        await client.sign_in(password=password)
        user_sessions[user_id]["step"] = "ready"
        return True
    except Exception as e:
        return str(e)

def is_verified(user_id):
    return user_id in user_sessions and user_sessions[user_id].get("step") == "ready"

# =============== دوال الإرسال ===============
async def send_takleesh_messages(user_id, target, count, chat_id, bot):
    if user_id in active_spams:
        active_spams[user_id]["stop"] = False
    else:
        active_spams[user_id] = {"stop": False}
    
    client = user_sessions[user_id]["client"]
    
    for i in range(count):
        if active_spams[user_id]["stop"]:
            await bot.send_message(chat_id, "🛑 تم إيقاف التكليش.")
            break
        
        word = random.choice(TAKLEESH_WORDS)
        try:
            await client.send_message(target, word)
        except Exception as e:
            await bot.send_message(chat_id, f"❌ فشل الإرسال: {str(e)}")
            break
        
        await asyncio.sleep(1)
    
    await bot.send_message(chat_id, f"✅ تم إرسال {count} كليشة.")
    if user_id in active_spams:
        del active_spams[user_id]

async def send_tasteer_messages(user_id, target, delay, chat_id, bot):
    if user_id in active_spams:
        active_spams[user_id]["stop"] = False
    else:
        active_spams[user_id] = {"stop": False}
    
    client = user_sessions[user_id]["client"]
    
    for i in range(3):
        if active_spams[user_id]["stop"]:
            await bot.send_message(chat_id, "🛑 تم إيقاف التسطير.")
            break
        
        word = random.choice(TASTEER_WORDS)
        try:
            await client.send_message(target, word)
        except Exception as e:
            await bot.send_message(chat_id, f"❌ فشل الإرسال: {str(e)}")
            break
        
        await asyncio.sleep(delay)
    
    await bot.send_message(chat_id, "✅ تم الانتهاء من التسطير.")
    if user_id in active_spams:
        del active_spams[user_id]

# =============== بوت التحكم ===============
bot = AsyncTeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
async def start(message):
    user_id = message.from_user.id
    if is_verified(user_id):
        await bot.reply_to(message, "✅ أنت مسجل الدخول بالفعل.\nاستخدم:\n/takleesh - للتكليش\n/tasteer - للتسطير\n/stop - للإيقاف")
    else:
        await bot.reply_to(message, "🔐 مرحبًا بك في بوت فشار.\nأرسل رقم هاتفك مع رمز الدولة:\nمثال: +9647701234567")

@bot.message_handler(commands=['login'])
async def login(message):
    user_id = message.from_user.id
    if is_verified(user_id):
        await bot.reply_to(message, "✅ أنت مسجل بالفعل.")
        return
    
    await bot.reply_to(message, "📱 أرسل رقم هاتفك مع رمز الدولة:\nمثال: +9647701234567")

@bot.message_handler(func=lambda m: m.text and m.text.startswith('+') and len(m.text) >= 10)
async def handle_phone(message):
    user_id = message.from_user.id
    phone = message.text.strip()
    
    await bot.reply_to(message, "⏳ جاري إرسال كود التفعيل...")
    
    result = await send_code(user_id, phone)
    if result is True:
        await bot.reply_to(message, "✅ تم إرسال كود التفعيل إلى حسابك في تليجرام.\nأدخل الكود **بمسافات** بين كل رقم:\nمثال: 1 2 3 4 5")
    else:
        await bot.reply_to(message, f"❌ فشل الإرسال: {result}")

@bot.message_handler(func=lambda m: re.match(r'^\d(\s\d)+$', m.text))
async def handle_code(message):
    user_id = message.from_user.id
    code = message.text.strip().replace(" ", "")
    
    result = await verify_code(user_id, code)
    if result is True:
        await bot.reply_to(message, "✅ تم تسجيل الدخول بنجاح!\nالآن يمكنك استخدام:\n/takleesh - للتكليش\n/tasteer - للتسطير\n/stop - للإيقاف")
    elif result == "password_needed":
        await bot.reply_to(message, "🔐 حسابك مفعل بخطوتين. أرسل كلمة المرور:")
    else:
        await bot.reply_to(message, f"❌ كود غير صحيح: {result}\nاستخدم /login للمحاولة مجددًا")

@bot.message_handler(func=lambda m: user_sessions.get(m.from_user.id, {}).get("step") == "waiting_password")
async def handle_password(message):
    user_id = message.from_user.id
    password = message.text.strip()
    
    result = await verify_password(user_id, password)
    if result is True:
        await bot.reply_to(message, "✅ تم تسجيل الدخول بنجاح!\nاستخدم:\n/takleesh - للتكليش\n/tasteer - للتسطير\n/stop - للإيقاف")
    else:
        await bot.reply_to(message, f"❌ كلمة مرور خاطئة: {result}")

@bot.message_handler(commands=['takleesh'])
async def takleesh(message):
    user_id = message.from_user.id
    
    if not is_verified(user_id):
        await bot.reply_to(message, "❌ يجب تسجيل الدخول أولاً. استخدم /login")
        return
    
    if user_id in active_spams:
        await bot.reply_to(message, "⚠️ يوجد عملية نشطة. استخدم /stop أولاً")
        return
    
    await bot.reply_to(message, "✍️ أرسل معرف المستخدم المستهدف (@username أو ID):")
    bot.register_next_step_handler(message, get_target_takleesh)

async def get_target_takleesh(message):
    target = message.text.strip()
    user_id = message.from_user.id
    
    await bot.reply_to(message, "🔢 كم رسالة تريد إرسالها؟ (التطفية التلقائية)")
    bot.register_next_step_handler(message, lambda m: start_takleesh(m, target))

async def start_takleesh(message, target):
    user_id = message.from_user.id
    
    try:
        count = int(message.text.strip())
        if count < 1:
            raise ValueError
    except:
        await bot.reply_to(message, "❌ عدد غير صالح.")
        return
    
    await bot.reply_to(message, f"⚡ بدء إرسال {count} كليشة إلى {target}...")
    asyncio.create_task(send_takleesh_messages(user_id, target, count, message.chat.id, bot))

@bot.message_handler(commands=['tasteer'])
async def tasteer(message):
    user_id = message.from_user.id
    
    if not is_verified(user_id):
        await bot.reply_to(message, "❌ يجب تسجيل الدخول أولاً. استخدم /login")
        return
    
    if user_id in active_spams:
        await bot.reply_to(message, "⚠️ يوجد عملية نشطة. استخدم /stop أولاً")
        return
    
    await bot.reply_to(message, "🎯 أرسل معرف المستخدم المستهدف (@username أو ID):")
    bot.register_next_step_handler(message, get_target_tasteer)

async def get_target_tasteer(message):
    target = message.text.strip()
    user_id = message.from_user.id
    
    await bot.reply_to(message, "⏱️ السرعة بين كل سطر (بالثواني، مثال: 3):")
    bot.register_next_step_handler(message, lambda m: start_tasteer(m, target))

async def start_tasteer(message, target):
    user_id = message.from_user.id
    
    try:
        delay = float(message.text.strip())
        if delay < 0.5:
            raise ValueError
    except:
        await bot.reply_to(message, "❌ سرعة غير صالحة (أقل قيمة 0.5 ثانية).")
        return
    
    await bot.reply_to(message, f"🚀 سيتم إرسال 3 أسطر إلى {target} بفاصل {delay} ثانية.")
    asyncio.create_task(send_tasteer_messages(user_id, target, delay, message.chat.id, bot))

@bot.message_handler(commands=['stop'])
async def stop(message):
    user_id = message.from_user.id
    
    if user_id in active_spams:
        active_spams[user_id]["stop"] = True
        await bot.reply_to(message, "🛑 جاري إيقاف العملية...")
    else:
        await bot.reply_to(message, "⚠️ لا توجد عملية نشطة لإيقافها.")

# =============== تشغيل البوت ===============
async def main():
    print("🔥 SHΔDØW BOT with Telethon is running...")
    print("المستخدمون يسجلون دخول بحساباتهم الشخصية")
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(main())    "اذب تيزاب بكسمك", "ابول بحلكك", "افرش كسمك", "افلش كسمك بوكسات", "انيج رب ربك",
    "اخضع لجباتي الحاره", "استرجل", "اشكه لكسمك وعلي", "اخلي تمص جبتي", "اسد كس امك",
    "افترس طيزك", "اختك كحبتي", "اعجن عيورتي بكسمك", "ابن مصاصه عيورتي", "شو دتعال",
    "امد تيل بصرمك", "حدث", "ادحس رجلي بكس اختك", "اشنقك بلباس امك", "اله اشكه لحلكك",
    "احط عيورتي بطيزمك", "ابن سير النعال", "ابن كحباتي", "اخدر طيزختك", "اطشر مخك بعيري",
    "ابن زبوبتي", "احط العرك بكس امك", "اجب بلباس اختك", "ابن الحوله", "اصمل", "ولك فرخي",
    "اجنكل طيز اختك", "احط امك بطيزك", "اضربمك", "انيجمك فرنسي", "اخرمش طيزك", "ابن الدبل",
    "ارعن", "اكطع النعال على صرمك", "العب بوبجي بكسمك", "الفيمبوي", "اتنايج وي اهلك", "ادك كسمك"
]

# =============== كلمات التسطير ===============
TASTEER_WORDS = [
    "القحاب", "يا اخو الشرموطه", "يا ابن الوسيعه", "يا ديوث", "يا ابن القحبه",
    "يا ابن المنيوكه", "يا ابن الزقتين", "يا ابن الشرموطه", "يا ابن الحماره",
    "يا خنيث", "يا اخو الشرموط", "الخنيث", "يا ابن الديوث", "يا ابن الزب",
    "يا ابن الوسيعه", "اصمل بنيك", "عار امك", "يا مخنث", "يا ابن الكس",
    "يا ابن الهايته", "يا حمار", "يا فحل اختك", "يا ابن السافله", "يا كس امك",
    "يا زب الكلب", "يا ابن المتناكه", "يا شرمطه", "يا عاهر", "يا ابن العرص",
    "يا نجس", "يا خول", "يا قواد", "يا منيوك", "يا ابن الحزانه", "يا وسخ", "يا جربان"
]

# =============== دوال تسجيل الدخول ===============
async def send_code(user_id, phone):
    """إرسال كود التفعيل إلى رقم المستخدم"""
    client = TelegramClient(f"sessions/user_{user_id}", API_ID, API_HASH)
    await client.connect()
    
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            user_sessions[user_id] = {"client": client, "phone": phone, "step": "waiting_code"}
            return True
        except Exception as e:
            return str(e)
    else:
        user_sessions[user_id] = {"client": client, "phone": phone, "step": "ready"}
        return True

async def verify_code(user_id, code):
    """التحقق من الكود"""
    data = user_sessions.get(user_id)
    if not data or data["step"] != "waiting_code":
        return False
    
    client = data["client"]
    phone = data["phone"]
    
    try:
        await client.sign_in(phone, code)
        user_sessions[user_id]["step"] = "ready"
        return True
    except SessionPasswordNeededError:
        user_sessions[user_id]["step"] = "waiting_password"
        return "password_needed"
    except Exception as e:
        return str(e)

async def verify_password(user_id, password):
    """إذا كان الحساب مفعل بخطوتين"""
    data = user_sessions.get(user_id)
    if not data or data["step"] != "waiting_password":
        return False
    
    client = data["client"]
    try:
        await client.sign_in(password=password)
        user_sessions[user_id]["step"] = "ready"
        return True
    except Exception as e:
        return str(e)

def is_verified(user_id):
    return user_id in user_sessions and user_sessions[user_id].get("step") == "ready"

# =============== دوال الإرسال ===============
async def send_takleesh_messages(user_id, target, count, chat_id, bot):
    """إرسال كلايش بعدد محدد"""
    if user_id in active_spams:
        active_spams[user_id]["stop"] = False
    else:
        active_spams[user_id] = {"stop": False}
    
    client = user_sessions[user_id]["client"]
    
    for i in range(count):
        if active_spams[user_id]["stop"]:
            await bot.send_message(chat_id, "🛑 تم إيقاف التكليش.")
            break
        
        word = random.choice(TAKLEESH_WORDS)
        try:
            await client.send_message(target, word)
        except Exception as e:
            await bot.send_message(chat_id, f"❌ فشل الإرسال: {str(e)}")
            break
        
        await asyncio.sleep(1)
    
    await bot.send_message(chat_id, f"✅ تم إرسال {count} كليشة.")
    if user_id in active_spams:
        del active_spams[user_id]

async def send_tasteer_messages(user_id, target, delay, chat_id, bot):
    """إرسال 3 أسطر بسرعة محددة"""
    if user_id in active_spams:
        active_spams[user_id]["stop"] = False
    else:
        active_spams[user_id] = {"stop": False}
    
    client = user_sessions[user_id]["client"]
    
    for i in range(3):
        if active_spams[user_id]["stop"]:
            await bot.send_message(chat_id, "🛑 تم إيقاف التسطير.")
            break
        
        word = random.choice(TASTEER_WORDS)
        try:
            await client.send_message(target, word)
        except Exception as e:
            await bot.send_message(chat_id, f"❌ فشل الإرسال: {str(e)}")
            break
        
        await asyncio.sleep(delay)
    
    await bot.send_message(chat_id, "✅ تم الانتهاء من التسطير.")
    if user_id in active_spams:
        del active_spams[user_id]

# =============== بوت التحكم (باستخدام asyncio) ===============
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
async def start(message):
    user_id = message.from_user.id
    if is_verified(user_id):
        await bot.reply_to(message, "✅ أنت مسجل الدخول بالفعل.\nاستخدم:\n/takleesh - للتكليش\n/tasteer - للتسطير\n/stop - للإيقاف")
    else:
        await bot.reply_to(message, "🔐 مرحبًا بك في بوت فشار.\nأرسل رقم هاتفك مع رمز الدولة:\nمثال: +9647701234567")

@bot.message_handler(commands=['login'])
async def login(message):
    user_id = message.from_user.id
    if is_verified(user_id):
        await bot.reply_to(message, "✅ أنت مسجل بالفعل.")
        return
    
    await bot.reply_to(message, "📱 أرسل رقم هاتفك مع رمز الدولة:\nمثال: +9647701234567")

@bot.message_handler(func=lambda m: m.text and m.text.startswith('+') and len(m.text) >= 10)
async def handle_phone(message):
    user_id = message.from_user.id
    phone = message.text.strip()
    
    await bot.reply_to(message, "⏳ جاري إرسال كود التفعيل...")
    
    result = await send_code(user_id, phone)
    if result is True:
        await bot.reply_to(message, "✅ تم إرسال كود التفعيل إلى حسابك في تليجرام.\nأدخل الكود **بمسافات** بين كل رقم:\nمثال: 1 2 3 4 5")
    else:
        await bot.reply_to(message, f"❌ فشل الإرسال: {result}")

@bot.message_handler(func=lambda m: re.match(r'^\d(\s\d)+$', m.text))
async def handle_code(message):
    user_id = message.from_user.id
    code = message.text.strip().replace(" ", "")
    
    result = await verify_code(user_id, code)
    if result is True:
        await bot.reply_to(message, "✅ تم تسجيل الدخول بنجاح!\nالآن يمكنك استخدام:\n/takleesh - للتكليش\n/tasteer - للتسطير\n/stop - للإيقاف")
    elif result == "password_needed":
        await bot.reply_to(message, "🔐 حسابك مفعل بخطوتين. أرسل كلمة المرور:")
    else:
        await bot.reply_to(message, f"❌ كود غير صحيح: {result}\nاستخدم /login للمحاولة مجددًا")

@bot.message_handler(func=lambda m: user_sessions.get(m.from_user.id, {}).get("step") == "waiting_password")
async def handle_password(message):
    user_id = message.from_user.id
    password = message.text.strip()
    
    result = await verify_password(user_id, password)
    if result is True:
        await bot.reply_to(message, "✅ تم تسجيل الدخول بنجاح!\nاستخدم:\n/takleesh - للتكليش\n/tasteer - للتسطير\n/stop - للإيقاف")
    else:
        await bot.reply_to(message, f"❌ كلمة مرور خاطئة: {result}")

@bot.message_handler(commands=['takleesh'])
async def takleesh(message):
    user_id = message.from_user.id
    
    if not is_verified(user_id):
        await bot.reply_to(message, "❌ يجب تسجيل الدخول أولاً. استخدم /login")
        return
    
    if user_id in active_spams:
        await bot.reply_to(message, "⚠️ يوجد عملية نشطة. استخدم /stop أولاً")
        return
    
    await bot.reply_to(message, "✍️ أرسل معرف المستخدم المستهدف (@username أو ID):")
    bot.register_next_step_handler(message, get_target_takleesh)

async def get_target_takleesh(message):
    target = message.text.strip()
    user_id = message.from_user.id
    
    await bot.reply_to(message, "🔢 كم رسالة تريد إرسالها؟ (التطفية التلقائية)")
    bot.register_next_step_handler(message, lambda m: start_takleesh(m, target))

async def start_takleesh(message, target):
    user_id = message.from_user.id
    
    try:
        count = int(message.text.strip())
        if count < 1:
            raise ValueError
    except:
        await bot.reply_to(message, "❌ عدد غير صالح.")
        return
    
    await bot.reply_to(message, f"⚡ بدء إرسال {count} كليشة إلى {target}...")
    
    asyncio.create_task(send_takleesh_messages(user_id, target, count, message.chat.id, bot))

@bot.message_handler(commands=['tasteer'])
async def tasteer(message):
    user_id = message.from_user.id
    
    if not is_verified(user_id):
        await bot.reply_to(message, "❌ يجب تسجيل الدخول أولاً. استخدم /login")
        return
    
    if user_id in active_spams:
        await bot.reply_to(message, "⚠️ يوجد عملية نشطة. استخدم /stop أولاً")
        return
    
    await bot.reply_to(message, "🎯 أرسل معرف المستخدم المستهدف (@username أو ID):")
    bot.register_next_step_handler(message, get_target_tasteer)

async def get_target_tasteer(message):
    target = message.text.strip()
    user_id = message.from_user.id
    
    await bot.reply_to(message, "⏱️ السرعة بين كل سطر (بالثواني، مثال: 3):")
    bot.register_next_step_handler(message, lambda m: start_tasteer(m, target))

async def start_tasteer(message, target):
    user_id = message.from_user.id
    
    try:
        delay = float(message.text.strip())
        if delay < 0.5:
            raise ValueError
    except:
        await bot.reply_to(message, "❌ سرعة غير صالحة (أقل قيمة 0.5 ثانية).")
        return
    
    await bot.reply_to(message, f"🚀 سيتم إرسال 3 أسطر إلى {target} بفاصل {delay} ثانية.")
    
    asyncio.create_task(send_tasteer_messages(user_id, target, delay, message.chat.id, bot))

@bot.message_handler(commands=['stop'])
async def stop(message):
    user_id = message.from_user.id
    
    if user_id in active_spams:
        active_spams[user_id]["stop"] = True
        await bot.reply_to(message, "🛑 جاري إيقاف العملية...")
    else:
        await bot.reply_to(message, "⚠️ لا توجد عملية نشطة لإيقافها.")

# =============== تشغيل البوت ===============
async def main():
    print("🔥 SHΔDØW BOT with Telethon is running...")
    print("المستخدمون يسجلون دخول بحساباتهم الشخصية")
    await bot.polling()

if __name__ == "__main__":
    asyncio.run(main())    "اخضع لجباتي الحاره", "استرجل", "اشكه لكسمك وعلي", "اخلي تمص جبتي", "اسد كس امك",
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
