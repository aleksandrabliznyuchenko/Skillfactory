from django.urls import path
from .views import AccountView, PersonalPostListView, PersonalReplyListView, ReplyListView, \
    accept_reply, delete_reply, decline_reply, delete_my_reply
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60 * 15)(AccountView.as_view()), name='account'),  # ссылка на страницу пользователя
    # ссылка на объявления пользователя
    path('my_posts/', PersonalPostListView.as_view(), name='my_posts'),

    # ссылка на отклики пользователя
    path('my_replies/', PersonalReplyListView.as_view(), name='my_replies'),
    path('my_replies/delete/<int:pk>', delete_my_reply, name='delete_my_reply'),  # удалить отклик

    # ссылка на отклики, которые оставили пользователю
    path('replies/', ReplyListView.as_view(), name='replies'),
    path('replies/accept/<int:pk>', accept_reply, name='accept'),  # принять отклик
    path('replies/decline/<int:pk>', decline_reply, name='decline'),  # отклонить принятый отклик
    path('replies/delete/<int:pk>', delete_reply, name='delete'),  # удалить отклик
]
