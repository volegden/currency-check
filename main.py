# 01.10.21
# Denis 'Volegden' Volegov

import telebot
import config
from extensions import ConvertionException, Converter

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_command(message):
    bot.send_message(message.chat.id, f"To check the currency price please use following format: \n\
<base currency> <currency to change to> <amount of base currency>. \n\
Example: usd eur 100. \n\n\
List of available currencies in /values command. ")


@bot.message_handler(commands=['values'])
def values_command(message):
    values_command_text = "List of available currencies: "
    for each_currency in config.list_of_currencies.keys():
        values_command_text = '\n'.join((values_command_text, each_currency))
    bot.send_message(message.chat.id, values_command_text)


@bot.message_handler(content_types=['text'])
def convert_values(message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise ConvertionException("Invalid number of parameters. Must be 3.")
        quote, base, amount = values
        total = Converter.get_price(quote, base, amount)

    except ConvertionException as e:
        bot.send_message(message.chat.id, f"Error.\n{e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Failed to process command.\n{e}")

    else:
        reply_result = f"Price {amount} {quote} in {base} — {total * float(amount)}"
        bot.send_message(message.chat.id, reply_result)


bot.polling(none_stop=True)
