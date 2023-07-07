import telebot
import requests
import json

TOKEN = "6290467291:AAG2ThBZgOx-WQ_FbwfuNLsfgWnwKgJFI-c"
bot = telebot.TeleBot(TOKEN)

# @bot.message_handler()
# def echo_test(message: telebot.types.Message):
#     bot.send_message(message.chat.id, 'hello')
keys = {
    'биткоин': 'BTC',
    'эфириум': 'ETH',
    'доллар': 'USD',
    'рубль': 'RUB',
    'евро': 'EUR',
}


class ConvertionException(Exception):
    pass


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу дайте команду боту в следующем формате: \n' \
           '<имя валюты> <в какую волюту перевести> <количество валюты> \n' \
           'Чтобы увидеть список доступных валют введите: /values\n'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    if len(values) != 3:
        raise ConvertionException('Неверное количество параметров.')
    quote, base, amount = values
    if quote == base:
        raise ConvertionException(f'Валюты не должны быть одинаковыми {base}.')

    try:
        quote_ticker = keys[quote]
    except KeyError:
        raise ConvertionException(f'Валюта {quote} не найдена.')

    try:
        base_ticker = keys[base]
    except KeyError:
        raise ConvertionException(f'Валюта {base} не найдена.')

    try:
        amount = float(amount)
    except ValueError:
        raise ConvertionException(f'Неверное значение {amount}.')

    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
    total_base = json.loads(r.content)[keys[base]]
    text = f'Цена {amount} {quote} в {base} = {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling()
