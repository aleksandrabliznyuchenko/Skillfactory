from django.views.generic import ListView, DetailView
from .models import Post


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')


# создаём представление, в котором будут детали конкретного отдельного товара
class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
