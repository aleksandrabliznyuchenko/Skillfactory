from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import View, CreateView
from .forms import BaseRegisterForm

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from news.tokens import account_activation_token
from news.models import Account, Author

import logging

logger = logging.getLogger(__name__)


@login_required
def upgrade_user(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context


class ActivateAccountView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            account = Account.objects.get(user=uid)
        except (TypeError, ValueError, OverflowError):
            account = None

        if account is not None and account_activation_token.check_token(account.user, token):
            account.is_confirmed = True
            account.save()
        return redirect('/')
