# -*- coding: utf-8 -*-
"""
Telegram bot (telebot / pyTelegramBotAPI asosida).
Funktsiyalar:
- /start → "📚 Darsni olish" tugmasi.
- "📚 Darsni olish" → inline tugmalar: "💳 Karta raqami", "✅ Check tashla", "📞 Obunachi telefon".
- "💳 Karta raqami" → karta raqamini chiqaradi.
- "✅ Check tashla" → foydalanuvchiga chek screenshot yuborish yo‘riqnomasi.
- "📞 Obunachi telefon" → obunachi telefon raqamini chiqaradi.
- Foydalanuvchi chek yuborsa → bot uni admin ga yuboradi.
- Admin tasdiqlash tugmasini bossа → bot foydalanuvchiga kanal havolasini yuboradi.
"""

import telebot
from telebot import types

# === Sozlamalar ===
BOT_TOKEN = "8314539881:AAFhhKnoNwwsjVk7sk4i7njGRonUcais2wI"
ADMIN_CHAT_ID = 32403212
ADMIN_USERNAME = "@Dilya9889"   
CARD_NUMBER = "9860 0101 2535 0164"
ADMIN_PHONE = "+998915539889"
SUBSCRIBER_PHONE = "+998915539889"
CHANNEL_LINK = "https://t.me/+fAzlw1mUiGFjMGYy"  # shu yerga kanal linkini qo'ying
# ===================

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Reply keyboard (asosiy menu)
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("📚 Darsni olish")) 
    return kb

# Inline keyboard (dars olish bo'limi)
def lessons_menu():
    ikb = types.InlineKeyboardMarkup()
    ikb.add(
        types.InlineKeyboardButton("💳 Karta raqami", callback_data="card"),
        types.InlineKeyboardButton("✅ Check tashla", callback_data="check"),
    )
    ikb.add(types.InlineKeyboardButton("📞 Obunachi telefon", callback_data="subscriber_phone"))
    return ikb

# Admin uchun inline keyboard
def approve_kb(user_id: int):
    ikb = types.InlineKeyboardMarkup()
    ikb.add(types.InlineKeyboardButton("✅ Tasdiqlash va link yuborish", callback_data=f"approve:{user_id}"))
    return ikb

# Start komandasi
@bot.message_handler(commands=["start"])
def start_cmd(message):
    text = (
        "Assalomu alaykum!\n\n"
        "📚 Darslarni olish uchun quyidagi tugmadan foydalaning.\n\n"
        f"Admin: <b>{ADMIN_USERNAME}</b>\n"
        f"☎️ Admin telefon: <code>{ADMIN_PHONE}</code>"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

# "📚 Darsni olish" tugmasi
@bot.message_handler(func=lambda m: m.text == "📚 Darsni olish")
def lessons_cmd(message):
    caption = (
        "Darsni olish uchun to‘lovni amalga oshiring va keyin <b>✅ Check tashla</b> tugmasini bosing.\n\n"
        f"Agar savollar bo‘lsa: {ADMIN_USERNAME}"
    )
    bot.send_message(message.chat.id, caption, reply_markup=lessons_menu())

# Inline tugmalar
@bot.callback_query_handler(func=lambda c: True)
def inline_callback(call):
    if call.data == "card":
        msg = f"💳 Karta raqami:Muminova Dilrabo\n<code>{CARD_NUMBER}</code>"
        bot.send_message(call.message.chat.id, msg)

    elif call.data == "check":
        msg = (
            "✅ <b>Check tashlash</b>\n\n"
            "To‘lov chek screenshotini ushbu botga yuboring.\n\n"
            f"Admin: <b>{ADMIN_USERNAME}</b>\n"
            f"☎️ Admin telefon: <code>{ADMIN_PHONE}</code>\n\n"
            "Admin tasdiqlagach, sizga kanal havolasi yuboriladi."
        )
        bot.send_message(call.message.chat.id, msg)

    elif call.data == "subscriber_phone":
        msg = f"📞 Obunachi telefon raqami: <code>{SUBSCRIBER_PHONE}</code>"
        bot.send_message(call.message.chat.id, msg)

    elif call.data.startswith("approve:"):
        if call.from_user.id != ADMIN_CHAT_ID:
            bot.answer_callback_query(call.id, "Faqat admin tasdiqlashi mumkin!", show_alert=True)
            return
        user_id = int(call.data.split(":")[1])
        txt = f"🎉 To‘lovingiz tasdiqlandi!\n\nKanal havolasi: {CHANNEL_LINK}"
        bot.send_message(user_id, txt)
        bot.send_message(call.message.chat.id, f"✅ Link yuborildi foydalanuvchiga: {user_id}")

# Chek screenshot qabul qilish
@bot.message_handler(content_types=["photo", "document"])
def handle_checks(message):
    user = message.from_user
    user_tag = f"@{user.username}" if user.username else f"id:{user.id}"
    caption = (
        "🧾 Yangi chek!\n\n"
        f"Foydalanuvchi: {user.first_name or ''} {user.last_name or ''} ({user_tag})\n"
        f"User ID: <code>{user.id}</code>\n\n"
        "Quyidagi tugma orqali tasdiqlashingiz mumkin."
    )

    if message.content_type == "photo":
        bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=caption, reply_markup=approve_kb(message.chat.id))
    else:
        bot.send_document(ADMIN_CHAT_ID, message.document.file_id, caption=caption, reply_markup=approve_kb(message.chat.id))

    bot.reply_to(message, "✅ Chek admin ga yuborildi. Tasdiqlanishini kuting.")

