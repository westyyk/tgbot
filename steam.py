import requests
import telebot
from telebot import types
import time
import json
import os
import threading
import traceback
from datetime import datetime

token = '7351672676:AAGG4zdqm39WrpMn5brgqrU6IJAeXijfrWM'  # Замените тут на ваш токен бота (если требуется)
bot = telebot.TeleBot(token)

current_directory = os.path.dirname(__file__)
subscriptions_file = os.path.join(os.path.dirname(__file__), 'subscriptions.json')
feedback_file = os.path.join(current_directory, 'feedback.txt')
votes_file = os.path.join(current_directory, 'poll_votes.txt')

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
    bot.reply_to(message, 'Приветствую! Напиши название игры, чтобы узнать ее цену в рублях. (Название нужно писать 1:1 как указано в Steam)\nНапример: вы хотите найти игру PUBG: BATTLEGROUNDS, если вы будете писать PUBG или же pubg вам выдаст что игра не найдена.\nТакже и с играми со специальными знаками по типу: Train Sim World® 5, если вы не напишете ® в названии то игру не найдет.\nТакже для того чтобы посмтреть за что отвечают команды используйте команду /help ', reply_markup=markup)

    chat_id = message.chat.id
    if chat_id in subscribers and subscribers.get(chat_id): 
        response = "Ваши подписки на игры:\n"
        for i, game in enumerate(subscribers[chat_id], start=1):
            response += f"{i}. {game}\n"
        bot.send_message(chat_id, response)
    else:
        bot.send_message(chat_id, 'У вас нет активных подписок.')

@bot.message_handler(commands=['subbuttons'])
def subbuttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    subscribe_button = types.KeyboardButton('Подписаться на игру')
    unsubscribe_button = types.KeyboardButton('Отписаться от игры')
    my_subscriptions_button = types.KeyboardButton('Мои подписки')
    send_subscriptions_button = types.KeyboardButton('Информация о подписках')
    markup.add(subscribe_button, unsubscribe_button, my_subscriptions_button, send_subscriptions_button)
    bot.reply_to(message, 'Выберите действие:', reply_markup=markup)

@bot.message_handler(commands=['feedback'])
def feedback(message):
    bot.send_message(message.chat.id, 'Пожалуйста, напишите ваш отзыв:')
    bot.register_next_step_handler(message, save_feedback)

def save_feedback(message):
    chat_id = message.chat.id
    feedback_text = message.text
    try:
        # Форматируем текущую дату и время
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Записываем отзыв в файл
        with open(feedback_file, 'a', encoding='utf-8') as file:
            file.write(f"{chat_id}|{timestamp}|{feedback_text}\n")  # Сохраняем chat_id, время и отзыв

        bot.send_message(chat_id, 'Ваш отзыв был успешно сохранен! Спасибо!')
    except Exception as e:
        bot.send_message(chat_id, 'Произошла ошибка при сохранении отзыва. Пожалуйста, попробуйте еще раз.')
        print(f"Ошибка при сохранении отзыва: {e}")

