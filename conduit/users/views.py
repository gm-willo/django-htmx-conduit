from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import redirect


class Login(LoginView):
    template_name = "login.html"
    next_page = reverse_lazy("home")
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.next_page)
        return super().get(request, *args, **kwargs)
    

class Logout(LogoutView):
    next_page = reverse_lazy("home")


class SignUpView(CreateView):
    model = get_user_model()
    fields = ["username", "email", "password"]
    template_name = "signup.html"
    success_url = reverse_lazy("home")
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)
