import requests
import telebot
from telebot import types
import time

token = '7351672676:AAGG4zdqm39WrpMn5brgqrU6IJAeXijfrWM'
bot = telebot.TeleBot(token)

subscribers = {}
unsubscribe_mode = {}
subscribe_mode = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.KeyboardButton('Подписаться на игру')
    unsubscribe_button = types.KeyboardButton('Отписаться от игры')
    my_subscriptions_button = types.KeyboardButton('Мои подписки')
    markup.add(subscribe_button, unsubscribe_button, my_subscriptions_button)
    bot.reply_to(message, 'Приветствую! Напиши название игры, чтобы узнать ее цену в рублях. (Название нужно писать 1:1 как указано в Steam)\nНапример: вы хотите найти игру PUBG: BATTLEGROUNDS, если вы будете писать PUBG или же pubg вам выдаст что игра не найдена.\nТакже и с играми со специальными знаками по типу: Train Sim World® 5, если вы не напишете ® в названии то игру не найдет.', reply_markup=markup)

def get_gameinfo(game_id: int):
    url = f"https://store.steampowered.com/api/appdetails?appids={game_id}&cc=RU&l=russian"
    response = requests.get(url)
    data = response.json()

    if str(game_id) in data and data[str(game_id)]['success']:
        game_data = data[str(game_id)]['data']
        normal_price = game_data.get('price_overview', {}).get('initial', 0)
        discounted_price = game_data.get('price_overview', {}).get('final', 0)
        
        if normal_price == 0 and discounted_price == 0:
            normal_price = "Бесплатная"
            discounted_price = "Бесплатная"
        elif normal_price == discounted_price:
            discounted_price = "В данный момент скидки не присутствует"

        description = game_data.get('short_description', 'Об этой игре отсутствует информация')
        image_url = game_data.get('header_image', '')

        return {
            'normal_price': normal_price if isinstance(normal_price, str) else normal_price / 100,
            'discounted_price': discounted_price if isinstance(discounted_price, str) else discounted_price / 100,
            'description': description,
            'image_url': image_url
        }
    return None

def searchgame(game_name: str):
    url = f"https://api.steampowered.com/ISteamApps/GetAppList/v2/"
    response = requests.get(url)
    data = response.json()

    found_games = []

    for game in data['applist']['apps']:
        if game_name.lower() == game['name'].lower():
            game_info = {
                'name': game['name'],
                'url': f"https://store.steampowered.com/app/{game['appid']}/"
            }
            game_details = get_gameinfo(game['appid'])
            if game_details:
                game_info.update(game_details)
            else:
                game_info['normal_price'] = "Нет информации о цене"
                game_info['discounted_price'] = "Нет информации о скидке"
                game_info['description'] = "Об этой игре отсутствует информация"
                game_info['image_url'] = ""

            found_games.append(game_info)
            break

    return found_games

@bot.message_handler(func=lambda message: True)
def gamemessage(message):
    game_name = message.text.strip()
    chat_id = message.chat.id

    if chat_id in unsubscribe_mode and unsubscribe_mode[chat_id]:
        unsubscribe_mode[chat_id] = False
        if chat_id in subscribers and game_name in subscribers[chat_id]:
            subscribers[chat_id].remove(game_name)
            bot.reply_to(message, f"Вы успешно отписались от обновлений игры {game_name}.")
        else:
            bot.reply_to(message, f"Вы не были подписаны на обновления игры {game_name}.")
    elif chat_id in subscribe_mode and subscribe_mode[chat_id]:
        subscribe_mode[chat_id] = False
        games = searchgame(game_name)
        if games:
            if chat_id not in subscribers:
                subscribers[chat_id] = []
            if game_name not in subscribers[chat_id]:
                subscribers[chat_id].append(game_name)
                bot.reply_to(message, f"Вы успешно подписались на обновления игры {game_name}.")
            else:
                bot.reply_to(message, f"Вы уже подписаны на обновления игры {game_name}.")
        else:
            response = "Игры не найдены.\n\nЕсли есть другие игры, которые вас интересуют, напишите их названия!"
            bot.reply_to(message, response)
    elif message.text == 'Подписаться на игру':
        subscribe_mode[chat_id] = True
        bot.reply_to(message, 'Напишите название игры, на которую хотите подписаться.')
    elif message.text == 'Отписаться от игры':
        unsubscribe_mode[chat_id] = True
        bot.reply_to(message, 'Напишите название игры, от которой хотите отписаться.')
    elif message.text == 'Мои подписки':
        if chat_id in subscribers and subscribers[chat_id]:
            response = "Ваши подписки на игры:\n"
            for game in subscribers[chat_id]:
                response += f"- {game}\n"
            bot.send_message(chat_id, response)
        else:
            bot.reply_to(message, 'У вас нет подписок на игры.')
    else:
        games = searchgame(game_name)
        if games:
            if len(games) == 1:
                response = "Найдена игра:\n"
            else:
                response = "Найдены игры:\n"
                
            for game in games:
                if game['discounted_price'] == "В данный момент скидки не присутствует":
                    response += f"{game['name']}:\nОбычная цена - {game['normal_price']} руб., В данный момент скидки на данную игру не присутствует.\n"
                elif game['normal_price'] == "Бесплатная":
                    response += f"{game['name']}:\nОбычная цена - Бесплатная.\n"
                else:
                    response += f"{game['name']}:\nОбычная цена - {game['normal_price']} руб., Цена со скидкой - {game['discounted_price']} руб.\n"
                response += f"Об этой игре: {game['description']}\nСсылка: {game['url']}\n\n"
                
                if game['image_url']:
                    bot.send_photo(chat_id, game['image_url'], response)
                else:
                    bot.send_message(chat_id, response)
            
            response = "Если есть другие игры, которые вас интересуют, напишите их названия!"
            bot.send_message(chat_id, response)
        else:
            response = "Игры не найдены.\n\nЕсли есть другие игры, которые вас интересуют, напишите их названия!"
            bot.reply_to(message, response)

def send_updates():
    while True:
        for subscriber in subscribers:
            for game in subscribers[subscriber]:
                game_details = searchgame(game)[0]
                response = (
                    f"Обновление для игры {game_details['name']}:\n"
                    f"Обычная цена: {game_details['normal_price']} руб.\n"
                    f"Цена со скидкой: {game_details['discounted_price']} руб.\n"
                    f"Описание: {game_details['description']}\n"
                    f"Ссылка: {game_details['url']}\n"
                )
                if game_details['image_url']:
                    bot.send_photo(subscriber, game_details['image_url'], response)
                else:
                    bot.send_message(subscriber, response)
        time.sleep(15)

if __name__ == '__main__':
    import threading
    update_thread = threading.Thread(target=send_updates)
    update_thread.start()
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка: {e}")
