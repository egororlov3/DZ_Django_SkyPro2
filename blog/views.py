from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
from .forms import BlogPostForm


# Список постов
class BlogPostListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    queryset = BlogPost.objects.filter(is_published=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perms'] = self.request.user.get_all_permissions()
        return context


# Детали поста
class BlogPostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.views += 1
        post.save()

        if post.views == 100:
            self.send_email_notification(post)

        return post

    def send_email_notification(self, post):
        subject = f"Пост '{post.title}' достиг 100 просмотров!"
        message = f"Ваш пост '{post.title}' набрал 100 просмотров."
        from_email = 'sidxxx3@yandex.ru'
        recipient_list = ['erop.orl@gmail.com']

        send_mail(subject, message, from_email, recipient_list)


# Создание поста
class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    permission_required = 'blog.add_post'
    template_name = 'blog/blog_form.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:blog_list')


# Обновление поста
class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    permission_required = 'blog.change_post'
    template_name = 'blog/blog_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        return context


# Удаление поста
class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')
    permission_required = 'blog.delete_post'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return BlogPost.objects.get(slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.get_object()
        return context
