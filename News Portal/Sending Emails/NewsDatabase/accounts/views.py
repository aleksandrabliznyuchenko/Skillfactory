from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .forms import CategorySubscriptionForm
from news.models import Account


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        if Account.objects.filter(user=self.request.user).exists():
            context['is_confirmed'] = Account.objects.get(user=self.request.user.id).is_confirmed
        return context


class CategoryView(LoginRequiredMixin, CreateView):
    template_name = 'accounts/category_subscription.html'
    form_class = CategorySubscriptionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
        categories = request.POST.getlist('category')
        categories_id_list = [int(c) for c in categories]

        # если пользователь уже подписан на категории, обновим список категорий в подписке
        # если пользователь ни на что не подписан, создадим подписку
        if (Account.objects.filter(user=self.request.user).exists()):
            user_subscription = Account.objects.get(user=self.request.user)
            user_subscription.category.set(categories_id_list)
        else:
            user_cat = Account(user=self.request.user)
            user_cat.save()
            user_cat.category.set(categories_id_list)
        return redirect('/')
