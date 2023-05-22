from chatrooms.forms import LoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView

class Login(LoginView):
    form_class = LoginForm
    template_name = 'user/login.html'
class Logout(LoginRequiredMixin, LogoutView):
    pass