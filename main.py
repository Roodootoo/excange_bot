import requests
import telebot
from auth_data import token


def get_data(currency_from, currency_to):
    response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{currency_from.upper()}').json()
    currencies = response.get('rates').get(currency_to.upper())
    return f'USD/{currency_to.upper()} = {currencies}'


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Hello! Lets check currencies')

    @bot.message_handler(content_types=['text'])
    def send_tex(message):
        if message.text.lower() == 'rub':
            try:
                sell_exchange = get_data(message.text)
                bot.send_message(message.chat.id, sell_exchange)
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, 'Something was wrong..')
        else:
            bot.send_message(message.chat.id, 'Not understood..')

    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)
