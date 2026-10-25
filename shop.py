import telebot
import json
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- НАСТРОЙКИ ---
BOT_TOKEN = "8953332376:AAHtfWpMyq9mMvYUyY99H6OdupFvi8jjSUg"
YOUR_ID = 7283034333 

bot = telebot.TeleBot(BOT_TOKEN)

# --- БАЗА ТОВАРОВ ---
PRODUCTS = {
    "rf": {"name": "РФ", "price": "310 руб."},
    "usa": {"name": "США", "price": "120 руб."},
    "pol": {"name": "Польша", "price": "210 руб."},
    "tha": {"name": "Таиланд", "price": "210 руб."},
    "fra": {"name": "Франция", "price": "230 руб."},
    "ind": {"name": "Индонезия", "price": "150 руб."},
    "jap": {"name": "Япония", "price": "370 руб."},
    "uk": {"name": "Великобритания", "price": "170 руб."},
    "ned": {"name": "Нидерланды", "price": "290 руб."},
    "chi": {"name": "Китай", "price": "290 руб."},
    "ban": {"name": "Бангладеш", "price": "150 руб."},
    "kaz": {"name": "Казахстан", "price": "230 руб."},
    "ger": {"name": "Германия", "price": "215 руб."},
    "bel": {"name": "Бельгия", "price": "350 руб."},
    "bra": {"name": "Бразилия", "price": "170 руб."},
    "ukr": {"name": "Украина", "price": "450 руб."},
    "chl": {"name": "Чили", "price": "130 руб."},
    "col": {"name": "Колумбия", "price": "110 руб."},
    "phi": {"name": "Филиппины", "price": "190 руб."},
    "ita": {"name": "Италия", "price": "260 руб."},
    "arg": {"name": "Аргентина", "price": "200 руб."},
    "est": {"name": "Эстония", "price": "210 руб."},
    "isr": {"name": "Израиль", "price": "180 руб."},
    "tkm": {"name": "Туркменистан", "price": "199 руб."},
    "tur": {"name": "Турция", "price": "230 руб."}
}

GIFTS = {
    "stars50": {"name": "⭐ 50 звезд", "price": "87 руб."},
    "stars100": {"name": "⭐ 100 звезд", "price": "167 руб."},
    "stars250": {"name": "⭐ 250 звезд", "price": "400 руб."},
    "stars500": {"name": "⭐ 500 звезд", "price": "800 руб."},
    "stars1000": {"name": "⭐ 1000 звезд", "price": "1600 руб."}
}

