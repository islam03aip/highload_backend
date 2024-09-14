from django.db import models
from datetime import date
from django.utils.timezone import now
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=3000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
