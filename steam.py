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

@bot.message_handler(message=['get_sales'])
def get_sales(message):
    chat_id = message.chat.id
    if chat_id not in users_data:
        bot.reply_to(message, 'Сначала отправьте два значения: API ключ и User ID')
        return

    user_data = users_data[chat_id]
    API_KEY = user_data['API_KEY']
    User_ID = user_data['User_ID']

    sales = get_sales(API_KEY, User_ID)
    if sales:
        sale_message = "Вот текущие скидки Steam игр, на которые вы подписались.:\n\n"
        for sale in sales:
            sale_message += f"{sale['name']}: {sale['discount']}% off, now {sale['final_price']}\n"
        bot.reply_to(message, sale_message)
    else:
        bot.reply_to(message, 'Скидок не найдено')


bot.polling(none_stop=True)
