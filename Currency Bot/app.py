import telebot

from config import TOKEN, currency
from extensions import ConversionException, CurrencyConverter, MorphoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands='start')
def greeting(message: telebot.types.Message):
    text = 'Вас приветствует бот, конвертирующий валюты!\n' \
           'Чтобы начать конвертацию, введите команду следующего формата:\n' \
           '<валюта для конвертации> <валюта, в которую конвертируем> <количество валюты>\n' \
           '(например, чтобы перевести 1 евро в доллары, введите ' \
           '"евро доллар 1")\n\n ' \
           'Чтобы получить список всех доступных к конвертации валют, ' \
           'введите команду /values \n\n' \
           'Чтобы ознакомиться с инструкцией, введите команду /help'
    bot.reply_to(message, text)


@bot.message_handler(commands='help')
def instruction(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию валют, введите команду следующего формата:\n' \
           '<валюта для конвертации> <валюта, в которую конвертируем> <количество валюты>\n' \
           '(например, чтобы перевести 1 евро в доллары, введите ' \
           '"евро доллар 1")\n\n ' \
           'Чтобы получить список всех доступных к конвертации валют, ' \
           'введите команду /values \n\n' \
           'Чтобы ещё раз ознакомиться с инструкцией, введите команду /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Список валют:"
    for key in currency.keys():
        text = "\n- ".join((text, key.capitalize()))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')
        if len(values) != 3:
            raise ConversionException("Неверное количество параметров.\n"
                                      "Для конвертации валюты введите команду вида\n"
                                      "<валюта для конвертации> <валюта, в которую конвертируем> <количество валюты>")

        quote, base, amount = values
        price = CurrencyConverter.convert(quote, base, amount)
    except ConversionException as ce:
        bot.reply_to(message, f"Ошибка пользователя.\n{ce}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        quote_name, base_name = MorphoConverter.convert(quote, base, (float(amount) > 1))
        reply = f"Цена {amount} {quote_name} в {base_name} : {price}"
        bot.send_message(message.chat.id, reply)


bot.polling()
