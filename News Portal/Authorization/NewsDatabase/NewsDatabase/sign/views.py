from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from .forms import BaseRegisterForm


@login_required
def upgrade_user(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'
