from django.contrib import admin
from .models import CustomUser, Connect, Room, Post
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Connect)
admin.site.register(Room)
admin.site.register(Post)