# Ishga tushirish
print("Bot ishlayapti...")
bot.infinity_polling()
# -*- coding: utf-8 -*-
"""
Telegram bot (telebot / pyTelegramBotAPI asosida).
Funktsiyalar:
- /start → "📚 Darsni olish" tugmasi.
- "📚 Darsni olish" → inline tugmalar: "💳 Karta raqami", "✅ Check tashla", "📞 Obunachi telefon".
- "💳 Karta raqami" → karta raqamini chiqaradi.
- "✅ Check tashla" → foydalanuvchiga chek screenshot yuborish yo‘riqnomasi.
- "📞 Obunachi telefon" → obunachi telefon raqamini chiqaradi.
- Foydalanuvchi chek yuborsa → bot uni admin ga yuboradi.
- Admin tasdiqlash tugmasini bossа → bot foydalanuvchiga kanal havolasini yuboradi.
"""

import telebot
from telebot import types

# === Sozlamalar ===
BOT_TOKEN = "8314539881:AAFhhKnoNwwsjVk7sk4i7njGRonUcais2wI"
ADMIN_CHAT_ID = 32403212
ADMIN_USERNAME = "@Dilya9889"   
CARD_NUMBER = "9860 0101 2535 0164"
ADMIN_PHONE = "+998915539889"
SUBSCRIBER_PHONE = "+998915539889"
CHANNEL_LINK = "https://t.me/+fAzlw1mUiGFjMGYy"  # shu yerga kanal linkini qo'ying
# ===================

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# Reply keyboard (asosiy menu)
def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("📚 Darsni olish")) 
    return kb

# Inline keyboard (dars olish bo'limi)
def lessons_menu():
    ikb = types.InlineKeyboardMarkup()
    ikb.add(
        types.InlineKeyboardButton("💳 Karta raqami", callback_data="card"),
        types.InlineKeyboardButton("✅ Check tashla", callback_data="check"),
    )
    ikb.add(types.InlineKeyboardButton("📞 Obunachi telefon", callback_data="subscriber_phone"))
    return ikb

# Admin uchun inline keyboard
def approve_kb(user_id: int):
    ikb = types.InlineKeyboardMarkup()
    ikb.add(types.InlineKeyboardButton("✅ Tasdiqlash va link yuborish", callback_data=f"approve:{user_id}"))
    return ikb

# Start komandasi
@bot.message_handler(commands=["start"])
def start_cmd(message):
    text = (
        "Assalomu alaykum!\n\n"
        "📚 Darslarni olish uchun quyidagi tugmadan foydalaning.\n\n"
        f"Admin: <b>{ADMIN_USERNAME}</b>\n"
        f"☎️ Admin telefon: <code>{ADMIN_PHONE}</code>"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

# "📚 Darsni olish" tugmasi
@bot.message_handler(func=lambda m: m.text == "📚 Darsni olish")
def lessons_cmd(message):
    caption = (
        "Darsni olish uchun to‘lovni amalga oshiring va keyin <b>✅ Check tashla</b> tugmasini bosing.\n\n"
        f"Agar savollar bo‘lsa: {ADMIN_USERNAME}"
    )
    bot.send_message(message.chat.id, caption, reply_markup=lessons_menu())

# Inline tugmalar
@bot.callback_query_handler(func=lambda c: True)
def inline_callback(call):
    if call.data == "card":
        msg = f"💳 Karta raqami:Muminova Dilrabo\n<code>{CARD_NUMBER}</code>"
        bot.send_message(call.message.chat.id, msg)

    elif call.data == "check":
        msg = (
            "✅ <b>Check tashlash</b>\n\n"
            "To‘lov chek screenshotini ushbu botga yuboring.\n\n"
            f"Admin: <b>{ADMIN_USERNAME}</b>\n"
            f"☎️ Admin telefon: <code>{ADMIN_PHONE}</code>\n\n"
            "Admin tasdiqlagach, sizga kanal havolasi yuboriladi."
        )
        bot.send_message(call.message.chat.id, msg)

    elif call.data == "subscriber_phone":
        msg = f"📞 Obunachi telefon raqami: <code>{SUBSCRIBER_PHONE}</code>"
        bot.send_message(call.message.chat.id, msg)

    elif call.data.startswith("approve:"):
        if call.from_user.id != ADMIN_CHAT_ID:
            bot.answer_callback_query(call.id, "Faqat admin tasdiqlashi mumkin!", show_alert=True)
            return
        user_id = int(call.data.split(":")[1])
        txt = f"🎉 To‘lovingiz tasdiqlandi!\n\nKanal havolasi: {CHANNEL_LINK}"
        bot.send_message(user_id, txt)
        bot.send_message(call.message.chat.id, f"✅ Link yuborildi foydalanuvchiga: {user_id}")

# Chek screenshot qabul qilish
@bot.message_handler(content_types=["photo", "document"])
def handle_checks(message):
    user = message.from_user
    user_tag = f"@{user.username}" if user.username else f"id:{user.id}"
    caption = (
        "🧾 Yangi chek!\n\n"
        f"Foydalanuvchi: {user.first_name or ''} {user.last_name or ''} ({user_tag})\n"
        f"User ID: <code>{user.id}</code>\n\n"
        "Quyidagi tugma orqali tasdiqlashingiz mumkin."
    )

    if message.content_type == "photo":
        bot.send_photo(ADMIN_CHAT_ID, message.photo[-1].file_id, caption=caption, reply_markup=approve_kb(message.chat.id))
    else:
        bot.send_document(ADMIN_CHAT_ID, message.document.file_id, caption=caption, reply_markup=approve_kb(message.chat.id))

    bot.reply_to(message, "✅ Chek admin ga yuborildi. Tasdiqlanishini kuting.")

# Ishga tushirish
print("Bot ishlayapti...")
bot.infinity_polling()
