from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from .. import models
class BlockTestMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            print(self.request.user)
            print(self.kwargs.get('pk'))
            blockcheck=models.Block.objects.get(blocked=self.request.user,block_id=self.kwargs.get('pk'))
            blockcheck=False
        except:
            blockcheck=True
        print(blockcheck)
        return blockcheck
    
    def handle_no_permission(self):
        return redirect("ul")

def connected_check(self,user):
    result = models.Connect.objects.filter(follower=self.request.user,follow_id=user.pk).exists()
    return result