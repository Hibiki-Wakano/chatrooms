from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    user_name = models.CharField(max_length=100, default=" ")
    memo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name

class Connect(models.Model):
    follow = models.ForeignKey(CustomUser, related_name='follow', on_delete=models.CASCADE)
    follower = models.ForeignKey(CustomUser, related_name='follower', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        display= str(self.follow) + " ⇒ " + str(self.follower)
        return display

class Block(models.Model):
    block = models.ForeignKey(CustomUser, related_name='block', on_delete=models.CASCADE)
    blocked = models.ForeignKey(CustomUser, related_name='blocked', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        display= str(self.block) + " ⇒ " + str(self.blocked)
        return display


class Room(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='room', height_field=None, width_field=None, blank=True, max_length=100, default=False)#サムネ

    def __str__(self):
        return self.title
    


class Post(models.Model):
    text = models.TextField()
    user = models.ForeignKey(CustomUser, related_name='post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, related_name='post', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.user.user_name + ' < ' + self.text + ' at ' +self.room.title
    
    image = models.ImageField(upload_to='post', height_field=None, width_field=None, blank=True, max_length=100, default=False)

class Message(models.Model):
    text = models.TextField()
    send_to = models.ForeignKey(CustomUser, related_name='received', on_delete=models.CASCADE)
    send_from = models.ForeignKey(CustomUser, related_name='sent', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)