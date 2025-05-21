from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.views.generic import (ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

from .filters import PostFilter
from .forms import PostForm, NewsSearchForm
from .models import Post, Category, PostCategory
from .tasks import send_notifications_subscribers_categories, send_out_weekly


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

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


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

# при событии m2m_changed (поле ManyToManyField модели Post) присваивания Post какой-либо Category
@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    # функция срабатывает только если присваивание Category происходит при создании Post
    if kwargs['action'] == 'post_add':
        # составляем список подписчиков на данную Category
        categories = instance.categories.all()
        subscribers = []

        for cat in categories:
            subscribers += cat.subscribers.all()

        # вызываем задачу send_notifications_subscribers_categories из news/tasks.py
        send_notifications_subscribers_categories(instance.preview(), instance.pk, instance.title, set(subscribers))
        # для проверки отправки сообщений так же вызываем задачу send_out_weekly из news/tasks.py
        send_out_weekly()