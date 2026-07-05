import telebot
import time

TOKEN = "8963620239:AAGyAdS_joCSjh8izmH1cRdro9UFnltnIuI"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Б")

@bot.message_handler(func=lambda m: m.text and m.text.startswith(".clear"))
def clear(message):
    if message.chat.type not in ["group", "supergroup"]:
        return

    member = bot.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in ["administrator", "creator"]:
        bot.reply_to(message, "еще не дорос использовать эту команду")
        return

    args = message.text.split()
    if len(args) != 2:
        bot.reply_to(message, "Использование:\n.clear 20")
        return

    try:
        count = int(args[1])
    except ValueError:
        bot.reply_to(message, "надо число а не это говно")
        return

    if count < 1:
        return
    if count > 1000:
        count = 1000

    # удаляем команду
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception:
        pass

    deleted = 0
    start_id = message.message_id - 1

    for msg_id in range(start_id, start_id - count, -1):
        if msg_id < 1:
            break
        try:
            bot.delete_message(message.chat.id, msg_id)
            deleted += 1
            time.sleep(0.05)
        except Exception:
            pass

    # отправляем первое сообщение
    msg = bot.send_message(message.chat.id, f"Удалено сообщений: {deleted}")

    # таймер 3... 2... 1...
    for i in range(3, 0, -1):
        time.sleep(1)
        bot.edit_message_text(
            f"Удалено сообщений: {deleted}\n{i}...",
            message.chat.id,
            msg.message_id
        )

    time.sleep(1)
    bot.delete_message(message.chat.id, msg.message_id)

print("Бот запущен")
bot.infinity_polling(skip_pending=True)
