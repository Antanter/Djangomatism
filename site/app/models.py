from django.db import models
from django.contrib.auth.models import User
from .src.censorer import Censorer

class Post(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text}"

    def save(self, *args, **kwargs):
        self.text = Censorer.censor_text(self.text)
        super().save(*args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"""{self.user.username} have liked post "{self.post.text}", made by {self.post.user} ({self.created_at.ctime()})"""

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""{self.user.username} have create comment "{self.text}" to post "{self.post.text}", made by {self.post.user} ({self.created_at.ctime()})"""
    
    def save(self, *args, **kwargs):
        self.text = Censorer.censor_text(self.text)
        super().save(*args, **kwargs)