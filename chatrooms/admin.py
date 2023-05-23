from django.contrib import admin
from .models import CustomUser, Connect, Block, Room, Post
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Connect)
admin.site.register(Block)
admin.site.register(Room)
admin.site.register(Post)