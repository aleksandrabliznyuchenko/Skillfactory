from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User

from posts.models import Account, Author, Reply, Post
from .filters import PostFilter, ReplyFilter

import logging

logger = logging.getLogger(__name__)


@login_required
def accept_reply(request, **kwargs):
    reply = Reply.objects.get(pk=kwargs.get('pk'))
    reply.is_accepted = True
    reply.save(update_fields=['is_accepted'])
    return redirect('/replies/')


@login_required
def decline_reply(request, **kwargs):
    reply = Reply.objects.get(pk=kwargs.get('pk'))
    reply.is_accepted = False
    reply.save(update_fields=['is_accepted'])
    return redirect('/replies/')


@login_required
def delete_reply(request, **kwargs):
    reply = Reply.objects.get(pk=kwargs.get('pk'))
    reply.delete()
    return redirect('/replies/')


@login_required
def delete_my_reply(request, **kwargs):
    reply = Reply.objects.get(pk=kwargs.get('pk'))
    reply.delete()
    return redirect('/my_replies/')


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        if Account.objects.filter(user=self.request.user).exists():
            context['is_confirmed'] = Account.objects.get(user=self.request.user.id).is_confirmed
        return context


class PersonalPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'accounts/personal_posts.html'
    context_object_name = 'personal_posts'
    ordering = ['-id']
    paginate_by = 10

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        qs = self.get_filter().qs.filter(author=Author.objects.get(user=self.request.user.id))
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.get_filter()
        context['filter'] = filter
        filter_params = ""
        for f_name in [str(k) for k in filter.filters]:
            if f_name in filter.data:
                filter_params += f"&{f_name}={filter.data[f_name]}"
        context['filter_params'] = filter_params
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context


class PersonalReplyListView(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'accounts/personal_replies.html'
    context_object_name = 'personal_replies'
    ordering = ['-id']
    paginate_by = 10

    def get_filter(self):
        return ReplyFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        qs = self.get_filter().qs.filter(author=Author.objects.get(user=self.request.user.id))
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.get_filter()
        context['filter'] = filter
        filter_params = ""
        for f_name in [str(k) for k in filter.filters]:
            if f_name in filter.data:
                filter_params += f"&{f_name}={filter.data[f_name]}"
        context['filter_params'] = filter_params
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context


class ReplyListView(LoginRequiredMixin, ListView):
    model = Reply
    template_name = 'accounts/reply_list.html'
    context_object_name = 'reply_list'
    ordering = ['-id']
    paginate_by = 10

    def get_filter(self):
        return ReplyFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        posts = Post.objects.filter(author=Author.objects.get(user=self.request.user.id))
        qs = self.get_filter().qs.filter(post__id__in=posts)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.get_filter()
        context['filter'] = filter
        filter_params = ""
        for f_name in [str(k) for k in filter.filters]:
            if f_name in filter.data:
                filter_params += f"&{f_name}={filter.data[f_name]}"
        context['filter_params'] = filter_params
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context
