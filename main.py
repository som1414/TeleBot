import telebot
from config import currencies, TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать дайте команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nЧтобы увидеть список доступных валют введите: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currencies.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверное колличество параметров')

        answer = CurrencyConverter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка в запросе\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Неизвестная ошибка\n{e}')
    else:
        bot.send_message(message.chat.id, answer)


bot.polling()
