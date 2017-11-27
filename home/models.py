from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Post(models.Model):
    title = models.CharField(max_length=1000)
    post = models.TextField(max_length=5000)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField()
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('home:single_post',kwargs={'pk':self.pk})

    def __str__(self):
        return str(self.pk)+" "+str(self.title) + " - "+ str(self.author)


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    author_id = models.IntegerField()
    date = models.DateTimeField()
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)

    def __str__(self):
        return self.comment

class Reply(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    reply = models.CharField(max_length=1000)
    author_id = models.IntegerField()
    date = models.DateTimeField()
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)

    def __str__(self):
        return self.reply

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return  self.name

class PostTag(models.Model):
    post_id = models.IntegerField()
    tag_id = models.IntegerField()