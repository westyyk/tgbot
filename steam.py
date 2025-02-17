import requests
import telebot
from telebot import types
import time
import json
import os
import threading
import traceback

token = '7351672676:AAGG4zdqm39WrpMn5brgqrU6IJAeXijfrWM'  #Замените тут на ваш токен бота (если требуется)
bot = telebot.TeleBot(token)

subscriptions_file = os.path.join(os.path.expanduser("~"), "Desktop", "tgbot-main", "subscriptions.json")

os.makedirs(os.path.dirname(subscriptions_file), exist_ok=True)

subscribers = {}

def load_subscriptions():
    global subscribers 
    try:
        with open(subscriptions_file, 'r', encoding='utf-8') as file:
            subscribers = json.load(file)
        print("Подписки успешно загружены из файла.")
    except FileNotFoundError:
        print("Файл подписок не найден. Будет создан новый.")
        subscribers = {}  
        save_subscriptions() 
    except json.JSONDecodeError:
        print("Ошибка при декодировании JSON. Файл подписок поврежден или пуст.")
        subscribers = {}  
    except Exception as e:
        print(f"Произошла ошибка при загрузке подписок: {e}")
        
        traceback.print_exc() 


def save_subscriptions():
    try:
        with open(subscriptions_file, 'w', encoding='utf-8') as file:
            json.dump(subscribers, file, ensure_ascii=False, indent=4)
        print("Подписки успешно сохранены в файл.")
    except Exception as e:
        print(f"Произошла ошибка при сохранении подписок: {e}")
       
        traceback.print_exc()

load_subscriptions() 

unsubscribe_mode = {}
subscribe_mode = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.KeyboardButton('Подписаться на игру')
    unsubscribe_button = types.KeyboardButton('Отписаться от игры')
    my_subscriptions_button = types.KeyboardButton('Мои подписки')
    send_subscriptions_button = types.KeyboardButton('Отправить информацию о подписках')
    markup.add(subscribe_button, unsubscribe_button, my_subscriptions_button, send_subscriptions_button)
    bot.reply_to(message, 'Приветствую! Напиши название игры, чтобы узнать ее цену в рублях. (Название нужно писать 1:1 как указано в Steam)\nНапример: вы хотите найти игру PUBG: BATTLEGROUNDS, если вы будете писать PUBG или же pubg вам выдаст что игра не найдена.\nТакже и с играми со специальными знаками по типу: Train Sim World® 5, если вы не напишете ® в названии то игру не найдет.', reply_markup=markup)

    chat_id = message.chat.id
    if chat_id in subscribers and subscribers.get(chat_id): 
        response = "Ваши подписки на игры:\n"
        for i, game in enumerate(subscribers[chat_id], start=1):
            response += f"{i}. {game}\n"
        bot.send_message(chat_id, response)
    else:
        bot.send_message(chat_id, 'У вас нет активных подписок.')


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

last_message = {}

