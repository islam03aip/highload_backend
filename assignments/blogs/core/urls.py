from django.contrib import admin
from django.urls import path, include
from .views import post_list, post_detail, add_comment, blog_list, blog_detail

urlpatterns = [
    path('', post_list),
    path('<int:post_id>', post_detail, name="post_detail"),
    path('<int:post_id>/add_comment', add_comment, name='add_comment'),
]