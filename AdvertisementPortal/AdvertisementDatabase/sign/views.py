from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.generic.edit import View, CreateView
from .forms import BaseRegisterForm

from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from posts.tokens import account_activation_token
from posts.models import Account, Author

import logging

logger = logging.getLogger(__name__)


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/posts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
        new_author = Author(user=self.request.user)
        new_author.save()
        return redirect('/posts/')

class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            account = Account.objects.get(user=uid)
        except (TypeError, ValueError, OverflowError):
            account = None

        if account is not None and account_activation_token.check_token(account.user, token):
            account.is_confirmed = True
            account.save()
        return redirect('/')
