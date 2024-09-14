from django.contrib import admin
from .models import Post, Comment
# Register your models here.



class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ['title']
    
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)