@bot.message_handler(commands=['show_feedback'])
def show_feedback(message):
    chat_id = str(message.chat.id)
    try:
        if os.path.exists(feedback_file):
            with open(feedback_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                
            user_feedback = [line.strip() for line in lines if line.startswith(chat_id)]

            if user_feedback:
                feedback_display = "\n".join([f"{i+1}. {line.split('|', 2)[1]}: {line.split('|', 2)[2]}" for i, line in enumerate(user_feedback)])
                bot.send_message(chat_id, f"Ваши отзывы:\n{feedback_display}")
            else:
                bot.send_message(chat_id, "У вас нет оставленных отзывов.")
        else:
            bot.send_message(chat_id, "У вас нет оставленных отзывов.")
    except Exception as e:
        bot.send_message(chat_id, 'Произошла ошибка при загрузке отзывов. Пожалуйста, попробуйте еще раз.')
        print(f"Ошибка при загрузке отзывов: {e}")

@bot.message_handler(commands=['poll'])
def poll(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    option1 = types.KeyboardButton('Поддержка новых игр')
    option2 = types.KeyboardButton('Улучшить интерфейс')
    option3 = types.KeyboardButton('Уведомления о скидках')
    option4 = types.KeyboardButton('Другое...')
    markup.add(option1, option2, option3, option4)
    bot.send_message(message.chat.id, 'Какую функцию вы хотите видеть?', reply_markup=markup)

# Функция для обновления голосов в файле
def update_votes(votes):
    try:
        with open(votes_file, 'w', encoding='utf-8') as file:
            file.write("Голосование:\n")
            for option in ['Поддержка новых игр', 'Улучшить интерфейс', 'Уведомления о скидках']:
                file.write(f"{option} - {votes[option]}\n")
            file.write(f"Другое - {len(votes['Другое'])}\n")

            file.write("\nГолосование за Другое:\n")
            for entry in votes['Другое']:
                file.write(f"{entry}\n")
    except Exception as e:
        print(f"Ошибка при записи голосов: {e}")

# Создадим словарь для хранения голосов
votes = {
    'Поддержка новых игр': 0,
    'Улучшить интерфейс': 0,
    'Уведомления о скидках': 0,
    'Другое': []  # Список для сообщений пользователей по "Другое"
}

# Обработка выбора пользователя в опросе
@bot.message_handler(func=lambda message: message.text in ['Поддержка новых игр', 'Улучшить интерфейс', 'Уведомления о скидках', 'Другое...'])
def handle_poll_selection(message):
    if message.text == 'Другое...':
        bot.send_message(message.chat.id, 'Напишите, что именно вы хотите видеть:')
        bot.register_next_step_handler(message, handle_other_suggestion)
    else:
        # Увеличиваем счетчик голосов
        votes[message.text] += 1  # Увеличиваем количество голосов за выбранный вариант
        update_votes(votes)  # Сохраняем обновленные данные в файл
        bot.send_message(message.chat.id, 'Спасибо за ваш ответ!')

# Обработка уточнения для выбранного "Другое"
def handle_other_suggestion(message):
    other_feedback = message.text
    chat_id = message.chat.id
    # Добавляем ответ от пользователя в список "Другое"
    votes['Другое'].append(f"{chat_id}: {other_feedback}")
    update_votes(votes)  # Сохраняем обновленные данные в файл
    bot.send_message(chat_id, 'Спасибо за вашу идею!')

# Команда для отображения результатов голосования
@bot.message_handler(commands=['poll_results'])
def poll_results(message):
    if not os.path.exists(votes_file):
        bot.send_message(message.chat.id, "Пока нет никаких результатов голосования.")
        return

    # Читаем результаты из файла и отправляем их пользователю
    try:
        with open(votes_file, 'r', encoding='utf-8') as file:
            results = file.read()
        bot.send_message(message.chat.id, results)
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при загрузке результатов.")
        print(f"Ошибка при загрузке результатов: {e}")

@bot.message_handler(func=lambda message: message.text in ['Поддержка новых игр', 'Улучшить интерфейс', 'Уведомления о скидках', 'Другое...'])
def handle_poll_selection(message):
    if message.text == 'Другое...':
        bot.send_message(message.chat.id, 'Напишите, что именно вы хотите видеть:')
        bot.register_next_step_handler(message, handle_other_suggestion)
    else:
        feedback = message.text
        print(f"Ответ на опрос: {feedback}")  # Сохраняйте этот ответ в файл или базу данных
        bot.send_message(message.chat.id, 'Спасибо за ваш ответ!')

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "Доступные команды:\n"
        "/start - Начать взаимодействие с ботом.\n"
        "/help - Показать это сообщение с доступными командами.\n"
        "/feedback - Оставить отзыв о боте.\n"
        "/show_feedback - Показать ваши оставленные отзывы.\n"
        "/poll - Принять участие в опросе.\n"
        "/subbuttons - Возвращение основного меню подписок на игры.\n"
    )
    bot.send_message(message.chat.id, help_text)

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
    elif message.text == 'Информация о подписках':
        if chat_id in subscribers and subscribers.get(chat_id):
            for game in subscribers[chat_id]:
                games = searchgame(game)
                if games:
                    game_details = games[0]
                    response = (
                        f"Информация о игре {game_details['name']}:\n"
                    )

                    # Проверяем, бесплатная ли игра
                    if game_details['normal_price'] == "Бесплатная":
                        response += "Цена: Бесплатная\n"
                    else:
                        response += f"Цена: {game_details['normal_price']} руб.\n"
                        if game_details['discounted_price'] != "В данный момент скидки не присутствует":
                            response += f"Цена со скидкой: {game_details['discounted_price']} руб.\n"

                    response += (
                        f"Описание: {game_details['description']}\n"
                        f"Ссылка: {game_details['url']}\n"
                    )

                    if game_details['image_url']:
                        bot.send_photo(chat_id, game_details['image_url'], response)
                    else:
                        bot.send_message(chat_id, response)
                else:
                    bot.send_message(chat_id, f"Информация о игре «{game}» не найдена.")
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
            if chat_id in subscribers and game_name in subscribers[chat_id]: 
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

                response = (
                    f"Информация о игре {game_details['name']}:\n"
                )

                # Проверяем, бесплатная ли игра
                if game_details['normal_price'] == "Бесплатная":
                    response += "Цена: Бесплатная\n"
                else:
                    response += f"Цена: {game_details['normal_price']} руб.\n"
                    if game_details['discounted_price'] != "В данный момент скидки не присутствует":
                        response += f"Цена со скидкой: {game_details['discounted_price']} руб.\n"

                response += (
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
                    games = searchgame(game)  # Ваша функция поиска игры
                    if games:
                        game_details = games[0]

                        response = f"Обновление для игры {game_details['name']}:\n"

                        # Если игра бесплатная
                        if game_details['normal_price'] == "Бесплатная":
                            response += (
                                f"Цена: Бесплатная\n"
                                f"Описание: {game_details['description']}\n"
                                f"Ссылка: {game_details['url']}\n"
                            )
                        else:
                            # Если игра платная
                            response += (
                                f"Цена: {game_details['normal_price']} руб.\n"
                            )
                            if game_details['discounted_price'] != "В данный момент скидки не присутствует":
                                response += (
                                    f"Цена со скидкой: {game_details['discounted_price']} руб.\n"
                                )
                            response += (
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