@bot.message_handler(content_types=['text'])
def gamemessage(message):
    global subscribers  
    chat_id = str(message.chat.id) 

    if message.text == 'Подписаться на игру':
        bot.send_message(chat_id, 'Напишите название игры, на которую хотите подписаться.')
        last_message[chat_id] = 'Подписаться на игру'
    elif message.text == 'Отписаться от игры':
        bot.send_message(chat_id, 'Напишите название игры, от которой хотите отписаться.')
        last_message[chat_id] = 'Отписаться от игры'
    elif message.text == 'Мои подписки':
        if chat_id in subscribers and subscribers.get(chat_id):
            response = "Ваши подписки на игры:\n"
            for i, game in enumerate(subscribers[chat_id], start=1):
                response += f"{i}. {game}\n"
            bot.send_message(chat_id, response)
        else:
            bot.send_message(chat_id, 'У вас нет подписок на игры.')
    elif message.text == 'Отправить информацию о подписках':
        if chat_id in subscribers and subscribers.get(chat_id):
            response = "Ваши подписки на игры:\n"
            for i, game in enumerate(subscribers[chat_id], start=1):
                response += f"{i}. {game}\n"
            bot.send_message(chat_id, response)
            for game in subscribers[chat_id]:
                games = searchgame(game)
                if games:
                    game_details = games[0]
                    if game_details['discounted_price'] == "В данный момент скидки не присутствует":
                       response = (
                                f"Обновление для игры {game_details['name']}:\n"
                                f"Цена: {game_details['normal_price']} руб.\n"
                                f"Описание: {game_details['description']}\n"
                                f"Ссылка: {game_details['url']}\n"
                            )
                    elif isinstance(game_details['normal_price'], str) and isinstance(game_details['discounted_price'], str) and game_details['normal_price'] != "Бесплатная":
                        response = (
                                f"Обновление для игры {game_details['name']}:\n"
                                f"Цена: {game_details['normal_price']}\n"
                                f"Цена со скидкой: {game_details['discounted_price']}\n"
                                f"Описание: {game_details['description']}\n"
                                f"Ссылка: {game_details['url']}\n"
                            )
                    elif isinstance(game_details['normal_price'], str) and isinstance(game_details['discounted_price'], str) and game_details['normal_price'] == "Бесплатная":
                        response = (
                                f"Обновление для игры {game_details['name']}:\n"
                                f"Цена: {game_details['normal_price']}\n"
                                f"Описание: {game_details['description']}\n"
                                f"Ссылка: {game_details['url']}\n"
                            )
                    else:
                        response = (
                                f"Обновление для игры {game_details['name']}:\n"
                                f"Цена: {game_details['normal_price']} руб.\n"
                                f"Цена со скидкой: {game_details['discounted_price']} руб.\n"
                                f"Описание: {game_details['description']}\n"
                                f"Ссылка: {game_details['url']}\n"
                        )
                    if game_details['image_url']:
                        bot.send_photo(chat_id, game_details['image_url'], response)
                    else:
                        bot.send_message(chat_id, response)
        else:
            bot.send_message(chat_id, 'У вас нет подписок на игры.')
    else:
        if last_message.get(chat_id) == 'Подписаться на игру':
            game_name = message.text
            if chat_id in subscribers:
                if game_name not in subscribers[chat_id]:
                    subscribers[chat_id].append(game_name)
                    save_subscriptions()
                    bot.send_message(chat_id, f'Вы успешно подписались на игру {game_name}.')
                else:
                    bot.send_message(chat_id, f'Вы уже подписаны на игру {game_name}.')
            else:
                subscribers[chat_id] = [game_name]
                save_subscriptions()
                bot.send_message(chat_id, f'Вы успешно подписались на игру {game_name}.')
            last_message[chat_id] = ''

        elif last_message.get(chat_id) == 'Отписаться от игры':
            game_name = message.text
            if chat_id in subscribers and subscribers.get(chat_id) and game_name in subscribers[chat_id]: 
                subscribers[chat_id].remove(game_name)
                save_subscriptions()
                bot.send_message(chat_id, f'Вы успешно отписались от игры {game_name}.')
            else:
                bot.send_message(chat_id, f'Вы не подписаны на игру {game_name}.')
            last_message[chat_id] = ''

        else:
            games = searchgame(message.text)
            if games:
                game_details = games[0]

                if game_details['discounted_price'] == "В данный момент скидки не присутствует":
                    response = (
                        f"Обновление для игры {game_details['name']}:\n"
                        f"Цена: {game_details['normal_price']} руб.\n"
                        f"Описание: {game_details['description']}\n"
                        f"Ссылка: {game_details['url']}\n"
                    )
                elif isinstance(game_details['normal_price'], str) and isinstance(game_details['discounted_price'], str) and game_details['normal_price'] != "Бесплатная":
                    response = (
                        f"Обновление для игры {game_details['name']}:\n"
                        f"Цена: {game_details['normal_price']}\n"
                        f"Цена со скидкой: {game_details['discounted_price']}\n"
                        f"Описание: {game_details['description']}\n"
                        f"Ссылка: {game_details['url']}\n"
                    )
                elif isinstance(game_details['normal_price'], str) and isinstance(game_details['discounted_price'], str) and game_details['normal_price'] == "Бесплатная":
                    response = (
                        f"Обновление для игры {game_details['name']}:\n"
                        f"Цена: {game_details['normal_price']}\n"
                        f"Описание: {game_details['description']}\n"
                        f"Ссылка: {game_details['url']}\n"
                    )
                else:
                    response = (
                        f"Обновление для игры {game_details['name']}:\n"
                        f"Цена: {game_details['normal_price']} руб.\n"
                        f"Цена со скидкой: {game_details['discounted_price']} руб.\n"
                        f"Описание: {game_details['description']}\n"
                        f"Ссылка: {game_details['url']}\n"
                    )

                if game_details['image_url']:
                    bot.send_photo(chat_id, game_details['image_url'], response)
                else:
                    bot.send_message(chat_id, response)
            else:
                bot.send_message(chat_id, f"Игра {message.text} не найдена.")


def send_updates():
    while True:
        for chat_id in subscribers:
            if subscribers.get(chat_id): 
                for game in subscribers[chat_id]:
                    games = searchgame(game)
                    if games:
                        game_details = games[0]

                        if game_details['discounted_price'] == "В данный момент скидки не присутствует":
                            response = (
                                f"Обновление для игры {game_details['name']}:\n"
                                f"Цена: {game_details['normal_price']} руб.\n"
                                f"Описание: {game_details['description']}\n"
                                f"Ссылка: {game_details['url']}\n"
                            )
                        elif isinstance(game_details['normal_price'], str) and isinstance(game_details['discounted_price'], str) and game_details['normal_price'] != "Бесплатная":
                            response = (
                                f"Обновление для игры {game_details['name']}:\n"
                                f"Цена: {game_details['normal_price']}\n"
                                f"Цена со скидкой: {game_details['discounted_price']}\n"
                                f"Описание: {game_details['description']}\n"
                                f"Ссылка: {game_details['url']}\n"
                            )
                        elif isinstance(game_details['normal_price'], str) and isinstance(game_details['discounted_price'], str) and game_details['normal_price'] == "Бесплатная":
                            response = (
                                f"Обновление для игры {game_details['name']}:\n"
                                f"Цена: {game_details['normal_price']}\n"
                                f"Описание: {game_details['description']}\n"
                                f"Ссылка: {game_details['url']}\n"
                            )
                        else:
                            response = (
                                f"Обновление для игры {game_details['name']}:\n"
                                f"Цена: {game_details['normal_price']} руб.\n"
                                f"Цена со скидкой: {game_details['discounted_price']} руб.\n"
                                f"Описание: {game_details['description']}\n"
                                f"Ссылка: {game_details['url']}\n"
                            )
                        try:
                            if game_details['image_url']:
                                bot.send_photo(chat_id, game_details['image_url'], response)
                            else:
                                bot.send_message(chat_id, response)
                        except telebot.apihelper.ApiTelegramException as e:
                            print(f"Ошибка при отправке обновления для {chat_id}: {e}")
                            if "chat not found" in str(e): 
                                print(f"Удаляю подписки для чата {chat_id}, так как он не найден")
                                if chat_id in subscribers:
                                    del subscribers[chat_id]
                                save_subscriptions()

        time.sleep(86400)

if __name__ == '__main__':
    update_thread = threading.Thread(target=send_updates)
    update_thread.start()
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Ошибка: {e}")
