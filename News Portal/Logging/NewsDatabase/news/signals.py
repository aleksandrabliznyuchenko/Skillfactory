from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from allauth.account.signals import user_signed_up

from .tokens import account_activation_token
from .models import User, Post, Account, Category, POST_TYPES
from NewsDatabase.settings import DOMAIN, DEFAULT_FROM_EMAIL


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        instance.account.save()


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    current_site = get_current_site(request)

    html_content = render_to_string(
        'email/confirm_registration.html',
        {
            'user' : user,
            'domain' : "%s:8000" % current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : account_activation_token.make_token(user),
         }
    )

    msg = EmailMultiAlternatives(
        subject="Добро пожаловать на новостной портал",
        body="",
        from_email=DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(m2m_changed, sender=Post.category.through)
def notify_new_post(instance, action, pk_set, **kwargs):
    recipients = []
    post_type = ""

    if action == 'post_add':
        for type in POST_TYPES:
            if instance.type in type:
                post_type = type[1]

        html_content = render_to_string(
            'email/new_post.html',
            {
                'post': instance,
                'post_type': post_type,
                'domain': DOMAIN
            }
        )

        subject = f'Добавлена новая статья автора {instance.author.user.username} "{instance.header}"'
        for pk in pk_set:
            category = Category.objects.get(pk=pk)
            subscribers = Account.objects.filter(category=category)
            recipients = [subscriber.user.email for subscriber in subscribers]

        msg = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email=DEFAULT_FROM_EMAIL,
            to=recipients
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
