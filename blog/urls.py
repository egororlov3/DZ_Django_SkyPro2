from django.urls import path

from .apps import BlogConfig
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView
)

app_name = BlogConfig.name

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_list'),
    path('create/', BlogPostCreateView.as_view(), name='blog_create'),
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='blog_detail'),
    path('<slug:slug>/edit/', BlogPostUpdateView.as_view(), name='blog_update'),
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='blog_delete'),
]