import telebot
from telebot import types

from config import keys, TOKEN
from extensions import ConvertionException, CriptoConverter

bot = telebot.TeleBot(TOKEN)


def create_markup(base=None):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    buttons = []
    for val in keys.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val.upper()))

    markup.add(*buttons)
    return markup


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет, это бот позволяющий узнавать информацию о \n' \
           'текущих курсах валют, поможет перевести одну валюту  \n' \
           'в другую согласно текущему курсу. \n' \
           'Чтобы получить подробную инструкцию введите: /help\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Бот понимает команду в следующем формате: \n' \
           '<имя валюты> <в какую перевести> <сколько перевести> \n' \
           'Например: доллар рубль 10 \n' \
           'Чтобы увидеть список доступных валют введите: /values\n' \
           'Попробовать интерактивный подход: /converter\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['converter'])
def interacive(message: telebot.types.Message):
    text = 'Какую валюту конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=create_markup())
    bot.register_next_step_handler(message, base_handler)


def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = 'В какую конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=create_markup(base))
    bot.register_next_step_handler(message, quote_handler, base)


def quote_handler(message: telebot.types.Message, base):
    quote = message.text.lower().strip()
    text = 'Сколько конвертировать:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)


def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        total_base = CriptoConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации: \n{e} ")
    else:
        text = f"Цена {amount} {base} в {quote} = {total_base}"
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.lower().split()
    try:
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров.')
        base, quote, amount = values
        total_base = CriptoConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
