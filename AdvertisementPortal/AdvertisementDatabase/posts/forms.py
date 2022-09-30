from django.forms import ModelForm, CharField, ChoiceField, Textarea
from .models import Post, POST_CATEGORIES, Reply
from django_summernote.widgets import SummernoteWidget

class PostForm(ModelForm):
    header = CharField(max_length=255,
                       label='Заголовок')
    text = CharField(max_length=1000,
                     label='Текст',
                     widget=SummernoteWidget())
    category = ChoiceField(choices=POST_CATEGORIES,
                           label='Категория объявления')


    class Meta:
        model = Post
        fields = ['header', 'text', 'category']


class ReplyForm(ModelForm):
    text = CharField(max_length=255,
                     label='Текст',
                     widget=Textarea())

    class Meta:
        model = Reply
        fields = ['text']
