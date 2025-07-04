import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен твоего бота (получи у @BotFather)
BOT_TOKEN = "8105134473:AAE-bTaKvOtD03rIIUG2dH8BnbaaF7KKmAU"

# Хранилище заметок пользователей (в реальном боте лучше использовать базу данных)
user_notes = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение при команде /start"""
    user = update.effective_user

    # Создаем клавиатуру с кнопками
    keyboard = [
        [
            InlineKeyboardButton("🕐 Время", callback_data='time'),
            InlineKeyboardButton("🌤️ Погода", callback_data='weather')
        ],
        [
            InlineKeyboardButton("ℹ️ Помощь", callback_data='help'),
            InlineKeyboardButton("📋 О боте", callback_data='about')
        ],
        [
            InlineKeyboardButton("🎲 Случайное число", callback_data='random'),
            InlineKeyboardButton("😄 Шутка", callback_data='joke')
        ],
        [
            InlineKeyboardButton("🐸 Мем", callback_data='meme'),
            InlineKeyboardButton("📝 Заметки", callback_data='notes')
        ],
        [
            InlineKeyboardButton("🎵 Слушать ВаниноВоробино", callback_data='audio')
        ],
        [
            InlineKeyboardButton("💬 Написать Ване", url='https://t.me/ivorobinho')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_html(
        f"Привет, {user.mention_html()}! 👋\n\n"
        f"Я простой телеграм-бот с удобными кнопками!\n\n"
        f"Выбери что тебя интересует, нажав на кнопку ниже 👇\n\n"
        f"Или просто напиши мне что-нибудь!",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет справку"""
    help_text = """
🤖 *Команды бота:*

/start - Запустить бота
/help - Показать эту справку
/about - Информация о боте
/echo - Повторить сообщение

📝 *Заметки:*
/note <текст> - Добавить заметку
/clearnotes - Очистить все заметки

*Дополнительные функции:*
• Напиши "время" - покажу текущее время
• Напиши "погода" - покажу погоду в Москве
• Кнопка "🐸 Мем" - случайный мем
• Кнопка "📝 Заметки" - твои заметки
• Отвечаю на любые текстовые сообщения
• Реагирую на стикеры и эмодзи
• Могу обработать фото

Просто напиши мне что-нибудь! 😊
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Информация о боте"""
    await update.message.reply_text(
        "🤖 *О боте*\n\n"
        "Версия: 1.0\n"
        "Создан на Python с использованием python-telegram-bot\n"
        "Разработчик: Ваше имя\n\n"
        "Бот создан для демонстрации базовых возможностей Telegram Bot API.",
        parse_mode='Markdown'
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Повторяет сообщение пользователя"""
    if context.args:
        message = ' '.join(context.args)
        await update.message.reply_text(f"📢 Вы сказали: {message}")
    else:
        await update.message.reply_text(
            "Использование: /echo <ваше сообщение>\n"
            "Пример: /echo Привет мир!"
        )

async def add_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Добавляет заметку пользователя"""
    user_id = update.effective_user.id

    if context.args:
        note_text = ' '.join(context.args)

        # Инициализируем список заметок для пользователя, если его нет
        if user_id not in user_notes:
            user_notes[user_id] = []

        # Добавляем заметку
        user_notes[user_id].append(note_text)

        await update.message.reply_text(
            f"✅ Заметка добавлена!\n\n"
            f"📝 \"{note_text}\"\n\n"
            f"У тебя теперь {len(user_notes[user_id])} заметок.\n"
            f"Посмотреть все заметки: нажми кнопку \"📝 Заметки\" в /start"
        )
    else:
        await update.message.reply_text(
            "Использование: /note <текст заметки>\n\n"
            "Примеры:\n"
            "• /note Купить молоко\n"
            "• /note Позвонить маме\n"
            "• /note Сделать домашку по математике"
        )

async def clear_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Очищает все заметки пользователя"""
    user_id = update.effective_user.id

    if user_id in user_notes and user_notes[user_id]:
        count = len(user_notes[user_id])
        user_notes[user_id] = []
        await update.message.reply_text(f"🗑️ Удалено {count} заметок. Все заметки очищены!")
    else:
        await update.message.reply_text("📝 У тебя нет заметок для удаления.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает обычные текстовые сообщения"""
    user_message = update.message.text.lower()

    # Простые ответы на ключевые слова
    if "время" in user_message:
        from datetime import datetime, timezone, timedelta

        # Московское время (UTC+3)
        moscow_tz = timezone(timedelta(hours=3))
        current_time = datetime.now(moscow_tz)
        formatted_time = current_time.strftime("%H:%M:%S")
        formatted_date = current_time.strftime("%d.%m.%Y")

        await update.message.reply_text(
            f"🕐 Текущее время: {formatted_time}\n"
            f"📅 Дата: {formatted_date}\n"
            f"🌍 Часовой пояс: Москва (UTC+3)"
        )
    elif "погода" in user_message:
        import requests

        try:
            # Используем бесплатный API wttr.in для получения погоды
            response = requests.get("https://wttr.in/Moscow?format=j1", timeout=5)
            if response.status_code == 200:
                weather_data = response.json()
                current = weather_data['current_condition'][0]

                temp = current['temp_C']
                feels_like = current['FeelsLikeC']
                humidity = current['humidity']
                description = current['weatherDesc'][0]['value']
                wind_speed = current['windspeedKmph']

                weather_emojis = {
                    'sunny': '☀️', 'clear': '☀️', 'partly cloudy': '⛅',
                    'cloudy': '☁️', 'overcast': '☁️', 'mist': '🌫️',
                    'fog': '🌫️', 'rain': '🌧️', 'drizzle': '🌦️',
                    'snow': '❄️', 'thunderstorm': '⛈️'
                }

                emoji = '🌤️'  # По умолчанию
                for key, value in weather_emojis.items():
                    if key in description.lower():
                        emoji = value
                        break

                await update.message.reply_text(
                    f"{emoji} *Погода в Москве:*\n\n"
                    f"🌡️ Температура: {temp}°C (ощущается как {feels_like}°C)\n"
                    f"💧 Влажность: {humidity}%\n"
                    f"💨 Ветер: {wind_speed} км/ч\n"
                    f"📋 Описание: {description}",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    "😔 Извините, не удалось получить данные о погоде. Попробуйте позже."
                )
        except Exception as e:
            await update.message.reply_text(
                "⚠️ Произошла ошибка при получении данных о погоде. Попробуйте позже."
            )
    elif "привет" in user_message or "hello" in user_message:
        await update.message.reply_text("Привет! 👋 Как дела?")
    elif "как дела" in user_message:
        await update.message.reply_text("У меня всё отлично! 😊 А у тебя как?")
    elif "спасибо" in user_message:
        await update.message.reply_text("Пожалуйста! 😊 Рад помочь!")
    elif "пока" in user_message or "до свидания" in user_message:
        await update.message.reply_text("До свидания! 👋 Увидимся позже!")
    else:
        # Обычный ответ
        responses = [
            f"Интересно! Ты написал: '{update.message.text}'",
            "Понял тебя! 👍",
            "Хорошее сообщение! 😊",
            "Спасибо за сообщение!",
            f"Получил твоё сообщение: {update.message.text}"
        ]
        import random
        await update.message.reply_text(random.choice(responses))

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает фотографии"""
    await update.message.reply_text(
        "📸 Отличное фото! К сожалению, я пока не умею анализировать изображения, "
        "но вижу, что ты прислал картинку! 👍"
    )

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает стикеры"""
    await update.message.reply_text("😄 Классный стикер! Я тоже люблю стикеры! 🎉")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатия на кнопки"""
    query = update.callback_query
    await query.answer()  # Убирает индикатор загрузки с кнопки

    if query.data == 'time':
        from datetime import datetime, timezone, timedelta

        moscow_tz = timezone(timedelta(hours=3))
        current_time = datetime.now(moscow_tz)
        formatted_time = current_time.strftime("%H:%M:%S")
        formatted_date = current_time.strftime("%d.%m.%Y")

        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"🕐 Текущее время: {formatted_time}\n"
            f"📅 Дата: {formatted_date}\n"
            f"🌍 Часовой пояс: Москва (UTC+3)",
            reply_markup=reply_markup
        )

    elif query.data == 'weather':
        import requests

        try:
            response = requests.get("https://wttr.in/Moscow?format=j1", timeout=5)
            if response.status_code == 200:
                weather_data = response.json()
                current = weather_data['current_condition'][0]

                temp = current['temp_C']
                feels_like = current['FeelsLikeC']
                humidity = current['humidity']
                description = current['weatherDesc'][0]['value']
                wind_speed = current['windspeedKmph']

                weather_emojis = {
                    'sunny': '☀️', 'clear': '☀️', 'partly cloudy': '⛅',
                    'cloudy': '☁️', 'overcast': '☁️', 'mist': '🌫️',
                    'fog': '🌫️', 'rain': '🌧️', 'drizzle': '🌦️',
                    'snow': '❄️', 'thunderstorm': '⛈️'
                }

                emoji = '🌤️'
                for key, value in weather_emojis.items():
                    if key in description.lower():
                        emoji = value
                        break
                keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await query.edit_message_text(
                    f"{emoji} *Погода в Москве:*\n\n"
                    f"🌡️ Температура: {temp}°C (ощущается как {feels_like}°C)\n"
                    f"💧 Влажность: {humidity}%\n"
                    f"💨 Ветер: {wind_speed} км/ч\n"
                    f"📋 Описание: {description}",
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            else:
                 keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')]]
                 reply_markup = InlineKeyboardMarkup(keyboard)
                 await query.edit_message_text(
                    "😔 Извините, не удалось получить данные о погоде.",
                    reply_markup=reply_markup
                )
        except Exception as e:
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                "⚠️ Произошла ошибка при получении данных о погоде.",
                reply_markup=reply_markup
            )

    elif query.data == 'help':
        help_text = """
🤖 *Команды бота:*

/start - Запустить бота и показать кнопки
/help - Показать справку
/about - Информация о боте
/echo - Повторить сообщение

📝 *Заметки:*
/note <текст> - Добавить заметку
/clearnotes - Очистить все заметки

*Дополнительные функции:*
• Кнопка "🕐 Время" - текущее время
• Кнопка "🌤️ Погода" - погода в Москве
• Кнопка "🐸 Мем" - случайный мем
• Кнопка "📝 Заметки" - твои заметки
• Отвечаю на любые текстовые сообщения
• Реагирую на стикеры и эмодзи
• Могу обработать фото
"""
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(help_text, parse_mode='Markdown', reply_markup=reply_markup)

    elif query.data == 'about':
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🤖 *О боте*\n\n"
            "Версия: 1.1 (с кнопками!)\n"
            "Создан на Python с использованием python-telegram-bot\n"
            "Разработчик: Ваше имя\n\n"
            "Бот создан для демонстрации базовых возможностей Telegram Bot API "
            "включая интерактивные кнопки!",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    elif query.data == 'random':
        import random
        number = random.randint(1, 100)
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"🎲 Твоё случайное число: *{number}*",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    elif query.data == 'joke':
        jokes = [
            "Почему программисты не любят природу? Там слишком много багов! 🐛",
            "Что говорит один байт другому? Ты выглядишь немного побитово! 💾",
            "Почему компьютер пошёл к врачу? У него был вирус! 🦠",
            "Как называется программист, который не пьёт кофе? Спящий режим! ☕",
            "Что сказал HTML, когда встретил CSS? Ты делаешь меня красивым! 💄"
        ]
        import random
        joke = random.choice(jokes)
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"😄 Вот тебе шутка:\n\n{joke}",
            reply_markup=reply_markup
        )

    elif query.data == 'meme':
        memes = [
            "https://i.imgur.com/dQw4w9WgXcQ.jpg 😂",
            "Когда увидел баг в коде:\n*паника* 😱",
            "Программист: «Работает на моей машине» 🤷‍♂️",
            "— Сколько программистов нужно, чтобы вкрутить лампочку?\n— Ноль. Это аппаратная проблема! 💡",
            "Жизнь программиста:\n☕ Кофе → 💻 Код → 🐛 Баг → 😩 Фикс → Повтор",
            "404: Мотивация не найдена 🤖",
            "Ctrl+C, Ctrl+V — мой любимый алгоритм! 📋",
            "Когда код заработал с первого раза:\n*подозрительно* 🤔"
        ]
        import random
        meme = random.choice(memes)
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            f"🐸 Лови мем:\n\n{meme}",
            reply_markup=reply_markup
        )

    elif query.data == 'notes':
        user_id = query.from_user.id
        if user_id in user_notes and user_notes[user_id]:
            notes_text = "\n".join([f"• {note}" for note in user_notes[user_id]])
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"📝 *Твои заметки:*\n\n{notes_text}\n\n"
                f"Чтобы добавить заметку, напиши: /note <текст>\n"
                f"Чтобы очистить заметки, напиши: /clearnotes",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
        else:
            keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(
                f"📝 *Заметки пусты*\n\n"
                f"Чтобы добавить заметку, напиши: /note <текст>\n"
                f"Пример: /note Купить молоко",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )

    elif query.data == 'audio':
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data='back_to_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Отправляем аудиофайл
        try:
            with open('attached_assets/untitled_1751277144360.mp3', 'rb') as audio_file:
                await context.bot.send_audio(
                    chat_id=query.message.chat_id,
                    audio=audio_file,
                    title="ВаниноВоробино",
                    performer="Ваня",
                    caption="🎵 Слушай ВаниноВоробино! 🎶"
                )
        except Exception as e:
            await query.edit_message_text(
                "😔 Извини, не удалось загрузить аудиофайл.",
                reply_markup=reply_markup
            )
            return
            
        await query.edit_message_text(
            "🎵 *ВаниноВоробино*\n\n"
            "Наслаждайся музыкой! 🎶\n"
            "Аудиофайл отправлен выше ⬆️",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    elif query.data == 'back_to_menu':
        # Возвращаемся в главное меню
        user = query.from_user

        # Создаем клавиатуру с кнопками (копируем из функции start)
        keyboard = [
            [
                InlineKeyboardButton("🕐 Время", callback_data='time'),
                InlineKeyboardButton("🌤️ Погода", callback_data='weather')
            ],
            [
                InlineKeyboardButton("ℹ️ Помощь", callback_data='help'),
                InlineKeyboardButton("📋 О боте", callback_data='about')
            ],
            [
                InlineKeyboardButton("🎲 Случайное число", callback_data='random'),
                InlineKeyboardButton("😄 Шутка", callback_data='joke')
            ],
            [
                InlineKeyboardButton("🐸 Мем", callback_data='meme'),
                InlineKeyboardButton("📝 Заметки", callback_data='notes')
            ],
            [
                InlineKeyboardButton("🎵 Слушать ВаниноВоробино", callback_data='audio')
            ],
            [
                InlineKeyboardButton("💬 Написать Ване", url='https://t.me/ivorobinho')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            f"Привет, {user.mention_html()}! 👋\n\n"
            f"Я простой телеграм-бот с удобными кнопками!\n\n"
            f"Выбери что тебя интересует, нажав на кнопку ниже 👇\n\n"
            f"Или просто напиши мне что-нибудь!",
            parse_mode='HTML',
            reply_markup=reply_markup
        )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает ошибки"""
    logger.warning(f'Update {update} caused error {context.error}')

def main() -> None:
    """Запускает бота"""
    # Создаём приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("note", add_note))
    application.add_handler(CommandHandler("clearnotes", clear_notes))

    # Добавляем обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))

    # Добавляем обработчик кнопок
    application.add_handler(CallbackQueryHandler(button_callback))

    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)

    # Запускаем бота
    print("🤖 Бот запускается...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()