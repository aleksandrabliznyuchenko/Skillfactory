from django.urls import path
from .views import AccountView, CategoryView

urlpatterns = [
    path('', AccountView.as_view(), name='account'),  # ссылка на страницу пользователя
    path('subscription/', CategoryView.as_view(), name='category_subscription')
    # ссылка на страницу с пподпиской на рассылку
]
