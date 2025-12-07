from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_post')
    content = models.TextField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, null=True, blank=True, related_name='user_likes')

    @property
    def date(self):
        return self.created.strftime("%B %d, %Y, %H:%M %p").replace("AM", "a.m.").replace("PM", "p.m.")

    @property
    def no_likes(self):
        return len(self.likes.all())

    def __str__(self):
        return f'Post by {self.author} on {self.date}'