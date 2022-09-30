from django_filters import FilterSet, CharFilter, DateFilter, ChoiceFilter
from posts.models import Reply, Post, POST_CATEGORIES


class PostFilter(FilterSet):

    author_filter = CharFilter(field_name='author__user__username',
                               lookup_expr='icontains',
                               label='По автору')
    header_filter = CharFilter(field_name='header',
                               lookup_expr='icontains',
                               label='По заголовку')
    date_filter = DateFilter(field_name='created_datetime',
                             lookup_expr='gt',
                             label='Опубликовано позднее')
    category_filter = ChoiceFilter(choices=POST_CATEGORIES,
                               field_name='category',
                               label='Категория',
                               empty_label='Все')

    class Meta:
        model = Post
        fields = (
            'author_filter', 'header_filter', 'date_filter', 'category_filter'
        )


class ReplyFilter(FilterSet):

    author_filter = CharFilter(field_name='author__user__username',
                               lookup_expr='icontains',
                               label='По автору объявления')
    reply_filter = CharFilter(field_name='text',
                               lookup_expr='icontains',
                               label='По ключевому слову отклика')
    header_filter = CharFilter(field_name='post__header',
                               lookup_expr='icontains',
                               label='По заголовку объявления')
    date_filter = DateFilter(field_name='post__created_datetime',
                             lookup_expr='gt',
                             label='Объявление опубликовано позднее')
    category_filter = ChoiceFilter(choices=POST_CATEGORIES,
                               field_name='post__category',
                               label='Категория объявления',
                               empty_label='Все')

    class Meta:
        model = Reply
        fields = (
            'author_filter', 'reply_filter', 'header_filter',
            'date_filter', 'category_filter'
        )
