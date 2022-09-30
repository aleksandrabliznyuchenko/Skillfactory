from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from allauth.account.signals import user_signed_up

from .tokens import account_activation_token
from .models import User, Reply, Account
from AdvertisementDatabase.settings import DOMAIN, DEFAULT_FROM_EMAIL


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        instance.account.save()


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    current_site = get_current_site(request)

    html_content = render_to_string(
        'email/confirm_account.html',
        {
            'user': user,
            'domain': "%s:8000" % current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
    )

    msg = EmailMultiAlternatives(
        subject="Добро пожаловать в мир RPG",
        body="",
        from_email=DEFAULT_FROM_EMAIL,
        to=[user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Reply)
def notify_new_reply(instance, created, update_fields, **kwargs):
    if created:
        html_content = render_to_string(
            'email/new_reply.html',
            {
                'reply': instance,
                'post': instance.post,
                'domain': DOMAIN
            }
        )

        subject = f'Вы получили новый отклик на объявление "{instance.post.header}"'
        recipient = instance.post.author.user.email

        msg = EmailMultiAlternatives(
            subject=subject,
            body="",
            from_email=DEFAULT_FROM_EMAIL,
            to=[recipient]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    else:
        for field in update_fields:
            if field == 'is_accepted':
                if instance.is_accepted:
                    html_content = render_to_string(
                        'email/reply_accepted.html',
                        {
                            'post': instance.post,
                            'domain': DOMAIN
                        }
                    )
                    subject = f'Ваш отклик на объявление "{instance.post.header}" принят'
                else:
                    html_content = render_to_string(
                        'email/reply_declined.html',
                        {
                            'post': instance.post,
                            'domain': DOMAIN
                        }
                    )

                    subject = f'Ваш отклик на объявление "{instance.post.header}" отклонён'

                recipient = instance.author.user.email
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body="",
                    from_email=DEFAULT_FROM_EMAIL,
                    to=[recipient]
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()
