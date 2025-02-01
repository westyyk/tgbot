import telebot
import requests

token = '7351672676:AAGG4zdqm39WrpMn5brgqrU6IJAeXijfrWM'
bot = telebot.TeleBot(token)

users_data = {}

@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    bot.send_message(message.chat.id, 'Приветствую, пришлите свой API ключ и User ID')
    users_data[chat_id] = {'API_KEY': '', 'User_ID': ''}

@bot.message_handler(func=lambda message: True)
def save_api_user_id(message):
    chat_id = message.chat.id
    if chat_id in users_data and users_data[chat_id]['API_KEY'] == '':
        user_input = message.text.split()
        if len(user_input) == 2:
            users_data[chat_id]['API_KEY'] = user_input[0]
            users_data[chat_id]['User_ID'] = user_input[1]
            bot.reply_to(message, 'Ваш API ключ и User ID сохранены.')
            print(users_data)
        else:
            bot.reply_to(message, 'Отправьте два значения: API ключ и User ID.')

bot.polling(none_stop=True)
