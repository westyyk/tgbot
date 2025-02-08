import requests
import telebot

token = '7351672676:AAGG4zdqm39WrpMn5brgqrU6IJAeXijfrWM'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Приветствую! Напиши название игры, чтобы узнать ее цену в рублях. (Название нужно писать 1:1 как указано в Steam)\nНапример: вы хотите найти игру PUBG: BATTLEGROUNDS, если вы будете писать PUBG или же pubg вам выдаст что игра не найдена.\nТакже и с играми со специальными знаками по типу: Train Sim World® 5, если вы не напишите ® в названии то игру не найдет.')

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
        if game_name == game['name']:
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

    return found_games

@bot.message_handler(func=lambda message: True)
def gamemessage(message):
    game_name = message.text.strip()
    
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
                bot.send_photo(message.chat.id, game['image_url'], response)
            else:
                bot.send_message(message.chat.id, response)

        response = "Если есть другие игры, которые вас интересуют, напишите их названия!"
        bot.send_message(message.chat.id, response)
    else:
        response = "Игры не найдены.\n\nЕсли есть другие игры, которые вас интересуют, напишите их названия!"
        bot.reply_to(message, response)

if __name__ == '__main__':
    try:
        bot.polling(none_stop = True)
    except Exception as e:
        print(f"Ошибка: {e}")
