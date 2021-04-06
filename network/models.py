from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class UserUser(models.Model):
    follower = models.ManyToManyField("User", related_name="followers")
    following = models.ManyToManyField("User", related_name="followings")

    def __str__(self):
        return f"{self.follower}"


class Post(models.Model):
    author = models.ForeignKey("User", on_delete=models.PROTECT, related_name="posted")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.body}"

    def serialize(self):
        return {
            "id": self.id,
            "author": self.author.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }


class Like(models.Model):
    liker = models.ForeignKey("User", on_delete=models.CASCADE, related_name="likers")
    post = models.ManyToManyField("Post", blank=True, related_name="post_likes")

    def __str__(self):
        post = ", ".join(str(p) for p in self.post.all())
        return "{} >> {}".format(self.liker, post)