# --- ФУНКЦИИ ---
def load_accounts():
    if not os.path.exists('accounts.txt'): return []
    with open('accounts.txt', 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if not content: return []
        return [block.strip() for block in content.split('\n\n') if block.strip()]

def save_accounts(accs):
    with open('accounts.txt', 'w', encoding='utf-8') as f:
        for a in accs: f.write(a + '\n\n')

def load_purchases():
    if not os.path.exists('purchases.json'): return {}
    with open('purchases.json', 'r', encoding='utf-8') as f:
        try: return json.load(f)
        except: return {}

def save_purchases(data):
    with open('purchases.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- МЕНЮ ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💜 Оплата", callback_data="pay_info"))
    markup.row(InlineKeyboardButton("🟣 Аккаунты", callback_data="menu_accounts"), InlineKeyboardButton("🎁 Подарки/Звезды", callback_data="menu_gifts"))
    markup.row(InlineKeyboardButton("🟪 Поддержка", url="https://t.me/molly_0183"), InlineKeyboardButton("🛍 Мои покупки", callback_data="my_purchases"))
    
    text = f"👋 {message.from_user.first_name}, добро пожаловать в MOLLY SHOP!\n\n🟣 Лучший магазин аккаунтов и звезд.\n\n🛡 У нас только качественные товары!"
    
    try:
        with open('start_bg.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)
    except:
        bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    def safe_edit(text, reply_markup=None):
        try: bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=text, reply_markup=reply_markup)
        except:
            try: bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=reply_markup)
            except: pass

    if call.data == "pay_info":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад", callback_data="restart_menu"))
        safe_edit("💳 РЕКВИЗИТЫ ДЛЯ ОПЛАТЫ\n\nКарта: 2200 3961 2603 6132\n\n⚠️ После оплаты напишите @molly_0183 и скиньте чек.", markup)
        bot.answer_callback_query(call.id)

    elif call.data == "my_purchases":
        user_id = str(call.from_user.id)
        purchases = load_purchases()
        if user_id in purchases and purchases[user_id]:
            history = "\n\n".join([f"🔹 {p['name']}\n{p['account']}" for p in purchases[user_id]])
            try: bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            markup = InlineKeyboardMarkup().add(InlineKeyboardButton("⬅️ Назад в меню", callback_data="restart_menu"))
            bot.send_message(call.message.chat.id, f"🛍 Твои покупки:\n\n{history}", reply_markup=markup)
        else:
            bot.answer_callback_query(call.id, "У тебя пока нет покупок.", show_alert=True)

    elif call.data == "menu_accounts":
        markup = InlineKeyboardMarkup()
        items = list(PRODUCTS.items())
        for i in range(0, len(items), 2):
            row = []
            key1, prod1 = items[i]
            row.append(InlineKeyboardButton(f"{prod1['name']} - {prod1['price']}", callback_data=f"buy_{key1}"))
            if i + 1 < len(items):
                key2, prod2 = items[i+1]
                row.append(InlineKeyboardButton(f"{prod2['name']} - {prod2['price']}", callback_data=f"buy_{key2}"))
            markup.row(*row)
        markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="restart_menu"))
        safe_edit("🛒 Выбери нужный аккаунт:", markup)

    elif call.data == "menu_gifts":
        markup = InlineKeyboardMarkup()
        items = list(GIFTS.items())
        for i in range(0, len(items), 2):
            row = []
            key1, prod1 = items[i]
            row.append(InlineKeyboardButton(f"{prod1['name']} - {prod1['price']}", callback_data=f"buygift_{key1}"))
            if i + 1 < len(items):
                key2, prod2 = items[i+1]
                row.append(InlineKeyboardButton(f"{prod2['name']} - {prod2['price']}", callback_data=f"buygift_{key2}"))
            markup.row(*row)
        markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="restart_menu"))
        safe_edit("🎁 Выбери подарок или звезды:", markup)

    elif call.data == "restart_menu":
         try: bot.delete_message(call.message.chat.id, call.message.message_id)
         except: pass
         markup = InlineKeyboardMarkup()
         markup.add(InlineKeyboardButton("💜 Оплата", callback_data="pay_info"))
         markup.row(InlineKeyboardButton("🟣 Аккаунты", callback_data="menu_accounts"), InlineKeyboardButton("🎁 Подарки/Звезды", callback_data="menu_gifts"))
         markup.row(InlineKeyboardButton("🟪 Поддержка", url="https://t.me/molly_0183"), InlineKeyboardButton("🛍 Мои покупки", callback_data="my_purchases"))
         text = f"👋 {call.from_user.first_name}, добро пожаловать в MOLLY SHOP!\n\n🟣 Лучший магазин аккаунтов и звезд.\n\n🛡 У нас только качественные товары!"
         try:
             with open('start_bg.jpg', 'rb') as photo: bot.send_photo(call.message.chat.id, photo, caption=text, reply_markup=markup)
         except: bot.send_message(call.message.chat.id, text, reply_markup=markup)

    elif call.data.startswith("buy_"):
        prod_key = call.data.split("_")[1]
        prod = PRODUCTS[prod_key]
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ Я оплатил", callback_data=f"paid_{prod_key}_{call.from_user.id}"))
        markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="menu_accounts"))
        safe_edit(f"{prod['name']}\n\n💰 К оплате: {prod['price']}\n💳 Реквизиты: 2200 3961 2603 6132\n\n⚠️ После оплаты нажми кнопку ниже.", markup)

    elif call.data.startswith("buygift_"):
        prod_key = call.data.split("_")[1]
        prod = GIFTS[prod_key]
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ Я оплатил", callback_data=f"paidgift_{prod_key}_{call.from_user.id}"))
        markup.add(InlineKeyboardButton("⬅️ Назад", callback_data="menu_gifts"))
        safe_edit(f"{prod['name']}\n\n💰 К оплате: {prod['price']}\n💳 Реквизиты: 2200 3961 2603 6132\n\n⚠️ После оплаты нажми кнопку ниже.", markup)

    elif call.data.startswith("paid_"):
        _, prod_key, user_id = call.data.split("_")
        prod = PRODUCTS[prod_key]
        admin_markup = InlineKeyboardMarkup().add(InlineKeyboardButton("✅ Выдать", callback_data=f"give_{prod_key}_{user_id}"))
        bot.send_message(YOUR_ID, f"🔔 ЗАКАЗ: {prod['name']} ({prod['price']})\nПокупатель: @{call.from_user.username} (ID: {user_id})", reply_markup=admin_markup)
        bot.answer_callback_query(call.id, "Ожидай товар.")
        safe_edit("⏳ Проверяем оплату...")

    elif call.data.startswith("paidgift_"):
        _, prod_key, user_id = call.data.split("_")
        prod = GIFTS[prod_key]
        admin_markup = InlineKeyboardMarkup().add(InlineKeyboardButton("✅ Выдать", callback_data=f"givegift_{prod_key}_{user_id}"))
        bot.send_message(YOUR_ID, f"🔔 ЗАКАЗ (Подарок): {prod['name']} ({prod['price']})\nПокупатель: @{call.from_user.username} (ID: {user_id})", reply_markup=admin_markup)
        bot.answer_callback_query(call.id, "Ожидай товар.")
        safe_edit("⏳ Проверяем оплату...")

    # --- УМНЫЙ ПОИСК СТРАНЫ ---
    elif call.data.startswith("give_"):
        _, prod_key, user_id = call.data.split("_")
        country_name = PRODUCTS[prod_key]['name']
        
        accounts = load_accounts()
        if not accounts:
            bot.answer_callback_query(call.id, "❌ В базе вообще нет аккаунтов!", show_alert=True)
            return

        target_index = -1
        for i, acc in enumerate(accounts):
            if country_name.lower() in acc.lower():
                target_index = i
                break
                
        if target_index == -1:
            bot.answer_callback_query(call.id, f"❌ Аккаунтов {country_name} нет в наличии!", show_alert=True)
            safe_edit(f"❌ ОШИБКА: Клиент просил {country_name}, но таких аккаунтов нет в файле accounts.txt!")
            return

        acc_data = accounts.pop(target_index)
        save_accounts(accounts)
        
        try:
            purchases = load_purchases()
            if user_id not in purchases: purchases[user_id] = []
            purchases[user_id].append({"name": country_name, "account": acc_data})
            save_purchases(purchases)
            bot.send_message(int(user_id), f"🎉 Оплата подтверждена!\n\nТвой товар:\n\n{acc_data}\n\nСпасибо за покупку в MOLLY SHOP!")
            safe_edit(f"✅ Товар ({country_name}) выдан!")
        except Exception as e:
            safe_edit(f"❌ Ошибка: {e}")

    elif call.data.startswith("givegift_"):
        _, prod_key, user_id = call.data.split("_")
        safe_edit(f"✅ Заказ на {GIFTS[prod_key]['name']} обработан!\n\nНапиши покупателю, чтобы он связался с @molly_0183.")
        purchases = load_purchases()
        if user_id not in purchases: purchases[user_id] = []
        purchases[user_id].append({"name": GIFTS[prod_key]['name'], "account": "Выдано вручную"})
        save_purchases(purchases)

if __name__ == '__main__':
    print("Магазин запущен...")
    bot.infinity_polling()
