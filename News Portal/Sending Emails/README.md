## Новостная рассылка.  
  
Добавлена новая страница подписки на новостные категории, открывающаяся по кнопке "Подписаться на рассылку" на личной странице пользователя.  
Пользователь может подписаться на любимые новостные категории и повещать оповещение на почту при добавлении статей из этих категорий.  
  
Добавлена новая модель *Profile* для управления личным профилем пользователя, с полями:  
* *user* - ссылка на пользователя  
* *category* - категории, на которые подписан пользователь  
* *is_confirmed* - подтверждён ли email пользователя  
* *created_datetime* - дата и время создания профиля  
  
Также теперь при создании новой страницы пользователя ему отправляется сообщение со ссылкой на подтверждение email-а. 
