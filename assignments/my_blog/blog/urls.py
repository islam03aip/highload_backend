from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',print_hello),
    path('blogs/', list_blogs, name='home'),
    path('blogs/<int:id>/', get_blog, name="blog_detail"),
    path('remove_blog/<int:id>/', delete_blog, name="delete_blog"),
    path('add_blogs/', add_blog, name='add_blog'),
    path('edit_blog/<int:id>/', edit_blog, name='edit_blog'),
    path('add_comment/<int:id>/', add_comment, name='add_comment'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
]
