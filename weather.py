import telebot
from telebot import types
token = '7555331120:AAH4jbM0M4EsXaMOFif15OEqRNA-iip27-c'
bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Алтайский край')
    item2 = types.KeyboardButton('Амурская область')
    item3 = types.KeyboardButton('Архангельская область')
    item4 = types.KeyboardButton('Астраханская область')
    item5 = types.KeyboardButton('Белгородская область')
    item6 = types.KeyboardButton('Брянская область')
    item7 = types.KeyboardButton('Владимирская область')
    item8 = types.KeyboardButton('Волгоградская область')
    item9 = types.KeyboardButton('Воронежская область')
    item10 = types.KeyboardButton('Еврейская автономная область')
    item11 = types.KeyboardButton('Забайкальский край')
    item12 = types.KeyboardButton('Запорожская область')
    item13 = types.KeyboardButton('Ивановская область')
    item14 = types.KeyboardButton('Иркутская область')
    item15 = types.KeyboardButton('Калининградская область')
    item16 = types.KeyboardButton('Калужская область')
    item17 = types.KeyboardButton('Камчатский край')
    item18 = types.KeyboardButton('Кемеровская область')
    item19 = types.KeyboardButton('Кировская область')
    item20 = types.KeyboardButton('Костромска область')
    item21 = types.KeyboardButton('Краснодарский край')
    item22 = types.KeyboardButton('Красноярский край')
    item23 = types.KeyboardButton('Крым')
    item24 = types.KeyboardButton('Курганская область')
    item25 = types.KeyboardButton('Курская область')
    item26 = types.KeyboardButton('Ленинградская область')
    item27 = types.KeyboardButton('Липецкая область')
    item28 = types.KeyboardButton('Магаданская область')
    item29 = types.KeyboardButton('Московская область')
    item30 = types.KeyboardButton('Мурманская область')
    item31 = types.KeyboardButton('Ненецкий автономный округ')
    item32 = types.KeyboardButton('Нижегородская область')
    item33 = types.KeyboardButton('Новгородская область')
    item34 = types.KeyboardButton('Новосибирская область')
    item35 = types.KeyboardButton('Омская область')
    item36 = types.KeyboardButton('Оренбургская область')
    item37 = types.KeyboardButton('Орловская область')
    item38 = types.KeyboardButton('Пензенская область')
    item39 = types.KeyboardButton('Пермский край')
    item40 = types.KeyboardButton('Приморский край')
    item41 = types.KeyboardButton('Всковская область')
    item42 = types.KeyboardButton('Республика Адыгея')
    item43 = types.KeyboardButton('Республика Алтай')
    item44 = types.KeyboardButton('Республика Башкортостан')
    item45 = types.KeyboardButton('Республика Бурятия')
    item46 = types.KeyboardButton('Республика Дагестан')
    item47 = types.KeyboardButton('Республика Ингушетия')
    item48 = types.KeyboardButton('Республика Калмыкия')
    item49 = types.KeyboardButton('Республика Карелия')
    item50 = types.KeyboardButton('Республика Коми')
    item51 = types.KeyboardButton('Республика Марий Эл')
    item52 = types.KeyboardButton('Республика Мордовия')
    item53 = types.KeyboardButton('Республика Якутия')
    item54 = types.KeyboardButton('Республика Северная Осетия - Алания')
    item55 = types.KeyboardButton('Республика Татарстан')
    item56 = types.KeyboardButton('Республика Тыва')
    item57 = types.KeyboardButton('Республика Хакасия')
    item58 = types.KeyboardButton('Ростовска область')
    item59 = types.KeyboardButton('Рязанская область')
    item60 = types.KeyboardButton('Самарская область')
    item61 = types.KeyboardButton('Саратовская область')
    item62 = types.KeyboardButton('Сахалинская область')
    item63 = types.KeyboardButton('Свердловская область')
    item64 = types.KeyboardButton('Смоленская область')
    item65 = types.KeyboardButton('Ставропольский край')
    item66 = types.KeyboardButton('Тамбовская область')
    item67 = types.KeyboardButton('Тверская область')
    item68 = types.KeyboardButton('Томская область')
    item69 = types.KeyboardButton('Тульская область')
    item70 = types.KeyboardButton('Тюменская область')
    item71 = types.KeyboardButton('Удмуртская Республика')
    item72 = types.KeyboardButton('Ульяновская область')
    item73 = types.KeyboardButton('Хабаровский край')
    item74 = types.KeyboardButton('Ханты-Мансийский автономный округ')
    item75 = types.KeyboardButton('Херсонская область')
    item76 = types.KeyboardButton('Челябинская область')
    item77 = types.KeyboardButton('Чеченская республика')
    item78 = types.KeyboardButton('Чувашская республика')
    item79 = types.KeyboardButton('Чукотский автономный округ')
    item80 = types.KeyboardButton('Ямало-Ненецкий автономный округ')
    item81 = types.KeyboardButton('Ярославская область')



    markup.add(item1,item2,item3,item4,item5,item6,item7,item8,item9,item10,item11,item12,item13,item14,item15,item16,item17,item18,item19,item20,item21,item22,item23,item24,item25,item26,item27,item28,item29,item30,item31,item32,item33,item34,item35,item36,item37,item38,item39,item40,item41,item42,item43,item44,item45,item46,item47,item48,item49,item50,item51,item52,item53,item54,item55,item56,item57,item58,item59,item60,item61,item62,item63,item64,item65,item66,item67,item68,item69,item70,item71,item72,item73,item74,item75,item76,item77,item78,item79,item80,item81)

    bot.send_message(message.chat.id, 'Привет! в каком регионе тебя интересует погода?'.format(message.from_user), reply_markup = markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
  if message.chat.type == 'private':
    if message.text == 'Алтайский край':
      markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
      item1 = types.KeyboardButton('Алейск')
      item2 = types.KeyboardButton('Барнаул')
      item3 = types.KeyboardButton('Белокуриха')
      item4 = types.KeyboardButton('Бийск')
      item5 = types.KeyboardButton('Горняк')
      item6 = types.KeyboardButton('Заринск')
      item7 = types.KeyboardButton('Змеиногорск')
      item8 = types.KeyboardButton('Камень-на-Оби')
      item9 = types.KeyboardButton('Новоалтайск')
      item10 = types.KeyboardButton('Рубцовск')
      item11 = types.KeyboardButton('Славгород')
      item12 = types.KeyboardButton('Яровое')


      back = types.KeyboardButton('Назад')
      markup.add(item1,item2,item3,item4,item5,item6,item7,item8,item9,item10,item11,item12, back)
      
      bot.send_message(message.chat.id, 'Какой город вас интересует?', reply_markup = markup)

    
    elif message.text == 'Амурская область':
      markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
      item1 = types.KeyboardButton('Барнаул')
      item2 = types.KeyboardButton('Заринск')
      back = types.KeyboardButton('Назад')
      markup.add(item1, item2, back)
      
      bot.send_message(message.chat.id, 'Какой город вас интересует?', reply_markup = markup)


    elif message.text == 'Архангельская область':
      markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
      item1 = types.KeyboardButton('Барнаул')
      item2 = types.KeyboardButton('Заринск')
      back = types.KeyboardButton('Назад')
      markup.add(item1, item2, back)
      
      bot.send_message(message.chat.id, 'Какой город вас интересует?', reply_markup = markup)
    

    elif message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('Алтайский край')
        item2 = types.KeyboardButton('Амурская область')
        item3 = types.KeyboardButton('Архангельская область')
        item4 = types.KeyboardButton('Астраханская область')
        item5 = types.KeyboardButton('Белгородская область')
        item6 = types.KeyboardButton('Брянская область')
        item7 = types.KeyboardButton('Владимирская область')
        item8 = types.KeyboardButton('Волгоградская область')
        item9 = types.KeyboardButton('Воронежская область')
        item10 = types.KeyboardButton('Еврейская автономная область')
        item11 = types.KeyboardButton('Забайкальский край')
        item12 = types.KeyboardButton('Запорожская область')
        item13 = types.KeyboardButton('Ивановская область')
        item14 = types.KeyboardButton('Иркутская область')
        item15 = types.KeyboardButton('Калининградская область')
        item16 = types.KeyboardButton('Калужская область')
        item17 = types.KeyboardButton('Камчатский край')
        item18 = types.KeyboardButton('Кемеровская область')
        item19 = types.KeyboardButton('Кировская область')
        item20 = types.KeyboardButton('Костромска область')
        item21 = types.KeyboardButton('Краснодарский край')
        item22 = types.KeyboardButton('Красноярский край')
        item23 = types.KeyboardButton('Крым')
        item24 = types.KeyboardButton('Курганская область')
        item25 = types.KeyboardButton('Курская область')
        item26 = types.KeyboardButton('Ленинградская область')
        item27 = types.KeyboardButton('Липецкая область')
        item28 = types.KeyboardButton('Магаданская область')
        item29 = types.KeyboardButton('Московская область')
        item30 = types.KeyboardButton('Мурманская область')
        item31 = types.KeyboardButton('Ненецкий автономный округ')
        item32 = types.KeyboardButton('Нижегородская область')
        item33 = types.KeyboardButton('Новгородская область')
        item34 = types.KeyboardButton('Новосибирская область')
        item35 = types.KeyboardButton('Омская область')
        item36 = types.KeyboardButton('Оренбургская область')
        item37 = types.KeyboardButton('Орловская область')
        item38 = types.KeyboardButton('Пензенская область')
        item39 = types.KeyboardButton('Пермский край')
        item40 = types.KeyboardButton('Приморский край')
        item41 = types.KeyboardButton('Всковская область')
        item42 = types.KeyboardButton('Республика Адыгея')
        item43 = types.KeyboardButton('Республика Алтай')
        item44 = types.KeyboardButton('Республика Башкортостан')
        item45 = types.KeyboardButton('Республика Бурятия')
        item46 = types.KeyboardButton('Республика Дагестан')
        item47 = types.KeyboardButton('Республика Ингушетия')
        item48 = types.KeyboardButton('Республика Калмыкия')
        item49 = types.KeyboardButton('Республика Карелия')
        item50 = types.KeyboardButton('Республика Коми')
        item51 = types.KeyboardButton('Республика Марий Эл')
        item52 = types.KeyboardButton('Республика Мордовия')
        item53 = types.KeyboardButton('Республика Якутия')
        item54 = types.KeyboardButton('Республика Северная Осетия - Алания')
        item55 = types.KeyboardButton('Республика Татарстан')
        item56 = types.KeyboardButton('Республика Тыва')
        item57 = types.KeyboardButton('Республика Хакасия')
        item58 = types.KeyboardButton('Ростовска область')
        item59 = types.KeyboardButton('Рязанская область')
        item60 = types.KeyboardButton('Самарская область')
        item61 = types.KeyboardButton('Саратовская область')
        item62 = types.KeyboardButton('Сахалинская область')
        item63 = types.KeyboardButton('Свердловская область')
        item64 = types.KeyboardButton('Смоленская область')
        item65 = types.KeyboardButton('Ставропольский край')
        item66 = types.KeyboardButton('Тамбовская область')
        item67 = types.KeyboardButton('Тверская область')
        item68 = types.KeyboardButton('Томская область')
        item69 = types.KeyboardButton('Тульская область')
        item70 = types.KeyboardButton('Тюменская область')
        item71 = types.KeyboardButton('Удмуртская Республика')
        item72 = types.KeyboardButton('Ульяновская область')
        item73 = types.KeyboardButton('Хабаровский край')
        item74 = types.KeyboardButton('Ханты-Мансийский автономный округ')
        item75 = types.KeyboardButton('Херсонская область')
        item76 = types.KeyboardButton('Челябинская область')
        item77 = types.KeyboardButton('Чеченская республика')
        item78 = types.KeyboardButton('Чувашская республика')
        item79 = types.KeyboardButton('Чукотский автономный округ')
        item80 = types.KeyboardButton('Ямало-Ненецкий автономный округ')
        item81 = types.KeyboardButton('Ярославская область')


    
    markup.add(item1,item2,item3,item4,item5,item6,item7,item8,item9,item10,item11,item12,item13,item14,item15,item16,item17,item18,item19,item20,item21,item22,item23,item24,item25,item26,item27,item28,item29,item30,item31,item32,item33,item34,item35,item36,item37,item38,item39,item40,item41,item42,item43,item44,item45,item46,item47,item48,item49,item50,item51,item52,item53,item54,item55,item56,item57,item58,item59,item60,item61,item62,item63,item64,item65,item66,item67,item68,item69,item70,item71,item72,item73,item74,item75,item76,item77,item78,item79,item80,item81)

    bot.send_message(message.chat.id, 'В каком регионе тебя интересует погода?'.format(message.from_user), reply_markup = markup)



bot.polling(none_stop = True)

