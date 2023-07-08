import telebot

from config import keys, TOKEN
from extensions import ConvertionException, CriptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет, это бот позволяющий узнавать информацию о \n' \
           'текущих курсах валют, поможет перевести одну валюту  \n' \
           'в другую согласно текущему курсу. \n' \
           'Чтобы получить подробную инструкцию введите: /help\n' \
           'Чтобы увидеть список доступных валют введите: /values\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['help']) # TODO Сделать кнопкой
def help(message: telebot.types.Message):
    text = 'Бот понимает команду в следующем формате: \n' \
           '<имя валюты> <в какую перевести> <сколько перевести> \n' \
           'Например: доллар рубль 10 \n' \
           'Чтобы увидеть список доступных валют введите: /values\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values']) # TODO Сделать кнопкой
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split()
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров.')
        quote, base, amount = values
        total_base = CriptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
