from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    user_name = models.CharField(max_length=100, default="no name")
    memo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.ImageField(upload_to='icon', height_field=None, width_field=None, blank=True, max_length=100, default=False)
    icon_changed = models.DateTimeField(blank=True, auto_now=True)
    def __str__(self):
        return self.user_name
    
    REQUIRED_FIELDS = ["user_name","memo"]
    groups = None
    user_permissions = None
    last_login = None
    #superuser_status = False
    first_name = None
    last_name = None
    email_address = models.EmailField(default='notset@example.com')
    #staff_status = False
    date_joined = None

class Config(models.Model):
    open_config = [
        (0,'全体に公開する'),
        (1,'フレンドのみ公開'),
        (2,'非公開')
    ]
    receive_config = [
        (0,'全員に許可する'),
        (1,'フレンドのみ許可'),
        (2,'全員から受け取らない')
    ]

    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    darkmode = models.BooleanField(default=False,blank=False)
    room_post_log = models.IntegerField(choices=open_config, default=0)
    friend = models.IntegerField(choices=open_config, default=0)
    notice = models.IntegerField(choices=receive_config, default=0)
    message = models.IntegerField(choices=receive_config, default=0)

class Message(models.Model):
    sent = models.ForeignKey(CustomUser, related_name='sent_message', on_delete=models.CASCADE)
    received = models.ForeignKey(CustomUser, related_name='received_message', on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='messasge', height_field=None, width_field=None, blank=True, max_length=100, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    cancel = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Notice(models.Model):
    kind_list=[
        (0,'system notice'),
        (1,'important or fatal notice in system notice'),
        (2,'notice from other users'),
    ]
    user = models.ForeignKey(CustomUser, related_name='notice', on_delete=models.CASCADE)
    kind = models.IntegerField(choices=kind_list,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    text = models.TextField()


class Connect(models.Model):
    follow = models.ForeignKey(CustomUser, related_name='follow', on_delete=models.CASCADE)
    follower = models.ForeignKey(CustomUser, related_name='follower', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): #admin上の表示設定
        display= str(self.follow) + " ⇒ " + str(self.follower)
        return display
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["follow", "follower"],name="connect_unique"),
        ]


class Block(models.Model):
    block = models.ForeignKey(CustomUser, related_name='block', on_delete=models.CASCADE)
    blocked = models.ForeignKey(CustomUser, related_name='blocked', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        display= str(self.block) + " ⇒ " + str(self.blocked)
        return display
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["block", "blocked"],name="block_unique"),
        ]

class Room(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='room', height_field=None, width_field=None, blank=True, max_length=100, default=False)#サムネ

    def __str__(self):
        return self.title
    
    def savePath(instance, filename):
        ext = filename.split('.')[-1]
        return f'room/{instance.id}.{ext}'
    


class Post(models.Model):
    text = models.TextField()
    user = models.ForeignKey(CustomUser, related_name='post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, related_name='post', on_delete=models.CASCADE)
    deleted = models.BooleanField(default=False)
    def __str__(self):
        return self.user.user_name + ' < ' + self.text + ' at ' +self.room.title
    
    image = models.ImageField(upload_to='post', height_field=None, width_field=None, blank=True, max_length=100, default=False)

