from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, \
    CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, User, Reply, Author
from .forms import PostForm, ReplyForm
from django.core.cache import cache

import logging

logger = logging.getLogger(__name__)


class PostList(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.id:
            context['is_authorized'] = User.objects.get(pk=self.request.user.id)
            context['current_user_id'] = self.request.user.id
        return context


class PostDetail(DetailView):
    template_name = 'posts/post_detail.html'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object()
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.id:
            user = User.objects.get(pk=self.request.user.id)
            post_author_user_id = Post.objects.get(pk=self.kwargs.get('pk')).author.user.id
            context['is_authorized'] = user
            context['is_author'] = (post_author_user_id == user.id)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'posts/post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
        post_header = request.POST.get('header')
        post_text = request.POST.get('text')
        post_cat = request.POST.get('category')
        author = Author.objects.get(user=self.request.user)
        new_post = Post(author=author, header=post_header, text=post_text, category=post_cat)
        new_post.save()
        return redirect('/posts/')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'posts/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context


class ReplyCreateView(LoginRequiredMixin, CreateView):
    template_name = 'replies/reply_create.html'
    form_class = ReplyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
        reply_text = request.POST.get('text')
        p = Post.objects.get(pk=self.kwargs.get('pk'))
        author = Author.objects.get(user=self.request.user)
        new_reply = Reply(author=author, post=p, text=reply_text)
        new_reply.save()
        return redirect('/posts/')
