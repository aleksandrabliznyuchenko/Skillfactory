# копия фильтра из предыдущего проекта - он "цензурирует" тексты объявлений
from django import template
import re

restricted_lexicon = ['fuck', 'дурак', 'идиот', 'бойкот', 'сука']

register = template.Library()


@register.filter(name='censor')
def Censor(text: str):
    for word in restricted_lexicon:
        text = re.sub(word, "#" * len(word), text)
    return text