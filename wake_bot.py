import os
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)
import subprocess

# разрешенные пользователи
ALLOWED_USERS = [452614431, 1328995399]

TOKEN = os.environ.get("WAKEBOT_TOKEN")
if not TOKEN:
    raise ValueError("Токен бота не задан! Создайте /root/.wakebot_env с WAKEBOT_TOKEN")

# список ПК
PCS = {
    "goozya": {
        "mac": "0A:E0:AF:DA:01:70",
        "iface": "br-lan",
    },
    "vlad": {
        "mac": "D8:5E:D3:E7:34:7E",
        "iface": "br-lan",
    },
}


def is_authorized(update):
    return update.effective_user.id in ALLOWED_USERS


def wake_pc(query, pc_key):
    # отправка WOL
    pc = PCS.get(pc_key)

    try:
        subprocess.run(["etherwake", "-b", "-i", pc["iface"], pc["mac"]])
        query.message.reply_text(f"💡 ПК {pc_key.upper()} ({pc['mac']}) пробуждён!")
    except Exception as e:
        query.message.reply_text(f"Ошибка: {e}")


def show_keyboard(update):
    keyboard = [["Goozya", "Vlad"]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, resize_keyboard=True, one_time_keyboard=False
    )
    update.message.reply_text("Выберите ПК для пробуждения:", reply_markup=reply_markup)


def start(update, _):
    if not is_authorized(update):
        update.message.reply_text("⛔ У тебя нет доступа к этой команде.")
        return
    text = update.message.text.lower()
    print(text)
    update.message.reply_text(text)
    if text in PCS:
        wake_pc(update, text)
    else:
        show_keyboard(update)


def text_handler(update, _):
    if not is_authorized(update):
        update.message.reply_text("⛔ У тебя нет доступа к боту.")
        return

    text = update.message.text.lower()  # приводим к нижнему регистру
    pcs_keys = [k.lower() for k in PCS.keys()]

    if text in pcs_keys:
        # если пользователь нажал кнопку или написал имя ПК
        # находим оригинальный ключ (чувствительный к регистру)
        pc_key = list(PCS.keys())[pcs_keys.index(text)]
        wake_pc(update, pc_key)
    else:
        # любой другой текст — показываем клавиатуру
        show_keyboard(update)


def button(update, _):
    query = update.callback_query
    query.answer()

    match query.data:
        case "wake_goozya":
            wake_pc(query, "goozya")
        case "wake_vlad":
            wake_pc(query, "vlad")


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
