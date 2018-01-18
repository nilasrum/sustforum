import json
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from channels import Group
from .settings import MSG_TYPE_MESSAGE
from django.http import JsonResponse

class Post(models.Model):
    title = models.TextField(max_length=1000)
    post = models.TextField(max_length=5000)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('home:single_post',kwargs={'post_id':self.pk})

    def __str__(self):
        return str(self.pk)+" "+str(self.title) + " - "+ str(self.author)


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000)
    author_id = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('home:single_post',kwargs={'post_id':self.post.pk})

    def get_last_id(self):
        response = {
            'id':self.id,
            'propic':UserInfo.objects.get(user=self.author_id).propic.url
        }
        return JsonResponse(response)

    def __str__(self):
        return str(self.pk)+" "+self.comment

class Reply(models.Model):
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    reply = models.TextField(max_length=1000)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField()
    vote = models.IntegerField(default=0)

    def __str__(self):
        return self.reply+" "+self.user.username

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return  self.name

class PostTag(models.Model):
    post_id = models.IntegerField()
    tag_id = models.IntegerField()

class PostVote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post_id = models.IntegerField()
    vote_type = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)+" "+str(self.post_id)+" "+str(self.vote_type)

    def get_absolute_url(self):
        return reverse('home:single_post',kwargs={'post_id':self.post_id})

class PostFollowed(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post_id = models.IntegerField()

    def __str__(self):
        return str(self.user)+" "+str(self.post_id)

    def get_absolute_url(self):
        return reverse('home:single_post',kwargs={'post_id':self.post_id})

class CommentVote(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post_id = models.IntegerField()
    cmnt_id = models.IntegerField()
    vote_type = models.IntegerField(default=0)
    vote = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)+" "+str(self.cmnt_id)+" "+str(self.vote_type)

    def get_absolute_url(self):
        return reverse('home:single_post',kwargs={'post_id':self.post_id})


class Room(models.Model):
    """
    A room for people to chat in.
    """
    title = models.CharField(max_length=255)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("room-%s" % self.id)

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        """
        Called to send a message to the room on behalf of a user.
        """
        final_msg = {'room': str(self.id), 'message': message, 'username': user.username, 'msg_type': msg_type}

        # Send out the message to everyone in the room
        self.websocket_group.send(
            {"text": json.dumps(final_msg)}
        )

class UserInfo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255,default="not set")
    lastname = models.CharField(max_length=255,default="not set")
    propic = models.FileField(default='default.png',blank=True)
    profession = models.CharField(max_length=255,blank=True)
    color = models.CharField(max_length=255,default="#46b8da")

    def __str__(self):
        return "info : "+self.firstname

    def get_absolute_url(self):
        return reverse('home:profile',kwargs={'user_id':self.user.pk})