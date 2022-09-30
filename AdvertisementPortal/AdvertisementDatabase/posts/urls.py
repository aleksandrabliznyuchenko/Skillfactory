from django.urls import path
from .views import PostList, PostDetail, PostCreateView, PostDeleteView, ReplyCreateView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(10)(PostList.as_view()), name='overview'),  # Ссылка на страницу с общим списком новостей
    path('<int:pk>/', cache_page(30)(PostDetail.as_view()), name='post_detail'),  # Ссылка на страницу новости
    path('add/', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание новости
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),  # Ссылка на удаление новости
    path('<int:pk>/reply_create', ReplyCreateView.as_view(), name='reply_create'),  # Ссылка на создание новости
]