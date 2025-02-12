# Telegram Bot для поиска игр в Steam

Этот Telegram-бот позволяет пользователям искать информацию об играх в Steam, включая их стоимость, описание и наличие скидок. Пользователи могут подписываться на обновления о ценах на игры и получать уведомления о скидках.

## Функции

- **Поиск игр**: Пользователи могут вводить название игры, и бот предоставит информацию о найденных играх, включая:
  - Название игры
  - Обычную цену
  - Скидочную цену (если доступно)
  - Описание игры
  - Ссылку на страницу игры в Steam
  - Изображение игры

- **Подписка на обновления**: Пользователи могут подписываться на обновления по конкретным играм и получать уведомления о изменении цен.

- **Отписка от обновлений**: Пользователи могут отписаться от уведомлений о конкретных играх.

- **Просмотр текущих подписок**: Пользователи могут просматривать список игр, на которые они подписаны.

## Установка

Eсли у вас нет git, вам нужно установить его: https://git-scm.com/downloads

Чтобы начать работу, вам нужно установить необходимые библиотеки Python. Зайдите в папку tgbot-main и введите в cmd или terminal эту команду (удерживайте SHIFT и нажмите ПКМ по пустому месту в папке для win10): 
```bash
pip install -r requirements.txt
```
Добавьте свой токен в код: В файле ```steam.py``` замените token = ```'BOT_TOKEN'``` на ваш собственный токен, который можно получить у <a href=https://t.me/BotFather>BotFather</a>.
1. **Клонируйте репозиторий**:
```bash
git clone https://github.com/westyyk/tgbot
```
2. **Запустите бота**:
```bash
python steam.py
```
## Использование

1. Найдите нашего бота в Telegram и начните с ним чат. (@Steamsales00Bot)
2. Введите команду /start, чтобы начать взаимодействие с ботом.
3. Используйте следующие команды:
   - **Подписаться на игру**: Введите "Подписаться на игру", затем название игры.
   - **Отписаться от игры**: Введите "Отписаться от игры", затем название игры.
   - **Мои подписки**: Введите "Мои подписки", чтобы увидеть список игр, на которые вы подписаны.
   - Вводите название игры для поиска информации о ней.

