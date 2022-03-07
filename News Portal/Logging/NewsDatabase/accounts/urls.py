from django.urls import path
from .views import AccountView, CategoryView
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(AccountView.as_view()), name='account'),  # ссылка на страницу пользователя
    path('subscription/', cache_page(60*5)(CategoryView.as_view()), name='category_subscription')
    # ссылка на страницу с пподпиской на рассылку
]
