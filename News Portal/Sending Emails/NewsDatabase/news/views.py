from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Post, User
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-id']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'posts_search'
    ordering = ['-id']
    paginate_by = 10

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        qs = self.get_filter().qs
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


class PostDetail(LoginRequiredMixin, DetailView):
    template_name = 'flatpages/post_detail.html'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'flatpages/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'flatpages/post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'flatpages/post_delete.html'
    queryset = Post.objects.all()
    permission_required = ('news.delete_post',)
    success_url = '/news/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authorized'] = User.objects.get(pk=self.request.user.id)
        return context
