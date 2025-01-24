import telebot
token = '()'
bot = telebot.TeleBot(token)


@bot.message_handler(func=lambda message: True)
def respond_to_greeting(message):
    if message.text.lower() == '/start':
        bot.reply_to(message, "Привет! в каком регионе тебя интересует погода?")
    else:
        bot.reply_to(message, "Напишите '/start', чтобы начать.")


if __name__ == '__main__':
    bot.polling(none_stop=True)
