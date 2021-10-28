import requests
import json
import pymorphy2

from config import currency, KEY


class ConversionException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        def check_parameters(quote: str, base: str, amount: str):
            try:
                quote = MorphoConverter.normal(quote)
            except:
                raise ConversionException(f"Не удалось обработать валюту {quote}.")

            try:
                base = MorphoConverter.normal(base)
            except:
                raise ConversionException(f"Не удалось обработать валюту {base}.")

            if quote == base:
                raise ConversionException(f"Укажите две разные валюты из списка /values.")

            try:
                quote_ticker = currency[quote]
            except KeyError:
                raise ConversionException(f"Валюта {quote} не найдена в списке доступных валют.\n"
                                          f"Для просмотра списка валют введите команду /values")

            try:
                base_ticker = currency[base]
            except KeyError:
                raise ConversionException(f"Валюта {base} не найдена в списке доступных валют.\n"
                                          f"Для просмотра списка валют введите команду /values")

            try:
                amount = float(amount)
            except:
                raise ConversionException(f"Не удалось обработать количество {amount}.")

            if amount <= 0:
                raise ConversionException("Количество валюты должно быть больше 0.")
            return quote_ticker, base_ticker, amount

        quote_ticker, base_ticker, amount = check_parameters(quote, base, amount)
        query = f"{quote_ticker}_{base_ticker}"
        r = requests.get(f'https://free.currconv.com/api/v7/convert?q={query}&compact=ultra&apiKey={KEY}')
        price = json.loads(r.content)[query]
        price = price * amount
        return price


class MorphoConverter:
    """
    Морфологическая обработка подаваемых на вход названий валют с помощью библиотеки pymorphy
    Приведение названий валют к нормальной форме ("доллары" -> "доллар"),
    а также склонение названий валют по падежам (чтобы вместо строки "Цена 100 доллар" бот выводил "Цена 100 долларов")
    """
    @staticmethod
    def normal(currency_name: str):
        morph = pymorphy2.MorphAnalyzer()
        p = morph.parse(currency_name)[0]
        return p.normal_form

    @staticmethod
    def convert(quote: str, base: str, plur: bool):
        morph = pymorphy2.MorphAnalyzer()
        quote_sg = morph.parse(quote)[0]
        base_sg = morph.parse(base)[0]
        quote_name = quote_sg.inflect({'gent', 'plur'}) if plur else quote_sg.inflect({'gent'})
        base_name = base_sg.inflect({'loct', 'plur'})
        return quote_name.word, base_name.word
