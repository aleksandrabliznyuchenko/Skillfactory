## Авторизация и аутентификация на новостном портале.  
  
Добавлен функционал регистрации на сайте - либо через email с паролем, либо через Google-аккаунт.  
Пользователи сайта разделены на две группы - *common* (обычные пользователи) и *authors* (авторы).  
При регистрации пользователь автоматически добавляется в группу *common*.  
  
Пользователи группы *common* имеют доступ к общему списку статей, странице поиска, а также к страницам статей.  
Пользователи группы *authors* могут создавать, редактировать и удалять статьи.  
  
Все материалы портала доступны только авторизованным пользователям - при попытке перехода на какую-нибудь страницу пользователю предложат войти в его аккаунт/зарегистрироваться.  
Для доступа к аккаунту (пока шаблонному) на главную страницу добавлена кнопка "Мой аккаунт". На странице аккаунта размещены кнопки "Перейти к новостям", "Выйти", 
а также кнопка "Стать автором" для пользователей, не принадлежащих к группе *authors*.
