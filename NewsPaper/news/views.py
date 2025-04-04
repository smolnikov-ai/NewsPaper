from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

from .forms import PostForm, NewsSearchForm
from .models import Post, Category
from .filters import PostFilter


class PostsList(ListView):
    model = Post
    ordering = '-date_time_in'
    template_name = 'flatpages/posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset

        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


def news_search(request):
    form = NewsSearchForm(request.GET)  # Заполняем форму данными из GET-запроса
    news = Post.objects.all()  # Получаем все новости (изначально)

    if form.is_valid():
        title = form.cleaned_data.get('title')
        author = form.cleaned_data.get('author')
        date_after = form.cleaned_data.get('date_after')

        # Фильтрация
        if title:
            news = news.filter(title__icontains=title)  # Поиск по названию

        if author:
            news = news.filter(
                author__user__username__icontains=author)  # Поиск по автору (предполагается поле author в модели)

        if date_after:
            news = news.filter(date_time_in__gte=date_after)  # Дата позже указанной

    context = {
        'form': form,
        'news': news,
    }
    return render(request, 'post_search.html', context)


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/create/':
            post.type = 'NW'
        elif self.request.path == '/articles/create/':
            post.type = 'AR'
        post.save()
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryList(ListView):
    model = Post
    ordering = '-date_time_in'
    template_name = 'categories.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category).order_by('-date_time_in')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context



# Представление для подписки User на Category
@login_required
def subscribe(request, pk):
    category = Category.objects.get(id=pk)
    user = request.user
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку постов категории '

    return render(request, 'category_subscribe.html', {'category': category, 'message': message})