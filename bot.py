import logging
import os
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, ContextTypes, filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8645405976:AAHXPnGHmxb4eELxOvGB_lSqL_i0tB9q9Kc")
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "537748292")

ENTER_ADDRESS, ENTER_TIME, CHOOSE_PAYMENT, CONFIRM_ORDER = range(4)

MAIN_KEYBOARD = ReplyKeyboardMarkup([
    ["🥕 Овощи", "🍎 Фрукты", "🥛 Молочка", "🌾 Крупы"],
    ["🍞 Мука и хлеб", "🥜 Орехи", "🍪 Выпечка и сладости", "🌿 Специи"],
    ["🥤 Напитки", "🧴 Масло и жиры", "🍅 Соусы", "🫙 Консервы"],
    ["📦 Каталог", "🛒 Моя корзина", "📋 Мои заказы"],
], resize_keyboard=True, is_persistent=True)

def get_cart(context):
    if "cart" not in context.user_data:
        context.user_data["cart"] = {}
    return context.user_data["cart"]

def get_orders(context):
    if "orders" not in context.user_data:
        context.user_data["orders"] = []
    return context.user_data["orders"]

def cart_total(cart):
    return sum(item["price"] * item["qty"] for item in cart.values())

def format_cart(cart):
    if not cart:
        return "Корзина пуста."
    lines = [f"• {item['name']} × {item['qty']} шт. — {item['price'] * item['qty']} грн" for key, item in cart.items()]
    lines.append(f"\n💰 <b>Итого: {cart_total(cart)} грн</b>")
    return "\n".join(lines)

KEYBOARD_TO_CATEGORY = {
    "🥕 Овощи": "Овощи", "🍎 Фрукты": "Фрукты", "🥛 Молочка": "Молочка",
    "🌾 Крупы": "Крупы", "🍞 Мука и хлеб": "Мука и хлеб", "🥜 Орехи": "Орехи",
    "🍪 Выпечка и сладости": "Выпечка и сладости", "🌿 Специи": "Специи и приправы",
    "🥤 Напитки": "Напитки", "🧴 Масло и жиры": "Масло и жиры",
    "🍅 Соусы": "Соусы", "🫙 Консервы": "Консервы и консервация",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = (
        "Добро пожаловать в <b>Едамобиль от Арса</b>! 🚚\n\n"
        "Бесплатная доставка продуктов питания по всему Днепру по ценам ниже розничных. "
        "От 2000 грн — и свежие продукты уже завтра у вас дома.\n\n"
        "Экономьте время и деньги каждый день!"
    )
    inline_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 Открыть каталог", callback_data="show_catalog"),
         InlineKeyboardButton("🛒 Моя корзина", callback_data="show_cart")],
        [InlineKeyboardButton("📋 Мои заказы", callback_data="show_orders")],
        [InlineKeyboardButton("ℹ️ Инструкция", callback_data="info_bot"),
         InlineKeyboardButton("🏢 О компании", callback_data="info_company"),
         InlineKeyboardButton("📞 Контакты", callback_data="info_contacts")]
    ])
    await update.message.reply_text(welcome, reply_markup=MAIN_KEYBOARD, parse_mode="HTML")
    await update.message.reply_text("Выберите действие:", reply_markup=inline_kb)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome = (
        "Добро пожаловать в <b>Едамобиль от Арса</b>! 🚚\n\n"
        "Бесплатная доставка продуктов питания по всему Днепру по ценам ниже розничных. "
        "От 2000 грн — и свежие продукты уже завтра у вас дома.\n\n"
        "Экономьте время и деньги каждый день!"
    )
    inline_kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 Открыть каталог", callback_data="show_catalog"),
         InlineKeyboardButton("🛒 Моя корзина", callback_data="show_cart")],
        [InlineKeyboardButton("📋 Мои заказы", callback_data="show_orders")],
        [InlineKeyboardButton("ℹ️ Инструкция", callback_data="info_bot"),
         InlineKeyboardButton("🏢 О компании", callback_data="info_company"),
         InlineKeyboardButton("📞 Контакты", callback_data="info_contacts")]
    ])
    await update.message.reply_text(welcome, reply_markup=MAIN_KEYBOARD, parse_mode="HTML")
    await update.message.reply_text("Выберите действие:", reply_markup=inline_kb)

